import json
import os
from dotenv import load_dotenv
from config.database import get_session
from operations.entryops import get_next_entry
from operations.evalops import create_evaluation
from operations.promptops import create_prompt_version_for_run
from operations.responseops import create_response, sample_recent_examples, set_content
from operations.runops import create_run
from schema import State
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

gen_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
eval_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
meta_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

async def create_run_node(state: State) -> dict:
    with get_session() as session:
        out = create_run(session, state["initial_prompt_id"], state["eval_prompt_id"])
    return {"run_id": out["run_id"], "processed_count": 0, "initial_prompt_content": out["initial_prompt_content"], "eval_prompt_content": out["eval_prompt_content"]}

async def get_next_entry_node(state: State) -> dict:
    with get_session() as session:
        nxt = get_next_entry(session, state["processed_count"])
    if not nxt:
        return {"entry_id": None, "entry_content": None}
    return {"entry_id": nxt["entry_id"], "entry_content": nxt["entry_content"]}

async def generate_and_store_node(state: State) -> dict:
    run_id = state["run_id"]
    entry_id = state["entry_id"]
    prompt = state["initial_prompt_content"]
    entry_content = state["entry_content"]

    with get_session() as session:
        response_id = create_response(session, run_id, entry_id)

    output = (await gen_llm.ainvoke([
        # system prompt = prompt version
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Journal entry is a <<TEXT>>:{}  <<History>> : {}  <<RecentResponses>>: {}".format(entry_content, "", "") },
    ])).content

    with get_session() as session:
        set_content(session, response_id, output) 

    return {"response_id": response_id, "model_output": output}

async def evaluate_output_node(state: State) -> dict:
    output = state["model_output"]
    response_id = state["response_id"]

    entry_text = state["entry_content"]

    eval_prompt_template = f""

    eval_msg = [
        SystemMessage(content=eval_prompt_template),
        HumanMessage(content=f"INPUT:\n{entry_text}\n\nOUTPUT:\n{output}"),
    ]
    eval_json_text = (await eval_llm.ainvoke(eval_msg)).content
 
    with get_session() as session:
        response_id = create_evaluation(session, response_id, eval_json_text)

    return {"evaluation_score": json.loads(eval_json_text)}

HARDCODED_META_PROMPT = """You are a prompt optimizer.
Given:
- current prompt
- recent examples (prompt, output, score)
- current output + score
Propose an improved prompt that should increase scores.
Return ONLY the new prompt text.
"""

async def improve_prompt_node(state: State) -> dict:
    run_id = state["run_id"]
    eval_prompt_id = state["eval_prompt_id"]
    evaluation_score = state["evaluation_score"]
    model_output = state["model_output"]
    current_prompt = state["initial_prompt_content"]

    with get_session() as session:
        examples = sample_recent_examples(session,eval_prompt_id)

    meta_input = {
        "current_prompt": current_prompt,
        "recent_examples": examples,
        "current_output": model_output,
        "current_score": evaluation_score,
    }

    msg = [
        SystemMessage(content=HARDCODED_META_PROMPT),
        HumanMessage(content=str(meta_input)),
    ]
    new_prompt = (await meta_llm.ainvoke(msg)).content.strip()
    with get_session() as session:
        create_res = create_prompt_version_for_run(session, run_id, new_prompt)

    return {"proposed_prompt_content": new_prompt, "proposed_prompt_id": create_res["result_prompt_id"]}

def should_continue(state: State):
    if state.get("entry_id") is None:
        return "stop"
    return "go"
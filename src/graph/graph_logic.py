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

    eval_prompt_template = state["eval_prompt_content"]

    eval_msg = [
        SystemMessage(content=eval_prompt_template),
        HumanMessage(content=f"INPUT:\n{entry_text}\n\nRESPONSE:\n{output}"),
    ]
    eval_json_text = (await eval_llm.ainvoke(eval_msg)).content
 
    with get_session() as session:
        response_id = create_evaluation(session, response_id, eval_json_text)

    return {"evaluation_score": json.loads(eval_json_text)}

HARDCODED_META_PROMPT = """You are a deep psychoanalytic supervisor with strong prompt-engineering expertise. 

You are given: 

- a base prompt that generates psychoanalytic interventions for journal entries 
- users journal input and corresponding generated response. 
- evaluation scores for generated response 
- previous examples of entries, responses, and scores 

Your task is to improve the base prompt to increase future evaluation scores. 
Use scores to infer evaluation criteria and identify systematic weaknesses in the prompt. 
Use previous examples to identify general failure patterns, not to optimize for individual cases.
Propose exactly one minimal prompt edit (≤20 words changed) that targets a single weakness. 
When evidence is mixed, prefer changes that improve consistency over expressiveness.
Do not copy language from examples or tailor the prompt to specific entries. Preserve the psychoanalytic stance and intervention style.

OUTPUT FORMAT (JSON ONLY):
{
  "new_prompt": "<the full updated base prompt text>",
  "meta": {
    "change": {
      "edit_description": "<what changed, in one sentence>",
      "before": "<exact fragment changed>",
      "after": "<exact replacement fragment>",
      "words_changed_estimate": <integer>
    },
    "why": [
      "<reason tied to observed scoring weaknesses>",
      "<reason tied to inferred evaluation criteria>"
    ],
    "expected_effect": "<how this should improve scores>"
  }
}

Rules:
- Output valid JSON only. No markdown. No commentary outside JSON.
- Ensure the edit changes ≤20 words.
- Do not invent new constraints unless justified by scores.
"""

async def improve_prompt_node(state: State) -> dict:
    run_id = state["run_id"]
    eval_prompt_id = state["eval_prompt_id"]
    evaluation_score = state["evaluation_score"]
    model_output = state["model_output"]
    current_prompt = state["initial_prompt_content"]
    processed_count= state["processed_count"]

    with get_session() as session:
        examples = sample_recent_examples(session, run_id, eval_prompt_id)

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

    raw_response = (await meta_llm.ainvoke(msg)).content.strip()

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Meta-LLM returned invalid JSON: {raw_response}") from e

    if not isinstance(parsed, dict) or "new_prompt" not in parsed or "meta" not in parsed:
        raise ValueError(f"Meta-LLM JSON must contain top-level keys 'new_prompt' and 'meta': {parsed}")

    new_prompt = parsed["new_prompt"]
    meta = parsed.get("meta") or {}
    with get_session() as session:
        create_res = create_prompt_version_for_run(session, run_id, new_prompt, meta)

    return {"proposed_prompt_content": new_prompt, "proposed_prompt_id": create_res["result_prompt_id"], "processed_count": processed_count+1}

def should_continue(state: State):
    if state.get("entry_id") is None:
        return "stop"
    return "go"
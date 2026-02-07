import asyncio
import sys
from pathlib import Path

# Add parent directory to path to enable imports when running as script
if __name__ == "__main__":
    src_path = Path(__file__).parent
    project_root = src_path.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from langgraph.graph import StateGraph, MessagesState, START, END
from graph.flow import get_graph

async def main():
    graph = get_graph()
    await graph.ainvoke({
        "initial_prompt_id": "",
        "eval_prompt_id": "",
    })

if __name__ == "__main__":
    asyncio.run(main())
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
        "initial_prompt_id": "418a5e54-d013-4056-9df3-ca9ed07ecde8",
        "eval_prompt_id": "3f9f5c00-3da7-4ae6-916d-ac73e0222ff8",
    })

if __name__ == "__main__":
    asyncio.run(main())
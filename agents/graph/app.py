from __future__ import annotations

from agents.graph.nodes import build_graph


def main() -> None:
    workflow = build_graph()
    app = workflow.compile()
    print("LangGraph app compiled successfully.")
    print(app)


if __name__ == "__main__":
    main()

from __future__ import annotations

from agents.graph.nodes import build_graph


def main() -> None:
    analysis = build_graph()
    app = analysis.compile()
    print("LangGraph app compiled successfully.")
    print(app)


if __name__ == "__main__":
    main()

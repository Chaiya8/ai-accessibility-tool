# backend/diagram.py

from graphviz import Digraph
from .simplify import run_instruction  
def extract_steps(text: str) -> list[str]:

    # Use the existing instruction system to get steps from the text.
    steps_text = run_instruction(text, mode="steps", level="8th grade")
    raw_lines = steps_text.splitlines()

    steps = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
       
        if line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()
        if line.startswith("- "):
            line = line[2:].strip()
        steps.append(line)
    return steps[:7]


def create_diagram_svg(steps: list[str]) -> str:
    #Turn a list of step strings into a simple top-to-bottom flowchart.
    dot = Digraph()
    dot.attr(rankdir="TB", fontsize="12", nodesep="0.5", ranksep="0.6")
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="#111827",
             fontcolor="white", color="#00e6c3", penwidth="1.5")

    for i, step in enumerate(steps):
        dot.node(str(i), step)

    for i in range(len(steps) - 1):
        dot.edge(str(i), str(i + 1), color="#00e6c3")
    svg_bytes = dot.pipe(format="svg")
    return svg_bytes.decode("utf-8")

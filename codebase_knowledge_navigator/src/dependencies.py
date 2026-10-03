import re
from pathlib import Path

PY_IMPORT = re.compile(r"^\s*(?:from|import)\s+([A-Za-z0-9_\.]+)", re.M)
JS_IMPORT = re.compile(r"""(?:import\s+.*?\s+from\s+|require\()\s*['"]([^'"]+)['"]""")

def build_dependency_graph(source_dir: Path):
    files = {p.stem: p for p in source_dir.rglob("*") if p.is_file()}
    graph = {}
    for path in files.values():
        text = path.read_text(encoding="utf-8", errors="ignore")
        deps = set()
        for match in PY_IMPORT.findall(text):
            root = match.split(".")[0]
            if root in files and root != path.stem:
                deps.add(root)
        for match in JS_IMPORT.findall(text):
            root = Path(match).stem
            if root in files and root != path.stem:
                deps.add(root)
        graph[str(path.relative_to(source_dir))] = sorted(deps)
    return graph

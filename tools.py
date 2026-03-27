import requests
import ast
import operator as op

SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
}

def _safe_eval(node):
    """Safely evaluates an AST node for supported mathematical operations."""
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        operator = SAFE_OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported operator")
        return operator(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        operator = SAFE_OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported operator")
        return operator(operand)
    raise ValueError("Unsupported expression")


def search_web(query):
    """Searches the web using DuckDuckGo API and returns a summary of the query."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        res = requests.get(url, timeout=8)
        res.raise_for_status()
        json_data = res.json()
        abstract = json_data.get("Abstract")
        if abstract:
            return abstract
        related = json_data.get("RelatedTopics", [])
        if related and isinstance(related, list) and "Text" in related[0]:
            return related[0]["Text"]
        return "No results found"
    except Exception as e:
        return f"Search unavailable: {str(e)}"


def calculator(expr):
    """Calculates the result of a mathematical expression using safe evaluation."""
    try:
        parsed = ast.parse(expr, mode="eval")
        result = _safe_eval(parsed.body)
        return str(result)
    except Exception:
        return "Invalid calculation"

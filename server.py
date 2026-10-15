import ast
import json
import operator
from datetime import datetime, timezone

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Developer utility server")

# Tool 1: Safely evaluate basic arthmetic
@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression using +, -, *, and /."""

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression must be a non-empty string.")

    if len(expression) > 100:
        raise ValueError("Expression is too long.")

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Unsupported arithmetic expression.")

    tree = ast.parse(expression, mode="eval")
    return str(evaluate(tree.body))

# Tool 2: Count words, characters and sentences
@mcp.tool()
def count_words(text:str) -> dict:
    """Count words, characters, and sentences in a text."""

    if not isinstance(text,str):
        raise ValueError("Text must be a string")

    stripped = text.strip()
    sentences = sum(stripped.count(mark) for mark in ".!?")

    return {
        "character_count": len(text),
        "word_count": len(stripped.split()),
        "sentence_count": sentences
    }

#Tool 3: Convert temperature
@mcp.tool()
def convert_temperature(value:float, from_unit:str, to_unit:str)->dict:
    """Convert a temperature between Celsius, Fahrenheit, and Kelvin."""
 
    units = {"C","F","K"}

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("Temperature value must be numeric.")
    
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if from_unit not in units or to_unit not in units:
        raise ValueError("Units must be C, F or K")

    if from_unit=="C":
        celsius = value
    elif from_unit == "F":
        celsius = (value-32)*5/9
    else:
        celsius = value - 273.15

    if celsius < -273.15:
        raise ValueError("Temperature cannot be below absolute zero.")

    if to_unit == "C":
        converted = celsius
    elif to_unit == "F":
        converted = celsius * 9 / 5 + 32
    else:
        converted = celsius + 273.15

    return {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": round(converted, 2),
    }

# Tool 4: Validate and pretty print JSON
@mcp.tool()
def format_json(json_text:str) -> str:
    """Validate JSON text and return formatted JSON."""

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e.msg} from e")

    return json.dumps(parsed, indent=2,ensure_ascii=False)

#Tool 5: Return the current UTC timestamp
@mcp.tool()
def get_timestamp() -> dict:
    """Return the current UTC timestamp in ISO 8601 format."""

    now = datetime.now(timezone.utc)
    return{
        "utc_timestamp": now.isoformat(),
        "unix_timestamp": now.timestamp()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")


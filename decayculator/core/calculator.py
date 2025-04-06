import ast
import operator

from decayculator.core.entropy import GrowingNoiseEntropy
from decayculator.core.models import DecayingNumber
from decayculator.utils.logging import logger


class Calculator:
    """Safely evaluates math expressions using decaying numbers."""

    def __init__(self, entropy_strategy=None):
        self.entropy_strategy = entropy_strategy or GrowingNoiseEntropy()

        # Map basic operators to functions
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

    def evaluate(self, expression: str) -> DecayingNumber:
        """
        Parse and evaluate a simple arithmetic expression.
        Returns a DecayingNumber as result.
        """
        logger.debug(f"Evaluating expression: '{expression}'")
        tree = ast.parse(expression, mode="eval")
        result = self._eval_node(tree.body)
        logger.debug(f"Evaluation complete → DecayingNumber: {result}")
        return result

    def _eval_node(self, node: ast.AST) -> DecayingNumber:

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_func = self.operators[type(node.op)]

            # Combine and return new DecayingNumber
            result_value = op_func(left.read(), right.read())
            return DecayingNumber(result_value, self.entropy_strategy)

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            operand = self._eval_node(node.operand)
            return DecayingNumber(-operand.read(), self.entropy_strategy)

        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return DecayingNumber(node.value, self.entropy_strategy)

        raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

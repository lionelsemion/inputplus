import ast
import operator as op
from abc import ABC, abstractmethod
import sys
import time
import readline


__operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


class InputConstraint(ABC):
    @abstractmethod
    def satisfies(self, value) -> bool:
        pass

    error_message: str


class Constraint:
    class Min(InputConstraint):
        def __init__(self, min_value) -> None:
            super().__init__()
            self.min_value = min_value
            self.error_message = f"Input must be at least {min_value}"

        def satisfies(self, value) -> bool:
            return value >= self.min_value

    class Max(InputConstraint):
        def __init__(self, max_value) -> None:
            super().__init__()
            self.max_value = max_value
            self.error_message = f"Input must be at most {max_value}"

        def satisfies(self, value) -> bool:
            return value <= self.max_value

    class Min(InputConstraint):
        def __init__(self, min_value) -> None:
            super().__init__()
            self.min_value = min_value
            self.error_message = f"Input must be greater than {min_value}"

        def satisfies(self, value) -> bool:
            return value > self.min_value

    class Max(InputConstraint):
        def __init__(self, max_value) -> None:
            super().__init__()
            self.max_value = max_value
            self.error_message = f"Input must be less than {max_value}"

        def satisfies(self, value) -> bool:
            return value < self.max_value

    class DivisibleBy(InputConstraint):
        def __init__(self, quotient) -> None:
            super().__init__()
            self.quotient = quotient
            self.error_message = f"Input must be divisible by {quotient}"

        def satisfies(self, value) -> bool:
            return value % self.quotient == 0

    class NotDivisibleBy(InputConstraint):
        def __init__(self, quotient) -> None:
            super().__init__()
            self.quotient = quotient
            self.error_message = f"Input must not be divisible by {quotient}"

        def satisfies(self, value) -> bool:
            return value % self.quotient != 0

    class MinLen(InputConstraint):
        def __init__(self, min_len) -> None:
            super().__init__()
            self.min_len = min_len
            self.error_message = f"Input must have at least {min_len} characters"

        def satisfies(self, value) -> bool:
            return len(value) >= self.min_len

    class MaxLen(InputConstraint):
        def __init__(self, max_len) -> None:
            super().__init__()
            self.max_len = max_len
            self.error_message = f"Input must have at most {max_len} characters"

        def satisfies(self, value) -> bool:
            return len(value) <= self.max_len

    class Int(InputConstraint):
        def __init__(self) -> None:
            super().__init__()
            self.error_message = f"Input must be an integer"

        def satisfies(self, value) -> bool:
            return value % 1 == 0


def __eval_expr(expr):
    return __eval_(ast.parse(expr, mode="eval").body)


def __eval_(node):
    match node:
        case ast.Constant(value) if isinstance(value, (int, float)):
            return value
        case ast.BinOp(left, op, right):
            return __operators[type(op)](__eval_(left), __eval_(right))
        case ast.UnaryOp(op, operand):
            return __operators[type(op)](__eval_(operand))
        case _:
            raise TypeError(node)


def __try_to_convert_to_float(text: str) -> int | None:
    try:
        return float(text)
    except ValueError:
        try:
            return __eval_expr(text)
        except TypeError:
            return None
        except SyntaxError:
            return None


def __get_first_constraint_error(
    value, constraints: tuple[InputConstraint]
) -> str | None:
    for constraint in constraints:
        if not constraint.satisfies(value):
            return constraint.error_message


def input_int(prompt: str, input_constraints: tuple[InputConstraint] = ()) -> int:
    return int(input_float(prompt, input_constraints + (Constraint.Int(),)))


def input_float(prompt: str, input_constraints: tuple[InputConstraint] = ()) -> int:
    while 1:
        while 1:
            text = input(prompt + "\n").strip()
            x = __try_to_convert_to_float(text)
            if x is None:
                print("Invalid expression")
                continue
            break
        error = __get_first_constraint_error(x, input_constraints)
        if error is not None:
            print(error)
            continue
        break
    return x


def input_string(prompt: str, input_constraints: tuple[InputConstraint] = ()) -> int:
    while 1:
        text = input(prompt + "\n")
        x = text.strip()
        error = __get_first_constraint_error(x, input_constraints)
        if error is not None:
            print(error)
            continue
        break
    return x


print(input_string("What's your name? ", (Constraint.MinLen(2), Constraint.MaxLen(35))))
print(input_int("What's your body count? ", (Constraint.Min(0),)))


# for x in range(0, 5):
#     b = "Loading" + "." * x
#     print(b, end="", flush=True)
#     sys.stdout.write("\033[2K\033[1G")
#     time.sleep(1)

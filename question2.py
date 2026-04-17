# evaluator.py

import os
import math

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type  # NUM, OP, LPAREN, RPAREN, END
        self.value = value      # for NUM tokens, the numeric value; for OP, the operator char

    def __repr__(self):
        if self.type == "NUM":
            return f"[NUM:{self.value}]"
        elif self.type == "OP":
            return f"[OP:{self.value}]"
        elif self.type == "LPAREN":
            return "[LPAREN:(]"
        elif self.type == "RPAREN":
            return "[RPAREN:)]"
        else:
            return f"[{self.type}]"

class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0
        self.length = len(expression)

    def get_next_token(self):
        # Skip whitespace
        while self.pos < self.length and self.expression[self.pos].isspace():
            self.pos += 1

        if self.pos >= self.length:
            return Token("END")

        current_char = self.expression[self.pos]

        # Handle numbers
        if current_char.isdigit() or current_char == '.':
            start = self.pos
            has_decimal = False
            while self.pos < self.length and (self.expression[self.pos].isdigit() or self.expression[self.pos] == '.'):
                if self.expression[self.pos] == '.':
                    if has_decimal:
                        # Invalid number with two decimals
                        raise ValueError("Invalid number format")
                    has_decimal = True
                self.pos += 1

            num_str = self.expression[start:self.pos]
            try:
                value = float(num_str) if '.' in num_str else int(num_str)
            except ValueError:
                raise ValueError(f"Invalid number format: {num_str}")
            return Token("NUM", value)

        # Handle operators
        if current_char in '+-*/':
            self.pos += 1
            return Token("OP", current_char)

        # Handle parentheses
        if current_char == '(':
            self.pos += 1
            return Token("LPAREN")

        if current_char == ')':
            self.pos += 1
            return Token("RPAREN")

        # Unsupported characters
        raise ValueError(f"Unsupported character: {current_char}")

    def tokenize(self):
        tokens = []
        try:
            while True:
                token = self.get_next_token()
                tokens.append(token)
                if token.type == "END":
                    break
            return tokens
        except ValueError as e:
            return None

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def match(self, expected_type, expected_value=None):
        if self.current_token and self.current_token.type == expected_type:
            if expected_value is None or self.current_token.value == expected_value:
                self.advance()
                return True
        return False

    def parse_expression(self):
        """Parse addition and subtraction (lowest precedence)"""
        node = self.parse_term()

        while self.current_token and self.current_token.type == "OP" and self.current_token.value in ('+', '-'):
            op = self.current_token.value
            self.advance()
            right = self.parse_term()
            node = (op, node, right)

        return node

    def parse_term(self):
        """Parse multiplication and division"""
        node = self.parse_factor()

        while self.current_token and self.current_token.type == "OP" and self.current_token.value in ('*', '/'):
            op = self.current_token.value
            self.advance()
            right = self.parse_factor()
            node = (op, node, right)

        return node

    def parse_factor(self):
        """Parse unary negation and parentheses"""
        # Handle unary negation
        if self.current_token and self.current_token.type == "OP" and self.current_token.value == '-':
            self.advance()
            operand = self.parse_factor()
            return ('neg', operand)

        # Handle parentheses
        if self.current_token and self.current_token.type == "LPAREN":
            self.advance()
            node = self.parse_expression()
            if not (self.current_token and self.current_token.type == "RPAREN"):
                raise ValueError("Missing closing parenthesis")
            self.advance()
            return node

        # Handle numbers
        if self.current_token and self.current_token.type == "NUM":
            value = self.current_token.value
            self.advance()
            return value

        raise ValueError("Unexpected token")

    def parse(self):
        try:
            tree = self.parse_expression()
            if self.current_token and self.current_token.type != "END":
                raise ValueError("Unexpected tokens after expression")
            return tree
        except ValueError:
            return None

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, tree):
        """Evaluate the parse tree and return the result"""
        if isinstance(tree, (int, float)):
            return float(tree)

        if isinstance(tree, tuple):
            if tree[0] == '+':
                return self.evaluate(tree[1]) + self.evaluate(tree[2])
            elif tree[0] == '-':
                return self.evaluate(tree[1]) - self.evaluate(tree[2])
            elif tree[0] == '*':
                return self.evaluate(tree[1]) * self.evaluate(tree[2])
            elif tree[0] == '/':
                right = self.evaluate(tree[2])
                if right == 0:
                    raise ValueError("Division by zero")
                return self.evaluate(tree[1]) / right
            elif tree[0] == 'neg':
                return -self.evaluate(tree[1])

        raise ValueError("Invalid tree structure")

    def tree_to_string(self, tree):
        """Convert the parse tree to string representation"""
        if isinstance(tree, (int, float)):
            # Format number: remove .0 if whole number
            if isinstance(tree, float) and tree.is_integer():
                return str(int(tree))
            elif isinstance(tree, int):
                return str(tree)
            else:
                # Round to remove floating point artifacts
                return str(round(tree, 10))

        if isinstance(tree, tuple):
            if tree[0] == 'neg':
                return f"(neg {self.tree_to_string(tree[1])})"
            else:
                return f"({tree[0]} {self.tree_to_string(tree[1])} {self.tree_to_string(tree[2])})"

        return str(tree)

def evaluate_file(input_path: str) -> list[dict]:
    """
    Read expressions from input file, evaluate each one, and write results to output.txt

    Args:
        input_path: Path to the input text file

    Returns:
        List of dictionaries containing evaluation results for each expression
    """
    results = []

    # Read input file
    try:
        with open(input_path, 'r') as f:
            expressions = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        print(f"Error reading input file: {e}")
        return results

    # Process each expression
    for expr in expressions:
        if not expr.strip():  # Skip empty lines
            continue

        result_dict = {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

        # Tokenize
        lexer = Lexer(expr)
        tokens = lexer.tokenize()

        if tokens is None:
            # Tokenization error
            results.append(result_dict)
            continue

        # Convert tokens to string representation
        token_str = ''.join(str(token) for token in tokens if token.type != "END")
        token_str += "[END]"
        result_dict["tokens"] = token_str

        # Parse
        parser = Parser(tokens)
        tree = parser.parse()

        if tree is None:
            # Parse error
            results.append(result_dict)
            continue

        # Convert tree to string
        evaluator = Evaluator()
        tree_str = evaluator.tree_to_string(tree)
        result_dict["tree"] = tree_str

        # Evaluate
        try:
            eval_result = evaluator.evaluate(tree)
            # Format result
            if isinstance(eval_result, float):
                if eval_result.is_integer():
                    result_dict["result"] = int(eval_result)
                else:
                    # Round to 4 decimal places
                    result_dict["result"] = round(eval_result, 4)
            else:
                result_dict["result"] = eval_result
        except Exception:
            # Evaluation error
            result_dict["result"] = "ERROR"

        results.append(result_dict)

    # Write output file
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    try:
        with open(output_path, 'w') as f:
            for i, result in enumerate(results):
                f.write(f"Input: {result['input']}\n")
                f.write(f"Tree: {result['tree']}\n")
                f.write(f"Tokens: {result['tokens']}\n")
                f.write(f"Result: {result['result']}\n")
                if i < len(results) - 1:
                    f.write("\n")
    except Exception as e:
        print(f"Error writing output file: {e}")

    return results

# Example usage when run as a script
if __name__ == "__main__":
    # For testing with sample_input.txt in the same directory
    results = evaluate_file("sample_input.txt")

    # Print results to console
    for result in results:
        print(f"Input: {result['input']}")
        print(f"Tree: {result['tree']}")
        print(f"Tokens: {result['tokens']}")
        print(f"Result: {result['result']}")
        print()
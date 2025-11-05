from syntax import Syntax, InnerSyntax

class Instruction:
    def __init__(self, lineNumber):
        # ["PRINT", ["Hello"], 2] or ["DECLARE_NUM", ["A", 2], 1]
        self.command: str = None # "PRINT", "DECLARE_NUM", ...
        self.data: list = None # ["Hello"], ["A", 2], ...
        self.executionAmount: str = None # 2, 1, ...
        self.lineNumber: int = lineNumber

    # Getters
    def get_command(self) -> str: return self.command
    def get_data(self) -> list: return self.data
    def get_execution_amount(self) -> str: return self.executionAmount
    def get_line_number(self) -> int: return self.lineNumber

    # Setters
    def set_command(self, command: str): self.command = command
    def set_data(self, data: list): self.data = data
    def set_execution_amount(self, amount: str): self.executionAmount = amount

    # toString()
    def __repr__(self):
        return f"Inst: ({self.command}: {self.data} x{self.executionAmount} [Line {self.lineNumber}])"
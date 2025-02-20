class Instruction:
    def __init__(self):
        self.command: str = None
        self.data: list = None
        self.executionAmount: str = None

    # Getters
    def get_command(self) -> str: return self.command
    def get_data(self) -> list: return self.data
    def get_execution_amount(self) -> str: return self.executionAmount

    # Setters
    def set_command(self, command: str): self.command = command
    def set_data(self, data: list): self.data = data
    def set_execution_amount(self, amount: str): self.executionAmount = amount

    # toString()
    def __repr__(self):
        return f"[{self.command} [{self.data}] x{self.executionAmount}"
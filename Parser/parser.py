class Parser:
    def __init__(self):
        self.instructions = None
    
    def execute(self, instructions: list):
        self.instructions = instructions
        print(instructions)
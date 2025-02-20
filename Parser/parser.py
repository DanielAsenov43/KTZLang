class Parser:
    def __init__(self):
        self.instructions = None
    
    def execute(self, instructions: list):
        # TODO convert an instruction to its own class, instead of using lists.
        self.instructions = instructions
        #print(instructions)
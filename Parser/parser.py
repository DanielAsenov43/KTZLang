from instruction import Instruction
from syntax import Syntax, InnerSyntax
from errors import Error, ErrorType

from variable import Variable

class Parser:
    def __init__(self):
        self.instructions = None
        self.globalVariables = []
    
    def execute(self, instructions: list):
        self.instructions = instructions
        for instruction in instructions:
            match(instruction.get_command()):

                # Variable declarations
                case InnerSyntax.VAR_DECLARE_NUM: self.__declare_new_variable(instruction, Syntax.VAR_NUMBER)
                case InnerSyntax.VAR_DECLARE_TEXT: self.__declare_new_variable(instruction, Syntax.VAR_TEXT)
                case InnerSyntax.VAR_DECLARE_BOOLEAN: self.__declare_new_variable(instruction, Syntax.VAR_BOOLEAN)
                
                # Variable updates
                case InnerSyntax.VAR_UPDATE:
                    updatedVarName = instruction.get_data()[0]
                    updatedVarValue = instruction.get_data()[1]

                case InnerSyntax.PRINT:
                    content = instruction.get_data()[0]
                    if("[" in content or "]" in content):
                        # TODO make the PRINT [a] work (probably recursively)
                        pass
                case _:
                    Error.throw(ErrorType.UNKNOWN_INSTRUCTION_TYPE, instruction.get_line_number())
        print("\n".join([str(x) for x in self.globalVariables]))

    def __declare_new_variable(self, instruction: Instruction, variableType: Syntax):
        varName = instruction.get_data()[0]
        varValue = instruction.get_data()[1]
        for globalVariable in self.globalVariables:
            if(globalVariable.get_name() == varName): Error.throw(ErrorType.VAR_REDECLARATION)
        variable = Variable(variableType, varName, varValue)
        self.globalVariables.append(variable)
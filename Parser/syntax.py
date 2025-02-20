from errors import Error, ErrorType
from instruction import Instruction
from enum import StrEnum

class Syntax(StrEnum): # Code syntax
    SCRIPT_START = "START"
    SCRIPT_END = "END"
    COMMENT = "#"

    PRINT = "PRINT"

    VAR_NUMBER = "NUM"
    VAR_TEXT = "TXT"
    VAR_BOOLEAN = "BOOL"
    VAR_DECLARATION = "="

    VAR_BOOLEAN_TRUE = "TRUE"
    VAR_BOOLEAN_FALSE = "FALSE"

    VAR_NUM_INCREASE = "+"
    VAR_NUM_DECREASE = "-"
    VAR_NUM_MULTIPLY = "*"
    VAR_NUM_DIVIDE = "/"
    VAR_NUM_POWER = "^"

class InnerSyntax: # Syntax understood by the machine internally
    EXECUTION_AMOUNT = "_"
    PRINT = "PRINT" # PRINT Hello, World!
    VAR_DECLARE_NUM = "DECLARE_NUM" # NUM A = 5
    VAR_DECLARE_TEXT = "DECLARE_TEXT" # NUM A = 5
    VAR_DECLARE_BOOLEAN = "DECLARE_BOOLEAN" # NUM A = 5
    VAR_UPDATE = "UPDATE" # A = 2

# =============================================================================================

class SyntaxChecker:
    def check_line_get_instruction(line: str, lineNumber: int) -> Instruction:
        instruction = Instruction()
        amountIndex = line.find(InnerSyntax.EXECUTION_AMOUNT)
        amount = line[0:amountIndex]
        command = line[amountIndex + 1:]
        commandType = SyntaxChecker.get_command_type(command)
        match(commandType):
            case Syntax.VAR_NUMBER:
                instructionData = SyntaxChecker.__check_var_num_declaration(command, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_NUM)
                instruction.set_data(instructionData)
                amount = 1 # Declarations can only be executed once

            case Syntax.VAR_BOOLEAN:
                instructionData = SyntaxChecker.__check_var_bool_declaration(command, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_BOOLEAN)
                amount = 1 # Declarations can only be executed once

            case Syntax.VAR_TEXT:
                instructionData = SyntaxChecker.__check_var_text_declaration(command, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_TEXT)
                amount = 1 # Declarations can only be executed once

            case Syntax.PRINT:
                instructionData = SyntaxChecker.__check_print(command, lineNumber)
                instruction.set_command(InnerSyntax.PRINT)

            case InnerSyntax.VAR_UPDATE:
                print("VAR_UPDATE -> " + command)
                pass

        instruction.set_execution_amount(amount)
        return instruction
    
    # Check if a "variableType" variable is declared correctly (NUM A = 5, BOOL B = TRUE, TXT C = Hi, etc)
    # Returns the string that the variable is assigned, regardless of type, to be checked by the other functions
    def __check_var_declaration(line: str, lineNumber: int) -> list:
        if(Syntax.VAR_DECLARATION not in line): Error.throw(ErrorType.VAR_MISSING_DECLARATION_CHARACTER, lineNumber)
        variableDeclarationIndex = line.find(Syntax.VAR_DECLARATION)
        variableName = line[0:variableDeclarationIndex]
        variableValue = line[variableDeclarationIndex+1:]
        #print(f"Declared {variableType} variable: '{variableName}' -> '{variableValue}'")
        if(len(variableName) <= 0): Error.throw(ErrorType.VAR_MISSING_NAME, lineNumber)
        if(len(variableValue) <= 0): Error.throw(ErrorType.VAR_MISSING_VALUE, lineNumber)
        try:
            variableName = int(variableName)
            Error.throw(ErrorType.VAR_NAME_IS_A_NUMBER, lineNumber)
        except ValueError:
            return [variableName, variableValue]
        

    def __check_var_num_declaration(line: str, lineNumber: int) -> list:
        instructionData = SyntaxChecker.__check_var_declaration(line, Syntax.VAR_NUMBER, lineNumber)
        # TODO
        return instructionData

    def __check_var_text_declaration(line: str, lineNumber: int) -> list:
        instructionData = SyntaxChecker.__check_var_declaration(line, Syntax.VAR_TEXT, lineNumber)
        # TODO
        return instructionData

    def __check_var_bool_declaration(line: str, lineNumber: int) -> list:
        instructionData = SyntaxChecker.__check_var_declaration(line, Syntax.VAR_BOOLEAN, lineNumber)
        variableName = line.split(Syntax.VAR_DECLARATION)[0]
        match(instructionData[1]):
            case Syntax.VAR_BOOLEAN_TRUE: instructionData = [variableName, True]
            case Syntax.VAR_BOOLEAN_FALSE: instructionData = [variableName, False]
            case _: Error.throw(ErrorType.VAR_BOOLEAN_INVALID_VALUE.replace("[VAR_VALUE]", instructionData[1]), lineNumber)
        return instructionData
    
    def __check_print(line: str, lineNumber: int) -> list:
        return [line]
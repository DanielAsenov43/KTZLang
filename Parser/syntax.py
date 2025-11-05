from errors import Error, ErrorType
from enum import StrEnum
import re

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
    def check_line_get_instruction(line: str, lineNumber: int): # Returns an Instruction object
        from instruction import Instruction # This is necessary to avoid circular imports
        from syntaxUtils import SyntaxUtils

        instruction = Instruction(lineNumber)
        amountIndex = line.find(InnerSyntax.EXECUTION_AMOUNT)
        amount = line[0:amountIndex]
        command = line[amountIndex + 1:]
        commandType = SyntaxUtils.get_command_type(command)
        
        match(commandType):
            case Syntax.VAR_NUMBER:
                instructionData = SyntaxChecker.__check_var_declaration(command, Syntax.VAR_NUMBER, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_NUM)
                amount = 1 # Declarations can only be executed once

            case Syntax.VAR_BOOLEAN:
                instructionData = SyntaxChecker.__check_var_declaration(command, Syntax.VAR_BOOLEAN, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_BOOLEAN)
                amount = 1 # Declarations can only be executed once

            case Syntax.VAR_TEXT:
                instructionData = SyntaxChecker.__check_var_declaration(command, Syntax.VAR_TEXT, lineNumber)
                instruction.set_command(InnerSyntax.VAR_DECLARE_TEXT)
                amount = 1 # Declarations can only be executed once

            case Syntax.PRINT:
                instructionData = SyntaxChecker.__check_print(command, lineNumber)
                instruction.set_command(InnerSyntax.PRINT)

            case InnerSyntax.VAR_UPDATE:
                instructionData = SyntaxChecker.__check_var_update(command, lineNumber)
                instruction.set_command(InnerSyntax.VAR_UPDATE)
                amount = 1
                pass
        
        instruction.set_data(instructionData)
        instruction.set_execution_amount(amount)
        return instruction
    
    def __check_valid_variable_name(name: str, lineNumber: int):
        from syntaxUtils import SyntaxUtils
        # 1. The variable name can't be empty (eg. "NUM = 2")
        if(len(name) <= 0): Error.throw(ErrorType.VAR_MISSING_NAME, lineNumber)
        # 2. The variable name can't be a number (eg. "NUM 1 = 2")
        try:
            name = float(name)
            Error.throw(ErrorType.VAR_NAME_IS_A_NUMBER, lineNumber)
        except ValueError: pass
        # 3. The variable name can't be a built-in syntax structure/command (eg. "TXT PRINT = Hi")
        # This also checks for (+, -, *, /, ^, ...). Not ideal but it works for now.
        if(SyntaxUtils.is_regular_command(name)): Error.throw(ErrorType.VAR_NAME_HAS_BUILT_IN_SYNTAX, lineNumber)
        if(re.findall(f"!({SyntaxUtils.get_variable_name_regex()})", name)):
            Error.throw(ErrorType.VAR_NAME_HAS_INVALID_CHARACTER, lineNumber, "{NAME}", name)

    # Check if a "variableType" variable is declared correctly (NUM A = 5, BOOL B = TRUE, TXT C = Hi, etc)
    # Returns the variable type concatenated to the variable name, 
    def __check_var_declaration(line: str, variableType: str, lineNumber: int) -> list:
        if(Syntax.VAR_DECLARATION not in line): Error.throw(ErrorType.VAR_MISSING_DECLARATION_CHARACTER, lineNumber) # missing an "=" sign
        variableDeclarationIndex = line.find(Syntax.VAR_DECLARATION) # "=" sign
        variableName = line[len(variableType):variableDeclarationIndex] # "a"
        variableValue = line[variableDeclarationIndex+1:] # "2"

        SyntaxChecker.__check_valid_variable_name(variableName, lineNumber)
        if(len(variableValue) <= 0): Error.throw(ErrorType.VAR_MISSING_VALUE, lineNumber)
        return [variableName, variableValue]
    
    def __check_print(line: str, lineNumber: int) -> list:
        value = line[len(Syntax.PRINT):]
        return [value]
    
    def __check_var_update(line: str, lineNumber: int) -> list: # a = 2, a++2, a^^2, ...
        variableDeclarationIndex = line.find(Syntax.VAR_DECLARATION) # "=" sign
        if(variableDeclarationIndex == 1):
            # TODO check other types of updates (++, --, ...)
            pass
        variableName = line[0:variableDeclarationIndex] # "a"
        variableValue = line[variableDeclarationIndex+1:] # "2
        return [variableName, variableValue]
from errors import Error, ErrorType
from enum import StrEnum
import re

class Syntax(StrEnum): # Code syntax
    SCRIPT_START = "START"
    SCRIPT_END = "END"
    COMMENT = "#"
    VAR_NUMBER = "NUM"
    VAR_TEXT = "TXT"
    VAR_BOOLEAN = "BOOL"
    VAR_DECLARATION = "="
    VAR_BOOLEAN_TRUE = "TRUE"
    VAR_BOOLEAN_FALSE = "FALSE"
    PRINT = "PRINT"


class InnerSyntax: # Syntax understood by the machine internally
    EXECUTION_AMOUNT = "_"
    PRINT = "PRINT" # PRINT Hello, World!
    VAR_DECLARE_NUM = "DECLARE_NUM" # NUM A = 5
    VAR_DECLARE_TEXT = "DECLARE_TEXT" # NUM A = 5
    VAR_DECLARE_BOOLEAN = "DECLARE_BOOLEAN" # NUM A = 5
    VAR_UPDATE = "UPDATE" # A = 2


'''
[
    ["PRINT": ["Text"], 2],
    ["DECLARE": ["A", "5"], 1],
    ["DECLARE": ["B", "10"], 1],
    ["UPDATE": ["A", "Hi"], 1], # Error
    ["UPDATE": ["A", "[A + 2]"], 1],
    ["PRINT": ["2 + 2 = [A]"], 3]
]
'''

class SyntaxChecker:
    def check_line_get_instruction(line: str, syntaxType: str, lineNumber: int) -> list:
        instruction = None
        instructionSyntax = None
        instructionData = []
        command = InnerSyntax.EXECUTION_AMOUNT.join(line.split(InnerSyntax.EXECUTION_AMOUNT)[1:])
        amount = line.split(InnerSyntax.EXECUTION_AMOUNT)[0]
        match(syntaxType):
            case Syntax.VAR_NUMBER:
                instructionData = SyntaxChecker.__check_var_num_declaration(command, lineNumber)
                instructionSyntax = InnerSyntax.VAR_DECLARE_NUM; amount = 1 # Can only be declared once
            case Syntax.VAR_BOOLEAN:
                instructionData = SyntaxChecker.__check_var_bool_declaration(command, lineNumber)
                instructionSyntax = InnerSyntax.VAR_DECLARE_BOOLEAN; amount = 1 # Can only be declared once
            case Syntax.VAR_TEXT:
                instructionData = SyntaxChecker.__check_var_text_declaration(command, lineNumber)
                instructionSyntax = InnerSyntax.VAR_DECLARE_TEXT; amount = 1 # Can only be declared once
            case Syntax.PRINT:
                instructionData = SyntaxChecker.__check_print(command, lineNumber)
                instructionSyntax = InnerSyntax.PRINT
            case _:
                variableUpdate = re.findall(f"\S*\s*{Syntax.VAR_DECLARATION}\s*\S*")[0] # A = 5
                if(variableUpdate):
                    match = re.findall(f"\S*\s*{Syntax.VAR_DECLARATION}\s*")[0]
                    matchIndex = len(match)
                    match.replace(" ", "")
                    variableName = match.split(Syntax.VAR_DECLARATION)[0]
                    value = match + command[matchIndex:]
                    print(f"Update -> {variableName} -> {value}")
                else:
                    print(f"Unknown -> {syntaxType} {command}")

        # ["PRINT", ["Text"], 2]  or  ["DECLARE", ["A", "5"], 1]
        return [instructionSyntax, instructionData, str(amount)] if instructionSyntax else None
    
    # Check if a "variableType" variable is declared correctly (NUM A = 5, BOOL B = TRUE, TXT C = Hi, etc)
    # Returns the string that the variable is assigned, regardless of type, to be checked by the other functions
    def __check_var_declaration(line: str, variableType: str, lineNumber: int) -> list:
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
        return instructionData

    def __check_var_text_declaration(line: str, lineNumber: int) -> list:
        instructionData = SyntaxChecker.__check_var_declaration(line, Syntax.VAR_TEXT, lineNumber)
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
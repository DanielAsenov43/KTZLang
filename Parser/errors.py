import sys

class ErrorType:
    # General
    FILE_NOT_FOUND = "File not found"
    MISSING_START = "Missing START statement at the start of the script"
    MISSING_END = "Missing END statement at the end of the script"
    END_BEFORE_START = "START must be defined before END"
    MULTIPLE_STARTS = "There must only be one START statement"
    MULTIPLE_ENDS = "There must only be one END statement"

    # Code execution errors
    UNKNOWN_COMMAND = "Unknown command"
    UNKNOWN_INSTRUCTION_TYPE = "(Internal) The instruction type is unknown"
    
    # General variable errors
    VAR_MISSING_NAME = "The variable must have a name"
    VAR_NAME_IS_A_NUMBER = "The variable name must not be a number"
    VAR_NAME_HAS_BUILT_IN_SYNTAX = "The variable name must not contain any operators or built-in syntax"
    VAR_NAME_HAS_OPERATOR = "The variable name must not contain operators"
    VAR_NAME_HAS_INVALID_CHARACTER = "The variable name \"{NAME}\" contains an invalid character"
    VAR_MISSING_DECLARATION_CHARACTER = "Missing '=' syntax when declaring a variable"
    VAR_MISSING_VALUE = "The variable must have a value"

    VAR_REDECLARATION = "The variable \"{VAR_NAME}\" has already been declared"

    # Boolean variables
    VAR_BOOLEAN_INVALID_VALUE = "The boolean variable must be TRUE or FALSE (not \"{VAR_VALUE}\")" # Circular import, cant use Syntax.VAR_BOOLEAN_TRUE

    # Updating variables
    VAR_UPDATE_INVALID_OPERATOR = "\"{OPERATOR}\" is not a valid operator"

PREFIX = "[!] ERROR: "
LINE_NUMBER = " [LINE {LINE-NUMBER}]"
class Error:
    def throw(errorType: ErrorType, lineNumber, find=None, replace=None):
        if(find and replace): errorType = errorType.replace(find, replace)
        print(PREFIX + errorType + LINE_NUMBER.replace("{LINE-NUMBER}", str(lineNumber)))
        sys.exit(0)



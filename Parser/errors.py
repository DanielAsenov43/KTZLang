class ErrorType:
    # General
    FILE_NOT_FOUND = "File not found"
    MISSING_START = "Missing START statement at the start of the script"
    MISSING_END = "Missing END statement at the end of the script"
    END_BEFORE_START = "START must be defined before END"
    MULTIPLE_STARTS = "There must only be one START statement"
    MULTIPLE_ENDS = "There must only be one END statement"
    
    # General variable errors
    VAR_MISSING_NAME = "The variable must have a name"
    VAR_NAME_IS_A_NUMBER = "The variable name must not be a number"
    VAR_MISSING_DECLARATION_CHARACTER = "Missing '=' syntax when declaring a variable"
    VAR_MISSING_VALUE = "The variable must have a value"

    # Boolean variables
    VAR_BOOLEAN_INVALID_VALUE = f"The boolean variable must be TRUE or FALSE (not '[VAR_VALUE]')" # Circular import, cant use Syntax.VAR_BOOLEAN_TRUE


PREFIX = "[!] ERROR: "
LINE_NUMBER = " [LINE {LINE-NUMBER}]"
class Error:
    def throw(errorType: ErrorType, *lineIndex):
        if(not lineIndex): print(PREFIX + errorType)
        else: print(PREFIX + errorType + LINE_NUMBER.replace("{LINE-NUMBER}", str(lineIndex[0])))
        exit(1)



from syntax import Syntax, InnerSyntax
import re

class SyntaxUtils:

    # CONSTANTS -------------------------------------------------------
    def get_update_character_amount() -> int: return 2 # Number of characters to update a variable ("A+2", "A++2", "A+++2", ...)

    # OPERATORS ----------------------------------------------------------------
    def get_number_operators() -> list: return [Syntax.VAR_NUM_INCREASE, Syntax.VAR_NUM_DECREASE, Syntax.VAR_NUM_MULTIPLY, Syntax.VAR_NUM_DIVIDE, Syntax.VAR_NUM_POWER]
    def get_operators() -> list: return SyntaxUtils.get_number_operators() + [Syntax.VAR_DECLARATION]
    
    # GETTING THE SYNTAX FROM A COMMAND ----------------------------------------
    def get_command_type(command: str) -> str:
        for syntax in list(map(str, Syntax)): # Check for regular commands
            if(command[0:len(syntax)] == syntax): return syntax
        return InnerSyntax.VAR_UPDATE if SyntaxUtils.is_update_command(command) else None
    
    # REGEX -----------------------------------------------------
    def get_variable_name_regex() -> str: return r"([A-Za-z_][A-Za-z_\d]*)"
    def get_variable_value_regex() -> str: return r"[A-Za-z_\d\\" + str("\\".join(SyntaxUtils.get_number_operators())) + "\[\]]+"
    def get_operator_regex() -> str: return "(" + "|".join([f"\\{x}" * SyntaxUtils.get_update_character_amount() for x in SyntaxUtils.get_operators()]) + ")"

    def clear_execution_amount(command: str) -> str: # Converts "2_PRINT Hello" to "PRINT Hello"
        return command[command.find(InnerSyntax.EXECUTION_AMOUNT)+1:] if InnerSyntax.EXECUTION_AMOUNT in command else command
    
    # CHECKING THE COMMAND TYPE -----------------------------------------------
    def is_regular_command(command: str, stripExecutionAmount: bool = False) -> bool: # Check if the command contains regular syntax ("PRINT", "NUM", ...)
        if(stripExecutionAmount): command = SyntaxUtils.clear_execution_amount(command)
        for syntax in list(map(str, Syntax)):
            if(command[0:len(syntax)] == syntax): return True
        return False
    
    def is_update_command(command: str) -> bool: # Check if the command contains a variable update or assignment ("A++2", "MyText = Hello")
        if(SyntaxUtils.is_regular_command(command)): return False
        return (SyntaxUtils.is_number_update_command(command) or SyntaxUtils.is_variable_assign_command(command))
    
    def is_number_update_command(command: str) -> bool: # Check if the command contains a variable update ("A++2")
        command = SyntaxUtils.clear_execution_amount(command)
        updateCharacterAmount = SyntaxUtils.get_update_character_amount()
        operatorRegex = SyntaxUtils.get_operator_regex() # (\+\+|\-\-|etc...)
        variableNameRegex = SyntaxUtils.get_variable_name_regex()
        variableValueRegex = SyntaxUtils.get_variable_value_regex()
        return True if re.match(fr"{variableNameRegex}\s*{operatorRegex}\s*{variableValueRegex}", command) else False
    
    def is_variable_assign_command(command: str, stripExecutionAmount: bool = False) -> bool: # Check if the command contains a variable assignment ("A = 5", "MyText = Hello")
        if(stripExecutionAmount): command = SyntaxUtils.clear_execution_amount(command)
        return True if re.findall(r"[A-Za-z][A-Za-z|\d]*\s*=\s*[A-Za-z\d\s\[\]\+\-\*\/]+", command) else False
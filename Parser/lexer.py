from syntax import Syntax, SyntaxChecker
from errors import Error, ErrorType # Shhh
from extras import Extras, InnerExtras

class Lexer:
    def __init__(self):
        self.lines = None # {1: "NUM a = 2", 2: "PRINT Hello", ...} (Stores their line numbers)
        self.variables = {} # {"a": 2, "b": "sup", ...}
        self.functions = {} # No idea lmao
        self.instructions = [] # [["DECLARE", ["A", 5], 1], ["PRINT", ["Hello"], 4], ...]
    
    def analyze(self, lines: str) -> list:
        self.lines = self.__convert_lines_to_dict(lines)
        self.__first_sweep() # Remove all unnecessary lines, spaces, tabs, comments and lines before START and after END, and check for basic syntax problems.
        self.__second_sweep() # Convert everything into a list of instructions [["DECLARE_NUM", ["A", 5], 1], ["PRINT", ["Hello"], 4], ...]
        return self.instructions # Return the instructions so the parser can execute them
    
    def __convert_lines_to_dict(self, lines: str) -> dict: # Converts ["line1", "line2"] to {1: "line1", 2: "line2"}, starting from 1
        return {i + 1:lines[i] for i in range(len(lines))}
    
    def linelist(self) -> list: # Returns the values of self.lines, so instead of {1: "line1", 2: "line2"} you get ["line1", "line2"]
        return list(self.lines.values())

    def __first_sweep(self): # This will remove comments, tabs, empty lines, lines before START and after END, and check for a START and END lines.
        self.lines = Extras.strip_whitespace(self.lines) # Clears the whitespace at the start and end of every line ("  NUM a = 5 " -> "NUM a = 5")
        self.lines = Extras.clear_comments(self.lines, Syntax.COMMENT) # Clears all the comments ("PRINT sup # prints stuff" -> "PRINT sup")
        #self.lines = Extras.clear_strings(self.lines, "\n", "\t") # Clears all the unnecessary strings from every line ("\tNUM a = 5\n" -> "NUM a = 5")
        #self.lines = Extras.clear_whitespace(self.lines, "", "\t") # Clears all the empty lines, including tabs ("", "\t")
        
        # Check for START and END declaration errors
        if(Syntax.SCRIPT_START not in self.lines.values()): Error.throw(ErrorType.MISSING_START) # Check if there's a START statement
        if(Syntax.SCRIPT_END not in self.lines.values()): Error.throw(ErrorType.MISSING_END) # Check if there's an END statement
        lineList = self.linelist() # Get all the lines (from dict to list): {1: "line1", 2: "line2"} -> ["line1", "line2"]
        if(lineList.count(Syntax.SCRIPT_START) > 1): Error.throw(ErrorType.MULTIPLE_STARTS, InnerExtras.lastIndexOf(self.lines, Syntax.SCRIPT_START)) # Check for multiple START statements
        if(lineList.count(Syntax.SCRIPT_END) > 1): Error.throw(ErrorType.MULTIPLE_ENDS, InnerExtras.lastIndexOf(self.lines, Syntax.SCRIPT_END)) # Check for multiple END statements
        startIndex = lineList.index(Syntax.SCRIPT_START) # Get the start line index
        endIndex = lineList.index(Syntax.SCRIPT_END) # Get the end line index
        if(startIndex >= endIndex): Error.throw(ErrorType.END_BEFORE_START, lineList.index(Syntax.SCRIPT_START)) # Check their order

        # Remove all lines before and after the start and end of the script
        output = Extras.get_lines_between(self.lines, Syntax.SCRIPT_START, Syntax.SCRIPT_END)
        match(output):
            case 0: Error.throw(ErrorType.MISSING_START)
            case 1: Error.throw(ErrorType.MISSING_END)
            case _: self.lines = output
    
    def __second_sweep(self): # This will check the syntax of every line. Once it's done, it will convert the lines into instructions for the parser to execute
        self.lines = Extras.normalize_execution_times(self.lines) # Normalizes the execution amount ("3 PRINT Hi" -> "3_PRINT Hi", "[a + 2] PRINT Hi" -> "[a+2]_PRINT Hi")

        # These functions remove all unnecessary spaces from every line, following a regex to avoid breaking any strings.
        self.lines, affectedTextLines = Extras.remove_spaces(self.lines, f"{Syntax.VAR_TEXT}\\s*\\S+\\s*{Syntax.VAR_DECLARATION}\\s*") # Check for text variable declarations
        self.lines, affectedPrintLines = Extras.remove_spaces(self.lines, f"{Syntax.PRINT}\\s*") # Check for prints
        self.lines, affectedUpdateLines = Extras.remove_update_spaces(self.lines, f"\\S+\\s*{Syntax.VAR_DECLARATION}\\s*\\S+") # Check for variable assignment
        protectedLines = affectedTextLines + affectedPrintLines + affectedUpdateLines # List of line indices that mustn't be changed when removing all the remaining spaces
        self.lines = Extras.remove_remaining_spaces(self.lines, protectedLines) # Remove the spaces from every line whose index isn't in the list
        #print(f"Text: {affectedTextLines}, Print: {affectedPrintLines}, Update: {affectedUpdateLines}")
        
        self.lines = dict(sorted(self.lines.items())) # Sort the lines by line number (key)
        self.instructions = Extras.convert_to_instructions(self.lines) # Convert the lines to instructions. It sends every line to the SyntaxChecker and returns a list.
        print("\n".join([str(x) for x in self.instructions]))
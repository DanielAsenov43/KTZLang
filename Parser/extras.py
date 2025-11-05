from syntax import Syntax, InnerSyntax, SyntaxChecker
from errors import Error, ErrorType
import re

class Extras:
    # Returns every single command between 2 specified lines, used mostly to get the code between START and END, FUNC and ENDFUNC, etc.
    # Returns 0 if the start string is missing, 1 if the end string is missing and the lines if everything went right 
    def get_lines_between(lines: dict, beginString: str, endString: str) -> any:
        if(beginString not in lines.values()): return 0 # If the beginString isn't in the lines, return 0
        if(endString not in lines.values()): return 1 # If the endString isn't in the lines, return 1
        started = False
        newLines = {}
        for lineNumber, command in lines.items():
            if(command == beginString): started = True
            if(not started): continue
            if(command == endString): return newLines
            if (command != beginString): newLines[lineNumber] = command
    
    def get_string_between(command: str, beginChar: str, endChar: str) -> str: # Returns the string between 2 characters (first and last char)
        return endChar.join(beginChar.join(command.split(beginChar)[1:]).split(endChar)[:-1])

    def clear_strings(lines: dict, *strings: str) -> dict: # Clears some strings from EVERY LINE
        return {lineNumber:[command.replace(string, "") for string in strings][0] for lineNumber, command in lines.items()}

    def strip_whitespace(lines: dict) -> dict: # Removes whitespace from the left and right side of every command
        return {lineNumber:command.strip() for lineNumber, command in lines.items()}
    
    def clear_whitespace(lines: dict, *whitespaceCharacters: str) -> dict: # Removes the LINES that ARE whitespace (depending on the args)
        return {lineNumber:command for lineNumber, command in lines.items() if command not in whitespaceCharacters}
    
    def clear_comments(lines: dict, commentChar: str) -> dict: # Removes all comments from the code, ignoring everything after the comment symbol.
        return {lineNumber:command for lineNumber, command in lines.items() if (len(command) > 0 and command[0] != commentChar)}
    
    # Removes command spaces except when it finds and command (Example: "TXT").
    # If a command is found, it removes all spaces until an exceptionChar is found (Example: "=")
    def remove_spaces(lines: dict, regex: str) -> dict:
        newLines = {}
        affectedLines = []
        for lineNumber, command in lines.items():
            amountIndex = command.find(InnerSyntax.EXECUTION_AMOUNT)
            newLine = command[amountIndex+1:]
            for syntax in list(map(str, Syntax)):
                if(newLine[0:len(syntax)] != syntax): continue
                match = re.findall(regex, newLine)
                if(match):
                    affectedLines.append(lineNumber)
                    valueIndex = len(match[0])
                    command = command[0:amountIndex+1] + match[0].replace(" ", "") + newLine[valueIndex:]
                    break
            newLines[lineNumber] = command
        return newLines, affectedLines
    
    def remove_update_spaces(lines: dict, regex: str) -> dict: # Same as remove_spaces, but for variable updating ("A = 5", "B++2", "C = Hello")
        newLines = {}
        affectedLines = []
        for lineNumber, command in lines.items():
            amountIndex = command.find(InnerSyntax.EXECUTION_AMOUNT)
            newLine = command[amountIndex+1:]
            hasRegularSyntax = False
            for syntax in list(map(str, Syntax)):
                if(newLine[0:len(syntax)] == syntax):
                    hasRegularSyntax = True
                    break
            if(not hasRegularSyntax):
                match = re.findall(regex, newLine)
                if(match):
                    affectedLines.append(lineNumber)
                    valueIndex = len(match[0])
                    command = command[0:amountIndex+1] + match[0].replace(" ", "") + newLine[valueIndex:]
            newLines[lineNumber] = command
        return newLines, affectedLines
    
    def normalize_execution_times(lines: dict) -> dict: # "PRINT Hi" -> "1_PRINT Hi", "5  PRINT Hi" -> "5_PRINT Hi", "A++2" -> "1_A++2"
        newLines = {}
        for lineNumber, line in lines.items():
            if(InnerExtras.isDigit(line.split(" ")[0])): # Case 1: "5 PRINT Hello"
                newLines[lineNumber] = line.split(" ")[0] + InnerSyntax.EXECUTION_AMOUNT + InnerExtras.getStringAfter(line, " ")
                continue
            if(line[0] == "[" and "] " in line): # Case 2: "[a] PRINT Hello"
                newLines[lineNumber] = line.split(" ")[0] + InnerSyntax.EXECUTION_AMOUNT + InnerExtras.getStringAfter(line, "] ")
                continue
            newLines[lineNumber] = "1_" + line # Case 3: "PRINT Hello"
        return newLines
    
    def remove_remaining_spaces(lines: dict, protectedLines: list) -> dict:
        protected = {lineNumber:command for lineNumber, command in lines.items() if lineNumber in protectedLines}
        unprotected = {lineNumber:command.replace(" ", "") for lineNumber, command in lines.items() if lineNumber not in protectedLines}
        return protected | unprotected
    
    def convert_to_instructions(lines: dict) -> list:
        instructions = []
        for lineNumber, command in lines.items():
            instruction = SyntaxChecker.check_line_get_instruction(command, lineNumber)
            instructions.append(instruction)
        return instructions
    # ===========================================================================================



class InnerExtras:
    def lastIndexOf(lines: dict, string: str) -> int: # Gets the last index of an element in a list
        for lineNumber, command in dict(reversed(list(lines.items()))).items():
            if(command == string): return lineNumber
    
    def isDigit(string: str) -> bool:
        try:
            int(string)
            return True
        except: return False
    
    def getStringAfter(originalString: str, regex: str) -> str:
        return regex.join(originalString.split(regex)[1:])
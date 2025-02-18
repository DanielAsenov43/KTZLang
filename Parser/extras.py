from syntax import Syntax, InnerSyntax, SyntaxChecker
import re

class Extras:
    def get_lines_between(lines: dict, beginString: str, endString: str) -> dict:
        if(beginString not in lines.values() or endString not in lines.values()): return None # Just in case
        started = False; ended = False
        newLines = {}
        for lineNumber, line in lines.items():
            if(line == beginString): started = True
            if(not started): return
            if(line == endString): return newLines
            if (line != beginString): newLines[lineNumber] = line
    
    def get_string_between(line: str, beginChar: str, endChar: str) -> str: # Returns the string between 2 characters (first and last char)
        return endChar.join(beginChar.join(line.split(beginChar)[1:]).split(endChar)[:-1])

    def clear_strings(lines: dict, *strings: str) -> dict: # Clears some strings from EVERY LINE
        return {lineNumber:[line.replace(string, "") for string in strings][0] for lineNumber, line in lines.items()}

    def strip_whitespace(lines: dict) -> dict: # Removes whitespace from the left and right side of every line
        return {lineNumber:line.strip() for lineNumber, line in lines.items()}
    
    def clear_whitespace(lines: dict, *whitespaceCharacters: str) -> dict: # Removes the LINES that ARE whitespace (depending on the args)
        return {lineNumber:line for lineNumber, line in lines.items() if line not in whitespaceCharacters}
    
    def clear_comments(lines: dict, commentChar: str) -> dict: # Removes all comments from the code, ignoring everything after the comment symbol.
        newLines = {} # I tried putting everything in one line but it imploded so ye dont do that
        for lineNumber, line in lines.items():
            commentIndex = line.find(Syntax.COMMENT)
            line = line[0:commentIndex] if commentIndex >= 0 else line
            newLines[lineNumber] = line
        return {lineNumber:line for lineNumber, line in newLines.items() if len(line) > 0 if line[0] != commentChar}
    
    def normalize_execution_times(lines: dict) -> dict: # "PRINT Hi" -> "1_PRINT Hi", "5  PRINT Hi" -> "5_PRINT Hi"
        newLines = {}
        excludedSyntax = (Syntax.VAR_DECLARATION, Syntax.VAR_BOOLEAN_TRUE, Syntax.VAR_BOOLEAN_FALSE)
        for lineNumber, line in lines.items():
            newLine = line
            for syntax in list(map(str, Syntax)):
                syntaxIndex = line.find(syntax)
                if(syntaxIndex >= 0 and syntax not in excludedSyntax):
                    amount = line[0:syntaxIndex].replace(" ", "")
                    amount = amount if len(amount) > 0 else "1"
                    newLine = amount + InnerSyntax.EXECUTION_AMOUNT + line[syntaxIndex:]
                newLines[lineNumber] = newLine
        return newLines

    # Removes line spaces except when it finds and command (Example: "TXT").
    # If a command is found, it removes all spaces until an exceptionChar is found (Example: "=")
    def remove_spaces(lines: dict, regex: str) -> dict:
        newLines = {}
        affectedLines = []
        for lineNumber, line in lines.items():
            amountIndex = line.find(InnerSyntax.EXECUTION_AMOUNT)
            newLine = line[amountIndex+1:]
            for syntax in list(map(str, Syntax)):
                if(newLine[0:len(syntax)] != syntax): continue
                match = re.findall(regex, newLine)
                if(match):
                    affectedLines.append(lineNumber)
                    valueIndex = len(match[0])
                    line = line[0:amountIndex+1] + match[0].replace(" ", "") + newLine[valueIndex:]
                    break
            newLines[lineNumber] = line
        return newLines, affectedLines
    
    def remove_remaining_spaces(lines: dict, protectedLines: list) -> dict:
        protected = {lineNumber:line for lineNumber, line in lines.items() if lineNumber in protectedLines}
        unprotected = {lineNumber:line.replace(" ", "") for lineNumber, line in lines.items() if lineNumber not in protectedLines}
        return protected | unprotected
    
    def convert_to_instructions(lines: dict) -> dict:
        instructions = []
        for lineNumber, line in lines.items():
            commandIndex = line.find(InnerSyntax.EXECUTION_AMOUNT)
            for syntax in list(map(str, Syntax)):
                if(line[commandIndex + 1:commandIndex + 1 + len(syntax)] == syntax):
                    instruction = SyntaxChecker.check_line_get_instruction(line.replace(syntax, ""), syntax, lineNumber)
                    if(instruction): instructions.append(instruction)
                    break
        return instructions
    # ===========================================================================================

    def lastIndexOf(lines: dict, string: str) -> int: # Gets the last index of an element in a list
        for lineNumber, line in dict(reversed(list(lines.items()))).items():
            if(line == string): return lineNumber
    
    def remove_line_spaces(line: str) -> str:
        return str.replace(" ", "")

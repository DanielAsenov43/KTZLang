from lexer import Lexer
from parser import Parser
from errors import Error, ErrorType
import os

SUFFIX = "ktz"

def main():
    #filename = input("Program name > ").lower()
    filename = "miprograma.ktz"
    
    filename = filename.replace(f".{SUFFIX}", "")
    relativePath = os.path.join(f"{filename}.{SUFFIX}")
    absolutePath = os.path.realpath(relativePath)
    
    lexer = Lexer()
    parser = Parser()

    try:
        with open(absolutePath, "r") as file: lines = file.readlines(); file.close()
    except FileNotFoundError:
        Error.throw(ErrorType.FILE_NOT_FOUND)

    executingMessage = f"\t--- Executing [{filename}.ktz] ---"
    endMessage = "\t    --- Program finished ---"

    print(executingMessage)
    instructions = lexer.analyze(lines)
    parser.execute(instructions)
    print(endMessage)

if(__name__ == "__main__"):
    main()
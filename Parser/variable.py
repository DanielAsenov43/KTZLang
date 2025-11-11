from syntax import Syntax
from errors import Error, ErrorType

class Variable:
    def __init__(self, variableType: Syntax, variableName: str, variableValue: any):
        self.variableType = variableType
        self.variableName = variableName
        self.variableValue = variableValue
    
    def get_type(self) -> str: return self.variableType
    def get_name(self) -> str: return self.variableName
    def get_value(self) -> str: return self.variableValue

    def set_value(self, value: any): self.variableValue = value

    def __repr__(self) -> str:
        return f"Variable({self.variableType} {self.variableName} = \"{self.variableValue}\")"
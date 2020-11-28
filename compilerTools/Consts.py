import enum

# Enum representing all token types. Keywords start from value 100. Operators from value 201
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    STRING = 2
    COLON = 3
    COMA = 4
    IDENTIFIER = 5
    # Keywords.
    VAR = 100
    CREATEIMAGE = 101
    ADDFRAME = 102
    COPYIMAGE = 103
    RESIZEIMAGE = 104
    SAVEIMAGE = 105
    ADDIMAGETOIMAGE = 106
    ADDIMAGETOFRAME = 107
    BEGIN = 108
    END = 109
    MULT = 110
    ABS = 111
    PRINT = 112
    GENERATEFLIP = 113
    ASSIGN = 114
    TERM = 115
    EXPRESSION = 116
    COPYFRAME = 117
    CREATEFRAME = 118
    GETIMAGESIZE = 119
    LOOP = 120
    # OPERATOR
    PLUS = 201


from compilerTools.Token import Token
from compilerTools.Consts import TokenType
import sys

class Lexer(object):

    def __init__(self, code):
        self.code = code + '\n' # Saves the source code. Append a newline in the end for easier parsing
        self.curPos = -1
        self.curChar = ''
        self.lastBegin = 0 # TODO: use to implement loop
        self.currLineNo = 1
        self.nextChar()

    def incLineNo(self):
        self.currLineNo +=1

    def getLineNo(self):
        return self.currLineNo

    """
        Method to resent cursor of lexer to last encountered Begin
        Incomplete
    """
    def resetBegin(self):
        self.curPos = self.lastBegin
        if self.curPos >= len(self.code):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.code[self.curPos]

    """
        Method to move the cursor to next character.
    """
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.code):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.code[self.curPos]

    """
        Method returns the next character without incrementing cursor. Used to perform checks.
    """
    def peek(self):
        if self.curPos + 1 >= len(self.code):
            return '\0'
        return self.code[self.curPos + 1]

    """
        Core method to get (next) token. Skips whitespaces till it gets a valid character. Moves cursor to first
        character after token. 
    """
    def getToken(self):
        self.skipWhitespace()
        token = None
        if self.curChar == ':':
            token = Token(TokenType.COLON, self.curChar)
        elif self.curChar == ',':
            token = Token(TokenType.COMA, self.curChar)
        elif self.curChar == '\n':
            token = Token( TokenType.NEWLINE, self.curChar)
        elif self.curChar == '\0':
            token = Token( TokenType.EOF, '')
        elif self.curChar == '+':
            token = Token(TokenType.PLUS, self.curChar)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == ".":
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Incorrent number formation")

                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.code[startPos: self.curPos + 1]
            token = Token(TokenType.NUMBER, tokText)

        elif self.curChar.isalpha():
            start = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            word = self.code[start : self.curPos + 1]
            # print(word)
            if self.isKeyword(word):
                token = Token(self.getKeyword(word), word)
                if token.kind == TokenType.BEGIN:
                    self.lastBegin = start
            else:
                token = Token(TokenType.IDENTIFIER, word)
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '%':
                    # or self.curChar == '>' or self.curChar == '<' or self.curChar == '*' \
                    #         or self.curChar == '?' or self.curChar == '|'
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.code[startPos: self.curPos]
            token = Token(TokenType.STRING, tokText)
        else:
            # print("Unknown Token ", self.curChar)
            self.abort("Unknown Token " + self.curChar)
            pass

        self.nextChar()
        return token

    """
        Utility Method to check if given word is a keyword. Keywords are identified by their value (>= 100)
    """
    def isKeyword(self, word):
        word = word.upper()
        for kind in TokenType:
            if kind.name == word and kind.value >= 100:
                return True
        return False

    """
        Utility method to fetch the keyword specified by given word. Used with checkKeyword
    """
    def getKeyword(self, word):
        word = word.upper()
        if not self.isKeyword(word):
            return None
        else:
            for kind in TokenType:
                if kind.name == word and kind.value >= 100:
                    return kind
        return None

    """
        Skips spaces, tabs and carraige returns.
    """
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    """
        Method to terminate execution and idsplay error message.
    """
    def abort(self, message):
        sys.exit("Lexer Error : "+ message + " at " +str(self.getLineNo()))



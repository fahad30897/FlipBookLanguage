import sys
from compilerTools.Lexer import Lexer
from compilerTools.Token import Token
from compilerTools.Consts import TokenType


class Parser(object):
    def __init__(self, lexer, executor):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.executor = executor
        self.nextToken()
        self.nextToken()

    """
        Compares current token type with given token type
    """
    def checkToken(self, kind):
        return kind == self.curToken.kind

    """
        Compares next tokens type with given token type
    """
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    """
        Compares current tokens type with given token type and moves to next token if matches. If the given type
        doesn't match it ends the program with error. Returns the current token.
    """
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        rval = self.curToken
        self.nextToken()
        return rval

    """
        Updates current token to next token and next token (peekToken) to the next to next token.
    """
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # print("lexer gave " + self.peekToken.text)

    """
       Method to skip arbitary number of newlines. 
    """
    def newline(self):
        self.match(TokenType.NEWLINE)
        self.lexer.incLineNo()
        self.executor.setLineNo(self.lexer.getLineNo())
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
            self.lexer.incLineNo()
            self.executor.setLineNo(self.lexer.getLineNo())

    """
        Parse a block from begin to end or EOF.
    """
    def begin(self):
        self.match(TokenType.BEGIN)
        self.match(TokenType.COLON)
        self.newline()
        while not self.checkToken(TokenType.END) and not self.checkToken(TokenType.EOF):
            self.command()
        if self.checkToken(TokenType.END):
            self.nextToken()
            self.match(TokenType.COLON)

        # if self.checkToken(TokenType.NEWLINE):
        #     self.newline()

    """
        Parse a TERM. return text of the term parsed. In case of string or number literal it would be the value string/number.
        In case of identifier it would be the name of the identifier.
    """
    def term(self):
        rval = None
        if self.checkToken(TokenType.STRING):
            # rval = self.curToken.text
            rval = self.match(TokenType.STRING).text
        elif self.checkToken(TokenType.NUMBER):
            # rval = float(self.curToken.text)
            rval = float(self.match(TokenType.NUMBER).text)
        else:

            ident = self.match(TokenType.IDENTIFIER).text
            if self.executor.checkIfPrimitive(ident):
                rval = self.executor.getPrimitiveValue(ident)
            else:
                self.abort("Only primitive types can be used in expressions")
        return rval


    """
        Parses a expression. 
    """
    def expression(self):

        rval = self.term()

        while self.checkToken(TokenType.PLUS):
            self.nextToken()
            tmpVal = self.term()
            if isinstance(rval, str) or isinstance(tmpVal,str):
                rval = str(rval) + str(tmpVal)
            else:
                rval = float(rval) + float(tmpVal)
        return rval

    """
        Parses all commands and their arguments. Also executes the commands by calling respective executor methods.
    """
    def command(self):

        if self.checkToken(TokenType.PRINT):
            # print("PRINT")
            self.nextToken()
            self.match(TokenType.COLON)
            expVal = self.expression()
            self.executor.printStatement(expVal)
        elif self.checkToken(TokenType.ASSIGN):
            # print("ASSIGN")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            value = self.expression()
            self.executor.assignIdentifier(identifier,value)
        elif self.checkToken(TokenType.VAR):
            # print("Variable declaration")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.executor.declareVariable(identifier)
        elif self.checkToken(TokenType.CREATEIMAGE):
            # print("Create image")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            path = str(self.curToken.text)
            self.match(TokenType.STRING)
            self.executor.createImage(identifier, path)
        elif self.checkToken(TokenType.RESIZEIMAGE):
            # print("resize image")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            type = None
            if self.checkToken(TokenType.MULT):
                type = self.curToken.text
                self.match(TokenType.MULT)
            else:
                type = self.curToken.text
                self.match(TokenType.ABS)

            # print(type)
            self.match(TokenType.COMA)
            width = self.expression()
            self.match(TokenType.COMA)
            height = self.expression()
            self.executor.resizeImage(identifier,type,width,height)
        elif self.checkToken(TokenType.SAVEIMAGE):
            # print("save image")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            path = self.match(TokenType.STRING).text
            self.executor.saveImage(identifier, path)
        elif self.checkToken(TokenType.ADDFRAME):
            # print("ADD FRAME")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.executor.addFrame(identifier)
        elif self.checkToken(TokenType.COPYFRAME):
            # print("COPY frame")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier1 = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            identifier2 = self.match(TokenType.IDENTIFIER).text
            self.executor.copyFrame(identifier1, identifier2)
        elif self.checkToken(TokenType.CREATEFRAME):
            # print("Create frame")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier = self.match(TokenType.IDENTIFIER).text
            self.executor.createFrame(identifier)
        elif self.checkToken(TokenType.ADDIMAGETOFRAME):
            # print("Add image to frame")
            self.nextToken()
            self.match(TokenType.COLON)
            identifier1 = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            identifier2 = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            x = self.expression()
            self.match(TokenType.COMA)
            y = self.expression()
            self.executor.addImageToFrame(identifier1,identifier2,x,y)
        elif self.checkToken(TokenType.GENERATEFLIP):
            # print("genereate")
            self.nextToken()
            self.match(TokenType.COLON)
            self.executor.genereateFlip()
        elif self.checkToken(TokenType.GETIMAGESIZE):
            self.nextToken()
            self.match(TokenType.COLON)
            image = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            x = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            y = self.match(TokenType.IDENTIFIER).text
            self.executor.getImageSize(image, x, y)
        elif self.checkToken(TokenType.LOOP):
            self.nextToken()
            self.match(TokenType.COLON)
            loopVar = self.match(TokenType.IDENTIFIER).text
            self.match(TokenType.COMA)
            start = int(self.expression())
            self.match(TokenType.COMA)
            end = int(self.expression())
            beginPos = self.lexer.curPos
            self.match(TokenType.COLON)

            self.newline()
            self.executor.startLoop(loopVar, start, end)
            for i in range(int(start),int(end)):
                self.begin()
                if i != end - 1:
                    self.lexer.curPos = beginPos

                    self.nextToken()
                    self.nextToken()
                    self.nextToken()
                    if self.checkToken(TokenType.NEWLINE):
                        self.newline()
                self.executor.incLoop(loopVar)



            self.executor.endLoop()
        else:
            self.abort("Invalid command")
        if self.checkToken(TokenType.NEWLINE):
            self.newline()

    def abort(self, message):
        sys.exit("Parser Error. " + message + " at " + str(self.lexer.getLineNo()))
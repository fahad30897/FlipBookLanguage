from compilerTools.Lexer import Lexer
from compilerTools.Parser import Parser
from compilerTools.Consts import TokenType
from compilerTools.Token import Token
from Execution.Executor import Executor
from Execution.State import State
from ImageTools.ImageProcessor import ImageProcessor
import sys

# Utility method to extract and initialize args from command line.
def parseArgs(args):
    outputFileFound = False
    argDict = {}
    argDict["inputFile"] = str(args[0])
    argDict["outputFile"] = ""
    argDict["outputType"] = "pdf"
    argDict["loop"] = 0
    argDict["resolution"] = 100
    argDict["duration"] = 400

    i = 1
    while i < len(args):
        opt = args[i]
        val = args[i+1]
        if opt == "-o":
            argDict["outputFile"] = str(val)
        elif opt == "-l":
            argDict["loop"] = 1 - int(val)
        elif opt == "-r":
            argDict["resolution"] = int(val)
        elif opt == "-t":
            argDict["outputType"] = str(val).upper()
        elif opt == "-d":
            argDict["duration"] = int(val)
        else:
            printUsage()

        i+=2
    return argDict

# Utility Method to print Usage
def printUsage():
    print("Invalid args")
    print("Usage python main.py <input-file> -o <output-file> [-d <int>] [-r <int>] [-l <int>] [-t (\"pdf\", \"gif\")]")
    print("Options:")
    print("-o output file")
    print("-t pdf/gif format (default pdf)")
    print("-d duration between frames in gif (default 400)")
    print("-l looping enabled in gif , 0 for disable, 1 for enabled, (default enabled)")
    print("-r resolution in pdf (default 100)")


def main():
    if len(sys.argv) < 4:
        printUsage()
        sys.exit()
    argDict = parseArgs(sys.argv[1:])
    if argDict["outputFile"] == "":
        print("Output file is required")
        printUsage()
        sys.exit()
    with open(argDict["inputFile"], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    state = State(argDict["outputFile"], argDict["outputType"], argDict["resolution"], argDict["duration"],argDict["loop"])
    imageProcessor = ImageProcessor()
    executor = Executor(state, imageProcessor)
    parser = Parser(lexer, executor)
    parser.begin()

main()
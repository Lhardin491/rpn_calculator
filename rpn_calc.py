#!/usr/bin/env python
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", action="store_true", help="specifies input is a filename to read from")
parser.add_argument("-n", "--notation", type=str, choices=["rpn", "infix"], help="specifies the input notation, default is rpn")
parser.add_argument("input", type=str, help="input equation, must be separated by spaces")

# list of operators
# added modulus division and exponents
ops = {"+": (lambda x,y: x+y),
       "-": (lambda x,y: x-y),
       "*": (lambda x,y: x*y),
       "/": (lambda x,y: x/y),
       "%": (lambda x,y: x%y),
       "^": (lambda x,y: x**y)}

def isNum(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

# function to covert infix to postfix notation
def convertRPN(expression):
    # sets up an output stack and an operators stack
    # iterates through each token adding each to appropriate stack
    expression = expression.split(' ')
    out_q = []
    ops_s = []
    for token in expression:
        if isNum(token):
            out_q.append(token)
        if token in ops:
            ops_s.append(token)
        if token is '(':
            ops_s.append(token)
        # when a closing parenthesis is found
        # adds the operators on the ops stack to the output stack
        # until an open parenthesis is found
        if token is ')':
            while ops_s[len(ops_s)-1] is not '(':
                out_q.append(ops_s.pop())
            if ops_s[len(ops_s)-1] is '(':
                ops_s.pop()
    # add remaining operators to the output stack
    while ops_s:
        out_q.append(ops_s.pop())
    return ' '.join(out_q)


# function to evaluate the RPN equation
def evalRPN(RPN):
    # iterates through each symbol and adds it to stack
    # if the token is an operator it performs the operation
    # and adds the result to the stack
    RPN = RPN.split(' ')
    stack = []
    for token in RPN:
        if token in ops:
            operand1 = stack.pop()
            operand2 = stack.pop()
            # performs the operation on the found operands
            # using the lambda function of the specified token
            result = ops[token](int(operand2), int(operand1))
            stack.append(result)
        else:
            stack.append(token)
    return stack.pop()



if __name__ == "__main__":
    # evaluates each line of the input file
    args = parser.parse_args()
    if args.filename:
        with open(args.input, "r") as file:
            data = file.readlines()
        for line in data:
            line = line.replace('\n', '')
            if args.notation == "infix":
                print("Equation: %s" % line)
                rpn = convertRPN(line)
            else:
                rpn = line
            print("RPN: %s" % rpn)
            result = evalRPN(rpn)
            print("Result: %s\n" % result)
    else:
        line = args.input
        line = line.replace('\n', '')
        if args.notation == "infix":
            print("Equation: %s" % line)
            rpn = convertRPN(line)
        else:
            rpn = line
        print("RPN: %s" % rpn)
        result = evalRPN(rpn)
        print("Result: %s\n" % result)


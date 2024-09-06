from collections import deque

class SyntaxAnalyzer:
    def __init__(self):
        # parsing table derived from problem 0
        self.parsing_table = [[ 'S3',    0,    0,    0,    0,     0, 1, 2],
                              [    0, 'S4', 'S5',    0,    0, 'ACC', 0, 0], 
                              [    0, 'R3', 'R3', 'S6', 'S7',  'R3', 0, 0],
                              [    0, 'R6', 'R6', 'R6', 'R6',  'R6', 0, 0],
                              [ 'S3',    0,    0,    0,    0,     0, 0, 8],
                              [ 'S3',    0,    0,    0,    0,     0, 0, 9],
                              ['S10',    0,    0,    0,    0,     0, 0, 0],
                              ['S11',    0,    0,    0,    0,     0, 0, 0],
                              [ 'S3', 'R1', 'R1', 'S6', 'S7',  'R1', 0, 0],
                              [ 'S3', 'R2', 'R2', 'S6', 'S7',  'R2', 0, 0],
                              [    0, 'R4', 'R4', 'R4', 'R4',  'R4', 0, 0],
                              [    0, 'R5', 'R5', 'R5', 'R5',  'R5', 0, 0]] 

    # lexer method to return lexemes and tokens
    def lexer(self, expr):
        idx = 0
        number = ''
        lexemes = []
        tokens = []
        while idx < len(expr):
            character = expr[idx]
            # if character is number, keep appending before non-number character appears.
            if '0' <= character <= '9':
                number += character
            else:
                try:
                    lexemes.append(int(number))
                    tokens.append('N')
                    number = ''
                    lexemes.append(character)
                    tokens.append(character)
                except:
                    print("Input expression cannot be made using the rules!")
                    exit()

            # in the case of last character
            if idx == len(expr) - 1 and number != '':
                lexemes.append(int(number))
                tokens.append('N')
            
            idx += 1
        # append '$' end token
        lexemes.append('$')
        tokens.append('$')

        return lexemes, tokens
    
    # method for calculating the result
    def calculate(self, operator_list, operand_list):
        operator = operator_list.pop()
        b = operand_list.pop()
        a = operand_list.pop()
        if operator == '*':
            operand_list.append(a*b)
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero error occured!")
            operand_list.append(a/b)
        elif operator == '+':
            operand_list.append(a+b)
        elif operator == '-':
            operand_list.append(a-b)
        
    # method to return Action or Goto based on parsing table
    
    def shift_reduce_parser(self, input):
        tokens = deque(input[1])
        elements = ['N', '+', '-', '*', '/', '$', 'E', 'T']
        stack = [0]
        print("Tracing Start!!")
        print("+------+------------------+-------------------+------------------+----------------------+")
        print("|      |                STACK                 |       INPUT      |        ACTION        |")
        print("+------+------------------+-------------------+------------------+----------------------+")
        action = 1
        start = 0

        # iterate every input stage and print execution process
        while len(tokens) != 0 and action != 'ACC':
            idx = 0
            for element in elements:
                if tokens[0] == element:
                    break
                idx += 1
            
            # error occurs when the token cannot be described based on the rules.
            if idx == len(elements):
                print(f"Error! Input lexeme : {tokens[0]} is out of rules. This expression cannot be made!")
                exit()

            stack_str = ''
            for value in stack:
                stack_str += f'{value} '
            input_str = ''
            for value in tokens:
                input_str += f'{value}'
            print(f'| ({start:02d}) | {stack_str:<36} | {input_str:>16}', end=" ")
            action = self.parsing_table[stack[-1]][idx]
            action = str(action)

            # Shift action case
            if action[0] == 'S':
                full_action = f'Shift {action[1]}'
                stack.append(tokens.popleft())
                stack.append(int(action[1:]))

            # Reduce action case, based on 6 reduce rules (provided in problem 0)
            elif action[0] == 'R':
                # R1, R2 case
                if action[1] == '1' or action[1] == '2':
                    for _ in range(6):
                        stack.pop()
                    prev_state = stack[-1]
                    reduce = 'E'
                    stack.append(reduce)
                    stack.append(self.parsing_table[prev_state][6])
                # R3 case
                elif action[1] == '3':
                    for _ in range(2):
                        stack.pop()
                    prev_state = stack[-1]
                    reduce = 'E'
                    stack.append(reduce)
                    stack.append(self.parsing_table[prev_state][6])
                # R4, R5 case
                elif action[1] == '4' or action[1] == '5':
                    for _ in range(6):
                        stack.pop()
                    prev_state = stack[-1]
                    reduce = 'T'
                    stack.append(reduce)
                    stack.append(self.parsing_table[prev_state][7])
                # R6 case
                else:
                    for _ in range(2):
                        stack.pop()
                    prev_state = stack[-1]
                    reduce = 'T'
                    stack.append(reduce)
                    stack.append(self.parsing_table[prev_state][7])

                full_action = f'Reduce {action[1]} (Goto[{prev_state}, {reduce}])'

            # Accept case
            elif action == 'ACC':
                full_action = "Accept"
            
            # if the action is not Shift, Reduce, Accept, then error
            else:
                print("Wrong input! This input expression cannot be syntatically anaylzed using BNF rules! Try another expression.")
                exit()
                
            print(f'| {full_action:>21}|')
            start += 1

        # group operands and operator in each list to calculate the result
        lexemes = input[0]
        tokens = input[1]
        operand_list = []
        operator_list = []
        # precedence based on the rule
        precedence = {
            '*': 2,
            '/': 2,
            '+': 1,
            '-': 1
        }

        for idx, token in enumerate(tokens):
            # end case
            if token == '$':
                break
            # if token is number
            if token == 'N':
                operand_list.append(int(lexemes[idx]))
            else:
                #calculate the term based on precedence
                while operator_list and precedence[operator_list[-1]] >= precedence[token]:
                    self.calculate(operator_list, operand_list)
                operator_list.append(token)

        # handle remaining operators
        while(operator_list):
            self.calculate(operator_list, operand_list)

        return operand_list[0]

    # return current token to check, if not finished checking yet
    def current_token(self):
        if self.position < len(self.tokens):
            return self.lexemes[self.position], self.tokens[self.position]
        else:
            None
    
    # if successfully checked the token, check next token
    def change_position(self, expected):
        lexeme, token = self.current_token()
        if token == expected:
            self.position += 1
        else:
            print("Input expression is invalid!")
            exit()

    # E -> TE'
    def expr(self):
        print("Enter E")
        first = self.term()
        value = self.expr_prime(first)
        print("Exit E")
        return value
    
    # E' -> +TE' | -TE' | epsilon
    def expr_prime(self, first):
        print("Enter E'")
        lexeme, token = self.current_token()
        # +TE' case
        if token == '+':
            self.change_position(token)
            second = self.term()
            value = self.expr_prime(first + second)
            print("Exit E'")
            return value
        # -TE' case
        elif token == '-':
            self.change_position(token)
            second = self.term()
            value = self.expr_prime(first - second)
            print("Exit E'")
            return value
        # epsilon case
        else:
            print('Epsilon')
            print("Exit E'")
            return first

    # T -> NT'
    def term(self):
        print("Enter T")
        first = self.factor()
        value = self.term_prime(first)
        print("Exit T")
        return value

    # T' -> *NT' | /NT' | epsilon
    def term_prime(self, first):
        print("Enter T'")
        lexemes, token = self.current_token()
        # *NT' case
        if token == '*':
            self.change_position(token)
            second = self.factor()
            value = self.term_prime(first * second)
            print("Exit T'")
            return value
        # /NT' case
        elif token == '/':
            self.change_position(token)
            second = self.factor()
            if second == 0:
                print("Division by Zero error!")
                exit()
            value = self.term_prime(first / second)
            print("Exit T'")
            return value
        # epsilon case
        else:
            print("Epsilon")
            print("Exit T'")
            return first

    # N case
    def factor(self):
        lexeme, token = self.current_token()
        if token == 'N':
            self.change_position(token)
            return int(lexeme)
        else:
            print("Input expression is invalid!")
            exit()
        

    def recursive_descent_parser(self, input):
        print("=====================================================================")
        print("Start!!")
        self.lexemes = input[0]
        self.tokens = input[1]
        self.position = 0

        result = self.expr()
        # in this case, there are some tokens that cannot be interpreted using BNF rules.
        if self.position < len(self.tokens)-1:
            print("Error! Input expression cannot be made! Try another expression.")
            exit()
        
        return result

    
    
        
S = SyntaxAnalyzer()
lexemes, tokens = S.lexer("100*100-120/12+1")
print("Lexemes:" + str(lexemes))
print("Tokens:" + str(tokens))

result = S.shift_reduce_parser((lexemes, tokens))
print("Result:", result)

result = S.recursive_descent_parser((lexemes, tokens))
print("Result:", result)
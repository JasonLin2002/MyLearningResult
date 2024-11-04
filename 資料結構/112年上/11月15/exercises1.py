def infix_to_postfix(infix_expression):
    def precedence(operator):
        precedence_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        return precedence_dict.get(operator, 0)

    def is_higher_precedence(op1, op2):
        return precedence(op1) >= precedence(op2)

    def infix_to_postfix_internal(infix_exp):
        stack = []
        postfix_exp = []
        operators = set('+-*/')

        for token in infix_exp:
            if token.isalnum():
                postfix_exp.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix_exp.append(stack.pop())
                stack.pop()  # Pop '('
            elif token in operators:
                while stack and stack[-1] in operators and is_higher_precedence(stack[-1], token):
                    postfix_exp.append(stack.pop())
                stack.append(token)

        while stack:
            postfix_exp.append(stack.pop())

        return postfix_exp

    infix_tokens = infix_expression.replace(' ', '').replace('(', ' ( ').replace(')', ' ) ').split()
    postfix_result = infix_to_postfix_internal(infix_tokens)
    return ' '.join(postfix_result)

infix_expr_1 = "3*((7+1)/4)+(17-5)"
infix_expr_2 = "8/2*3+(8-(16*18))"
infix_expr_3 = "5+(8/2)-(8*(20+(2-1)*8))"

postfix_result_1 = infix_to_postfix(infix_expr_1)
postfix_result_2 = infix_to_postfix(infix_expr_2)
postfix_result_3 = infix_to_postfix(infix_expr_3)

print("Infix Expression 1:", infix_expr_1)
print("Postfix Expression 1:", postfix_result_1)

print("\nInfix Expression 2:", infix_expr_2)
print("Postfix Expression 2:", postfix_result_2)

print("\nInfix Expression 3:", infix_expr_3)
print("Postfix Expression 3:", postfix_result_3)

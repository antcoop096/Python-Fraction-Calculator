import re, math

class Fraction: 

    def __init__(self, n, d): self.n, self.d = n, d #constructor

    def com_den(self, d1, d2): #finds common denominator
        orig_1, orig_2 = d1, d2
        while True:
            if d1 == d2: return d1
            if d1 < d2: d1 += orig_1
            else: d2 += orig_2

    def simplify(self, n, d): #simplifies fraction
        if d < 0: #fixes negative sign for division
            n *= -1
            d *= -1 
        
        gcd = math.gcd(n, d) #find greatest common divisor
        n //= gcd
        d //= gcd

        if n == 0: return f'Result: {0}' #checks if the result is 0 or a whole number
        if d == 1: return f'Result: {n}'

        sign, an = '-' if n < 0 else '', abs(n) #displays a mixed number, if necessary
        mixed = '' if an < d else f'\nMixed Number: {sign}{an//d} {an%d}/{d}' 

        return f'Result: {n}/{d}{mixed}' 
                
    def __add__(self, other): #fraction addition
        d = self.com_den(self.d, other.d)
        return self.simplify(self.n * (d // self.d) + other.n * (d // other.d), d)
            
    def __sub__(self, other): #fraction subtraction
        d = self.com_den(self.d, other.d)
        return self.simplify(self.n * (d // self.d) - other.n * (d // other.d), d)

    def __mul__(self, other): return self.simplify(self.n * other.n, self.d * other.d) #fraction multiplication
        
    def __truediv__(self, other): return self.simplify(self.n * other.d, self.d * other.n) #fraction division

pattern = re.compile(r'^-?\d+/-?\d+(\+|\-|\*|//)-?\d+/-?\d+$') #ensures proper input
examples = """
EXAMPLES:
Addition: 1/3+2/5
Subtraction: 4/7-2/7
Multiplication: -5/10*6/7
Division: 15/21//37/49
"""

print(f'\n{"*"*19}\nFRACTION CALCULATOR\n{"*"*19}\n') #user greeting
print("(use '//' for dividing fractions, to see example equations enter 'e', to quit enter 'q')\n")

while True:
    equation, valid = ''.join(input("Enter an equation: ").split()).lower(), False #takes and validates user input
    if equation == 'q': quit('Application closed')
    elif equation == 'e': print(examples)
    else:
        for match in pattern.finditer(equation): valid = True  
        if valid == False:
            print("Something went wrong. Please try again.\n")
            continue

        slash_1, slash_2 = equation.index('/'), len(equation) - equation[::-1].index('/') - 1 #finds operation and indexes of operation symbol and '/'s
        op_ind = slash_1 + 2
        while equation[op_ind].isdecimal(): op_ind += 1
        operator = equation[op_ind] + '/' if equation[op_ind] == '/' else equation[op_ind]

        num_1, den_1 = int(equation[:slash_1]), int(equation[slash_1 + 1:op_ind]) #captures numerators and denominators
        num_2, den_2 = equation[op_ind + 1:slash_2], int(equation[slash_2 + 1:])
        if num_2[0] == '/': num_2 = num_2[1:]
        num_2 = int(num_2)

        if (0 in [den_1, den_2]) or (operator == '//' and num_2 == 0): #checks for division by 0
            print('Cannot divide by zero. Please try again.\n')
            continue

        if (den_1 < 0 and num_1 >= 0) or (den_1 < 0 and num_1 < 0): #fixes negative sign to prevent infinite loop
            num_1 *= -1
            den_1 *= -1
        if (den_2 < 0 and num_2 >= 0) or (den_2 < 0 and num_2 < 0): 
            num_2 *= -1
            den_2 *= -1

        #calculates and displays result
        if operator == '+': print(f'{Fraction(num_1, den_1) + Fraction(num_2, den_2)}\n')
        elif operator == '-': print(f'{Fraction(num_1, den_1) - Fraction(num_2, den_2)}\n')
        elif operator == '*': print(f'{Fraction(num_1, den_1) * Fraction(num_2, den_2)}\n')
        elif operator == '//': print(f'{Fraction(num_1, den_1) / Fraction(num_2, den_2)}\n')
        
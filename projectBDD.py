# COLE LOGAN
# CPTS350 projectBDD
# 4/8/24

from pyeda.inter import *

# STATEMENT A
# for each node u in [prime], there is a node v in [even] such 
# that u can reach v in a positive even number of steps

def RoR(RR):
    # declare boolean variables
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    # replace all occurences of y with z
    banana = RR.compose({y[i]: z[i] for i in range(5)})
    # replace all occurences of x with z
    goodapple = RR.compose({x[i]: z[i] for i in range(5)})

    # combine the two and remove the z boolean variables
    RR2 = (banana & goodapple).smoothing(z)

    return RR2

def Rstar(RR2):
    # declare boolean variables
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    # see transitive closure alg in class notes
    H = RR2
    while (True):
        Hprime = H
        # H := H' v (H' o RR2)
        H = (Hprime | (H.compose({y[i]: z[i] for i in range(5)}) & RR2.compose({x[i]: z[i] for i in range(5)}))).smoothing(z)
        # if H === H'
        if (H.equivalent(Hprime)):
            return H

def statementA():
    # declare boolean variables
    x = bddvars('x', 5)
    y = bddvars('y', 5)

    # CONSTRUCTING EVEN BDD
    # evens = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    beven = ['00000', '00010', '00100', '00110', '01000', '01010', '01100', '01110', 
            '10000', '10010', '10100', '10110', '11000', '11010', '11100', '11110']
    even_exp = ""
    
    # constructing string expression for even nodes
    for i, e in enumerate(beven):
        for j in range(4):
            if e[j] == '0':
                even_exp += "~y[" + str(j) + "] & "
            else: # == '1'
                even_exp += "y[" + str(j) + "] & "
        if i != 15:
            if e[4] == '0':
                even_exp += "~y[" + "4" + "] | "
            else: # == '1'
                even_exp += "y[" + "4" + "] | "
        else: # == 15
            if e[4] == '0':
                even_exp += "~y[" + "4" + "]"
            else: # == '1'
                even_exp += "y[" + "4" + "]"
    # convert string to expression then BDD
    even_exp = expr(even_exp)
    EVEN = expr2bdd(even_exp)


    # CONSTRUCTING PRIME BDD
    # primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    bprime = ['00011', '00101', '00111', '01011', '01101', '10001', '10011', '10111',
            '11101', '11111']
    prime_exp = ""

    # constructing string expression for prime nodes
    for i, e in enumerate(bprime):
        for j in range(4):
            if e[j] == '0':
                prime_exp += "~x[" + str(j) + "] & "
            else: # == '1'
                prime_exp += "x[" + str(j) + "] & "
        if i != 9:
            if e[4] == '0':
                prime_exp += "~x[" + "4" + "] | "
            else: # == '1'
                prime_exp += "x[" + "4" + "] | "
        else: # == 11
            if e[4] == '0':
                prime_exp += "~x[" + "4" + "]"
            else: # == '1'
                prime_exp += "x[" + "4" + "]"
    # convert string to expression then BDD
    prime_exp = expr(prime_exp)
    PRIME = expr2bdd(prime_exp)


    # CONSTRUCTING RR BDD
    # nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
    #         17, 18, 19, 20, 21, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    binary = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', 
            '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111',
            '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111',
            '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111']
    R_exp = ""

    # constructing string expression for edges in G
    for i, e in enumerate(binary):
        for j, f in enumerate(binary):
            if (i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32:
                for m in range(5):
                    if e[m] == '0':
                        R_exp += "~x[" + str(m) + "] & "
                    else: # == '1'
                        R_exp += "x[" + str(m) + "] & "
                for m in range(4):
                    if f[m] == '0':
                        R_exp += "~y[" + str(m) + "] & "
                    else: # == '1'
                        R_exp += "y[" + str(m) + "] & "
                if f[4] == '0':
                    R_exp += "~y[" + "4" + "] | "
                else: # == '1'
                    R_exp += "y[" + "4" + "] | "
    # convert string to expression then BDD
    R_exp = R_exp[:-3] # get rid of " | " at the end of the string
    R_exp = expr(R_exp)
    RR = expr2bdd(R_exp)

    # GIVEN TEST CASES 
    print("\n***GIVEN TEST CASES FOR RR, EVEN, AND PRIME***")
    test1 = RR.restrict({x[0]: 1, x[1]: 1, x[2]: 0, x[3]: 1, x[4]: 1, y[0]: 0, y[1]: 0, y[2]: 0, y[3]: 1, y[4]: 1})
    print(f"RR(27, 3) is {test1.is_one()}")
    test2 = RR.restrict({x[0]: 1, x[1]: 0, x[2]: 0, x[3]: 0, x[4]: 0, y[0]: 1, y[1]: 0, y[2]: 1, y[3]: 0, y[4]: 0})
    print(f"RR(16, 20) is {test2.is_one()}")
    test3 = EVEN.restrict({y[0]: 0, y[1]: 1, y[2]: 1, y[3]: 1, y[4]: 0})
    print(f"EVEN(14) is {test3.is_one()}")
    test4 = EVEN.restrict({y[0]: 0, y[1]: 1, y[2]: 1, y[3]: 0, y[4]: 1})
    print(f"EVEN(13) is {test4.is_one()}")
    test5 = PRIME.restrict({x[0]: 0, x[1]: 0, x[2]: 1, x[3]: 1, x[4]: 1})
    print(f"PRIME(7) is {test5.is_one()}")
    test6 = PRIME.restrict({x[0]: 0, x[1]: 0, x[2]: 0, x[3]: 1, x[4]: 0})
    print(f"PRIME(2) is {test6.is_one()}")

    # R o R (RR2) [compose R]
    RR2 = RoR(RR)

    # GIVEN TEST CASES
    print("\n***GIVEN TEST CASES FOR RR2***")
    test7 = RR2.restrict({x[0]: 1, x[1]: 1, x[2]: 0, x[3]: 1, x[4]: 1, y[0]: 0, y[1]: 0, y[2]: 1, y[3]: 1, y[4]: 0})
    print(f"RR2(27, 6) is {test7.is_one()}")
    test8 = RR2.restrict({x[0]: 1, x[1]: 1, x[2]: 0, x[3]: 1, x[4]: 1, y[0]: 0, y[1]: 1, y[2]: 0, y[3]: 0, y[4]: 1})
    print(f"RR2(27, 9) is {test8.is_one()}")

    # R* (RR2*) [transitive closure of RR2]
    RR2star = Rstar(RR2)

    # STATEMENT A EVALUATION
    print("\nStatement A: for each node u in [prime], there is a node v in [even] such that u can reach v in a positive even number of steps")
    if (~(PRIME.smoothing(x)) | (EVEN.smoothing(y) & RR2star.smoothing(x+y))):
        print("Code evaluation: Statement A is true!\n")
    else:
        print("Code evaluation: Statement A is false.\n")

def main():
    statementA()

if __name__=="__main__":
    main()
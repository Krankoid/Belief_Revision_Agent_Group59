from entails import isEntailed
from sympy import *
from BeliefBaseAgent import *

def checkAGMpostulates():
    # Define the necessary symbols
    p, q, r = symbols('p q r')

    # Define the belief base and weights
    belief_base = {p, q}
    belief_weights = {p: 0.8, q: 0.2}
    
    # Postulate 1: Closure
    formula = r
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 1 (Closure):", bb.belief_base)

    # Postulate 2: Inclusion
    formula = p
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 2 (Inclusion):", bb.belief_base)

    # Postulate 3: Vacuity
    formula = ~p
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 3 (Vacuity):", bb.belief_base)

    # Postulate 4: Success
    formula = q
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 4 (Success):", bb.belief_base)

    # Postulate 5: Uniformity
    formula = p | q
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 5 (Uniformity):", bb.belief_base)

    # Postulate 6: Extensionality
    formula = p
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Postulate 6 (Extensionality):", bb.belief_base)

    # Superexpansion
    formula = r
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Superexpansion:", bb.belief_base)

    # Subexpansion
    formula = ~p
    bb = BeliefBase(belief_base, belief_weights)
    bb.revise(formula, 0.5)
    print("Subexpansion:", bb.belief_base)

# Call the function to check the AGM postulates
checkAGMpostulates()

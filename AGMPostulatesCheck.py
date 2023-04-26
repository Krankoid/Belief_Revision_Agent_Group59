from entails import is_entailed
from sympy import *

class BeliefBase:
    def __init__(self, belief_base=None, belief_weights=None):
        if belief_base is None:
            belief_base = set()
        if belief_weights is None:
            belief_weights = {}
        self.belief_base = belief_base
        self.belief_weights = belief_weights

    def expand(self, formula, weight):
        # Add the new formula to the belief base
        self.belief_base.add(formula)

        # Update the belief weights
        self.belief_weights[formula] = weight

    def contract(self, formula):
        # Compute the remainder sets
        remainder_sets = self._remainder_sets(formula)

        # Return early if remainder_sets is empty
        if not remainder_sets:
            return

        # Apply the selection function
        selected_remainders = self._selection_function(remainder_sets)

        # Contract the belief base
        self.belief_base = set().union(*selected_remainders)


    def revise(self, formula, weight):
        # Contract the belief base with the negation of the formula
        negation = ~formula
        self.contract(negation)
        
        # Add the new formula to the belief base
        self.belief_base.add(formula)

        # Update the belief weights
        self.belief_weights[formula] = weight

    def _remainder_sets(self, formula):
        remainder_sets = []
        for belief in self.belief_base:
            candidate_remainder = self.belief_base - {belief}
            if candidate_remainder and not is_entailed(candidate_remainder, formula):
                remainder_sets.append(candidate_remainder)
        return remainder_sets


    def _selection_function(self, remainder_sets):
        # Weighted selection
        if not remainder_sets:
            return []
        
        weights = []
        for remainder_set in remainder_sets:
            weights.append(sum([self.belief_weights[belief] for belief in remainder_set]))

        max_weight = max(weights)
        selected_remainders = [remainder_set for remainder_set, weight in zip(remainder_sets, weights) if weight == max_weight]

        return selected_remainders

def check_agm_postulates():
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
check_agm_postulates()



#p, q, r = symbols('p q r')

# belief_base = {p, q}
# belief_weights = {p: 0.8, q: 0.5}
# bb = BeliefBase(belief_base, belief_weights)

# new_formula = r
# new_weight = 0.8
# bb.revise(new_formula, new_weight)

# print("Revised belief base:", bb.belief_base)
# print("Updated belief weights:", bb.belief_weights)


    
# def check_agm_postulates():
#     # Define the necessary symbols
#     p, q, r = symbols('p q r')

#     # Define belief weights
#     belief_weights = {p: 0.8, q: 0.8, r: 0.5}

#     # Postulate 1: Closure
#     belief_base = {p, q}
#     formula = r
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 1 (Closure):", bb.belief_base)

#     # Postulate 2: Inclusion
#     belief_base = {p, q}
#     formula = p
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 2 (Inclusion):", bb.belief_base)

#     # Postulate 3: Vacuity
#     belief_base = {p, q}
#     formula = ~p
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 3 (Vacuity):", bb.belief_base)

#     # Postulate 4: Success
#     belief_base = {p, q}
#     formula = q
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 4 (Success):", bb.belief_base)

#     # Postulate 5: Uniformity
#     belief_base = {p, q}
#     formula = p | q
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 5 (Uniformity):", bb.belief_base)

#     # Postulate 6: Extensionality
#     belief_base = {p, q, r}
#     formula = p
#     bb = BeliefBase(belief_base, belief_weights)
#     bb.contract(formula)
#     print("Postulate 6 (Extensionality):", bb.belief_base)

# # Call the function to check the AGM postulates
# check_agm_postulates()


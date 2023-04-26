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

if __name__ == "__main__":
    bb = BeliefBase()
    # Add beliefs, revise and test AGM postulates
    # Add a simple user input
    while True:
        print("1. Expand KB")
        print("2. Remove belief")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            new_formula = input("Enter the formula: ")
            new_weight = input("Enter formula's weight (0 to 1): ")

            if not bb.belief_base:
                bb.expand(sympify(new_formula), float(new_weight))
            else:
                bb.revise(sympify(new_formula), float(new_weight))

        elif choice == "2":
            formula = input("Enter the formula: ")
            bb.contract(sympify(formula))
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

        print("Current belief base:", bb.belief_base, bb.belief_weights)   

#p, q, r = symbols('p q r')

# belief_base = {p, q}
# belief_weights = {p: 0.8, q: 0.5}
# bb = BeliefBase(belief_base, belief_weights)

# new_formula = r
# new_weight = 0.8
# bb.revise(new_formula, new_weight)

# print("Revised belief base:", bb.belief_base)
# print("Updated belief weights:", bb.belief_weights)



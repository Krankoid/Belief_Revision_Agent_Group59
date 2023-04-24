from sympy.logic import to_cnf
from sympy import *
class BeliefRevision:
    def __init__(self, belief_set):
        self.belief_set = belief_set

    def negate_formula(self, formula):
        return ~formula

    def is_entailed(self, formula):
        cnf_belief_set = [to_cnf(belief) for belief in self.belief_set]
        cnf_negated_formula = to_cnf(self.negate_formula(formula))

        return self.resolution(cnf_belief_set, cnf_negated_formula)

    def resolution(self, cnf_belief_set, cnf_negated_formula):
        # Add the negation of the formula to the belief set
        extended_belief_set = cnf_belief_set + [cnf_negated_formula]

        # Resolution algorithm
        while True:
            new_resolvents = set()

            for i, a in enumerate(extended_belief_set):
                for b in extended_belief_set[i+1:]:
                    resolvents = self.resolve(a, b)
                    if resolvents is None:
                        continue

                    # Empty clause found, return True (entailed)
                    if resolvents == set():
                        return True

                    new_resolvents |= resolvents

            if new_resolvents.issubset(extended_belief_set):
                return False

            extended_belief_set += list(new_resolvents)

    def resolve(self, a, b):
        for literal_a in a.args:
            for literal_b in b.args:
                if literal_a == ~literal_b:
                    new_clause = a.subs({literal_a: None}) | b.subs({literal_b: None})
                    return {new_clause}

        return None
    
# Define your symbols (propositional variables)
A, B, C = symbols('A B C')

# Define your belief set
belief_set = {A & B, B >> C}

# Create an instance of the BeliefRevision class with your belief set
br = BeliefRevision(belief_set)

# Define the formula you want to check for entailment
formula = A

br

# Check if the formula is entailed by the belief set
entailment_result = br.is_entailed(formula)

print(entailment_result)
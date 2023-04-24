from sympy.logic import to_cnf
from sympy import *


class BeliefRevision:
    def __init__(self, belief_set):
        self.belief_set = {to_cnf(belief) for belief in belief_set}

    def _resolve(self, clause1, clause2):
        """
        This function takes two clauses and returns a new clause by applying the resolution rule.
        """
        resolved = False
        new_clause = set(clause1.args).union(set(clause2.args))
        for literal1 in clause1.args:
            for literal2 in clause2.args:
                if literal1 == Not(literal2) or Not(literal1) == literal2:
                    new_clause.discard(literal1)
                    new_clause.discard(literal2)
                    resolved = True
        return Or(*new_clause) if resolved and new_clause else None

    def _apply_resolution(self, clauses):
        """
        This function applies the resolution rule to all pairs of clauses in the given set.
        """
        new_clauses = set()
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    resolvent = self._resolve(clause1, clause2)
                    print(resolvent)
                    if resolvent is not None:
                        new_clauses.add(resolvent)
        return new_clauses

    def is_entailed(self, formula):
        """
        This function checks if the given formula is entailed by the belief set using the resolution method.
        """
        neg_formula = Not(formula)
        cnf_formula = to_cnf(neg_formula)
        clauses = self.belief_set.copy()
        clauses.add(cnf_formula)

        while True:
            new_clauses = self._apply_resolution(clauses)
            if len(new_clauses) == 0:
                return False
            if any(clause == False or clause == S.false for clause in new_clauses):
                return True
            if new_clauses.issubset(clauses):
                return False
            clauses |= new_clauses

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

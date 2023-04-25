import itertools
from sympy import symbols
from sympy.logic import to_cnf, Not, Or, And, simplify_logic

class BeliefRevision:

    def __init__(self, belief_set):
        self.belief_set = belief_set

    def is_entailed(self, formula):
        return self.resolution(to_cnf(formula))

    def resolution(self, formula):
        clauses = set()
        for belief in self.belief_set:
            clauses.update(self._cnf_to_clauses(to_cnf(belief)))

        negated_formula = to_cnf(Not(formula))
        clauses.update(self._cnf_to_clauses(negated_formula))

        while True:
            new_clauses = set()
            for c1, c2 in itertools.product(clauses, repeat=2):
                resolvents = self._resolve(c1, c2)
                if set() in resolvents:
                    return True
                new_clauses.update(resolvents)

            if new_clauses.issubset(clauses):
                return False

            clauses.update(new_clauses)

    def _cnf_to_clauses(self, cnf):
        if isinstance(cnf, And):
            clauses = set()
            for arg in cnf.args:
                if isinstance(arg, Or):
                    clauses.add(frozenset(arg.args))
                else:
                    clauses.add(frozenset((arg,)))
            return clauses
        elif isinstance(cnf, Or):
            return {frozenset(cnf.args)}
        else:
            return {frozenset((cnf,))}


    def _resolve(self, c1, c2):
        resolvents = set()
        for lit1 in c1:
            for lit2 in c2:
                if lit1 == ~lit2:
                    resolvent = (c1 - {lit1}) | (c2 - {lit2})
                    resolvents.add(frozenset(resolvent))
        return resolvents
    
def test_belief_revision():
    A, B, C, D = symbols('A B C D')

    belief_set = {A & B, B >> C}
    br = BeliefRevision(belief_set)

    # Test 1: Entailment
    assert br.is_entailed(A) == True

    # Test 2: Non-entailment
    assert br.is_entailed(D) == False

    # Test 3: Entailment with more complex formula
    belief_set_2 = {A | B, ~B}
    br2 = BeliefRevision(belief_set_2)
    assert br2.is_entailed(A) == True

    # Test 4: Non-entailment with more complex formula
    belief_set_3 = {A & B, B & ~C}
    br3 = BeliefRevision(belief_set_3)
    assert br3.is_entailed(A & C) == False

    print("All tests passed!")

test_belief_revision()




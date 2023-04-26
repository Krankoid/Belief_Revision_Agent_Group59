import itertools
from sympy import *
from sympy import symbols
from sympy.logic import to_cnf, Not, Or, And, simplify_logic

class BeliefRevision:


    def __init__(self, belief_set, belief_values=None):
        self.belief_set = belief_set
        if belief_values is None:
            self.belief_values = {belief: 1.0 for belief in belief_set}
        else:
            self.belief_values = belief_values

    def add_belief(self, belief, value):
        self.belief_set.add(belief)
        self.belief_values[belief] = value

    def remove_belief(self, belief):
        self.belief_set.remove(belief)
        del self.belief_values[belief]

    def update_belief_value(self, belief, value):
        self.belief_values[belief] = value

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
    belief_values = {(A & B): 0.9, (B >> C): 0.7}
    br = BeliefRevision(belief_set, belief_values)

    # Test 1: Entailment
    assert br.is_entailed(A) == True

    # Test 2: Non-entailment
    assert br.is_entailed(D) == False

    # Test 3: Entailment with more complex formula
    belief_set_2 = {A | B, ~B}
    belief_values_2 = {(A | B): 0.8, (~B): 0.6}
    br2 = BeliefRevision(belief_set_2, belief_values_2)
    assert br2.is_entailed(A) == True

    # Test 4: Non-entailment with more complex formula
    belief_set_3 = {A & B, B & ~C, A}
    belief_values_3 = {(A & B): 0.5, (B & ~C): 0.5, (A): 0.5}
    br3 = BeliefRevision(belief_set_3, belief_values_3)
    assert br3.is_entailed(A & C) == False

    # Test 5: Add belief
    br.add_belief(A | ~C, 0.7)
    assert (A | ~C) in br.belief_set
    assert br.belief_values[A | ~C] == 0.7

    # Test 6: Remove belief
    br.remove_belief(A & B)
    assert (A & B) not in br.belief_set
    assert (A & B) not in br.belief_values

    # Test 7: Update belief value
    br.update_belief_value(B >> C, 0.9)
    assert br.belief_values[B >> C] == 0.9

    print("All tests passed!")

test_belief_revision()

def main():
    belief_set = set()
    belief_values = {}
    br = BeliefRevision(belief_set, belief_values)

    while True:
        print("\nOptions:")
        print("1. Add a formula and a value to the belief set")
        print("2. Remove a formula from the belief set")
        print("3. Print the belief set")
        print("4. Check for entailment in the belief set")
        print("5. Quit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            formula_str = input("Enter the formula: ")
            value = float(input("Enter the value (0 to 1): "))

            try:
                formula = simplify_logic(sympify(formula_str))
                br.add_belief(formula, value)
                print(f"Added {formula} with value {value} to the belief set")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            formula_str = input("Enter the formula to remove: ")

            try:
                formula = simplify_logic(sympify(formula_str))
                br.remove_belief(formula)
                print(f"Removed {formula} from the belief set")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            print("Belief Set:")
            for belief, value in br.belief_values.items():
                print(f"{belief}: {value}")

        elif choice == '4':
            formula_str = input("Enter the formula to check for entailment: ")

            try:
                formula = simplify_logic(sympify(formula_str))
                result = br.is_entailed(formula)
                print(f"Entailment: {result}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()



from sympy import *

class BeliefRevisionAgent:

    def __init__(self):
        self.belief_base = set()
        self.belief_order = []
        self.add_belief(sympify("x"))

    def add_belief(self, formula):
        # Check if the formula is already in the belief base
        if formula not in self.belief_base:
            # Add the formula to the belief base
            self.belief_base.add(formula)
            self.belief_order.append(formula)
    
    def remove_belief(self, formula):
        # Check if the formula is in the belief base
        if formula in self.belief_base:
            # Implement the partial meet contraction
            contracted_belief_base = self._partial_meet_contraction(formula)
            self.belief_base = contracted_belief_base
    
    # first remove inconsistency with the incoming information, and then add the new information 
    def revise_belief(self, formula):
        # If the belief is already entailed by the belief base, no revision is needed
        if self.is_entailed(formula):
            print("Is entailed")
            return

        # Contract the belief base with the negation of the new belief
        negated_formula = Not(formula)
        contracted_belief_base = self._partial_meet_contraction(negated_formula)

        # Expand the contracted belief base with the new belief
        contracted_belief_base.add(formula)
        self.belief_base = contracted_belief_base

    def is_entailed(self, formula):
        # Convert the belief base to CNF
        belief_base_cnf = set()
        for belief in self.belief_base:
            belief_base_cnf.add(to_cnf(belief))

        # Convert the negation of the given formula to CNF
        negated_formula_cnf = to_cnf(Not(formula))

        # Combine the CNF forms
        combined_cnf = belief_base_cnf | {negated_formula_cnf}

        # Convert the CNF expressions into a suitable data structure for the resolution algorithm
        cnf_clauses = self._convert_cnf_to_clauses(combined_cnf)

        # Apply the resolution algorithm to check for unsatisfiability
        is_unsatisfiable = self._resolution(cnf_clauses)

        # If the combined CNF is unsatisfiable, the original formula is entailed by the belief base
        return is_unsatisfiable
    
    def _convert_cnf_to_clauses(self, cnf_formulas):
        clauses = set()
        for formula in cnf_formulas:
            if isinstance(formula, And):
                for clause in formula.args:
                    clauses.add(frozenset(self._get_literals_from_clause(clause)))
            elif isinstance(formula, Or) or isinstance(formula, Not) or isinstance(formula, Symbol):
                clauses.add(frozenset(self._get_literals_from_clause(formula)))
        return clauses

    def _get_literals_from_clause(self, clause):
        if isinstance(clause, Or):
            return clause.args
        else:
            return (clause,)
    
    def _resolution(self, clauses):
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    resolvents = self._resolve(clause1, clause2)
                    if resolvents is None:
                        return False  # Unsatisfiable
                    elif resolvents:
                        new_clauses.add(resolvents)

            if new_clauses.issubset(clauses):
                return True  # Satisfiable

            clauses = clauses.union(new_clauses)

    def _resolve(self, clause1, clause2):
        complementary_literals = set()
        for literal1 in clause1:
            for literal2 in clause2:
                if self._is_complementary(literal1, literal2):
                    complementary_literals.add((literal1, literal2))

        if len(complementary_literals) != 1:
            return None

        literal1, literal2 = complementary_literals.pop()
        resolvent = (clause1 - {literal1}) | (clause2 - {literal2})
        return frozenset(resolvent)

    def _is_complementary(self, literal1, literal2):
        if isinstance(literal1, Not) and literal1.args[0] == literal2:
            return True
        if isinstance(literal2, Not) and literal2.args[0] == literal1:
            return True
        return False

    def _partial_meet_contraction(self, formula):
        # If the belief is not entailed by the belief base, return the original belief base
        if not self.is_entailed(formula):
            return self.belief_base
        
        # Find all the minimal subsets of the belief base that do not include the formula
        minimal_subsets = self._find_minimal_subsets_without_formula(formula)

        # Apply a selection function to choose a subset or subsets
        selected_subsets = self._selection_function(minimal_subsets)

        # Combine the selected subsets into a new belief base
        contracted_belief_base = set().union(*selected_subsets)

        return contracted_belief_base
    
    # for partial meet contraction
    def _find_minimal_subsets_without_formula(self, formula):
        # Generate all possible subsets of the belief base without the formula
        all_subsets = self._generate_subsets(self.belief_base - {formula})

        # Filter out non-minimal subsets
        minimal_subsets = self._filter_minimal_subsets(all_subsets)

        return minimal_subsets

    def _generate_subsets(self, belief_set):
        if not belief_set:
            return [set()]

        element = belief_set.pop()
        subsets_without_element = self._generate_subsets(belief_set)

        subsets_with_element = [subset | {element} for subset in subsets_without_element]
        return subsets_with_element + subsets_without_element
    
    def _filter_minimal_subsets(self, subsets):
        minimal_subsets = []

        for subset in subsets:
            if not any(other.issubset(subset) for other in subsets if other != subset):
                minimal_subsets.append(subset)

        return minimal_subsets
    
    def _selection_function(self, minimal_subsets):
        # Assign a priority score to each minimal subset using the priority_function
        priority_scores = [self._priority_function(subset) for subset in minimal_subsets]

        # Find the highest priority score
        max_priority = max(priority_scores)

        # Select the minimal subsets with the highest priority score
        selected_subsets = [subset for subset, priority in zip(minimal_subsets, priority_scores) if priority == max_priority]

        return selected_subsets
    
    def _priority_function(self, subset):
        # Calculate the priority score as the sum of the indices of the beliefs in the belief_order list
        priority_score = sum(self.belief_order.index(belief) for belief in subset)

        # Since we want newer beliefs to have higher priority, negate the priority score
        return -priority_score

    def _agm_postulates(self):
        # Test the implementation against AGM postulates
        pass

if __name__ == "__main__":
    agent = BeliefRevisionAgent()
    # Add beliefs, revise and test AGM postulates
    # Add a simple user input
    while True:
        print("1. Expand KB")
        print("2. Remove belief")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            formula = input("Enter the formula: ")
            agent.revise_belief(sympify(formula))
        elif choice == "2":
            formula = input("Enter the formula: ")
            agent.remove_belief(sympify(formula))
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

        print("Current belief base:", agent.belief_base)





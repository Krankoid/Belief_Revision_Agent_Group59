import itertools
from sympy.logic import to_cnf, Not, Or, And

# Better funciton name for code clarity, just applies the resolution alogrithm to the belief base and formula
def isEntailed(belief_base, formula):
    return resolution(belief_base, to_cnf(formula))

# Resoltion algorithm that utilizes the resolve function to find the resolvents of the clauses
def resolution(belief_base, formula):
    clauses = set()
    for belief in belief_base:
        clauses.update(cnfToClauses(to_cnf(belief)))

    # Setting up the negated formula for proof by contradiction
    negated_formula = to_cnf(Not(formula))
    clauses.update(cnfToClauses(negated_formula))

    while True:
        new_clauses = set()
        for c1, c2 in itertools.product(clauses, repeat=2):
            resolvents = resolve(c1, c2)
            if set() in resolvents:
                # Empty clause found, contradiction found = entailed
                return True
            new_clauses.update(resolvents)

        if new_clauses.issubset(clauses):
            # No new clauses found, no contradiction found = not entailed
            return False

        clauses.update(new_clauses)

 # Intermediary step in reolsution algorithm, that attempts to resolve two clauses with negations of literal pairs
def resolve(c1, c2):
    resolvents = set()
    for lit1 in c1:
        for lit2 in c2:
            if lit1 == ~lit2:
                resolvent = (c1 - {lit1}) | (c2 - {lit2})
                resolvents.add(frozenset(resolvent))
    return resolvents

# Converts a CNF formula to a set of clauses again
def cnfToClauses(cnf):
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
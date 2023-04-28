import itertools
from sympy import symbols
from sympy.logic import to_cnf, Not, Or, And, simplify_logic

def is_entailed(belief_base, formula):
    return resolution(belief_base, to_cnf(formula))

def resolution(belief_base, formula):
    clauses = set()
    for belief in belief_base:
        clauses.update(_cnf_to_clauses(to_cnf(belief)))

    negated_formula = to_cnf(Not(formula))
    clauses.update(_cnf_to_clauses(negated_formula))

    while True:
        new_clauses = set()
        for c1, c2 in itertools.product(clauses, repeat=2):
            resolvents = _resolve(c1, c2)
            if set() in resolvents:
                return True
            new_clauses.update(resolvents)

        if new_clauses.issubset(clauses):
            return False

        clauses.update(new_clauses)

def _cnf_to_clauses(cnf):
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


def _resolve(c1, c2):
    resolvents = set()
    for lit1 in c1:
        for lit2 in c2:
            if lit1 == ~lit2:
                resolvent = (c1 - {lit1}) | (c2 - {lit2})
                resolvents.add(frozenset(resolvent))
    return resolvents
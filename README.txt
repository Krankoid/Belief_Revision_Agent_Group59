How to use our belief revision agent:
- The belief revision agent will take incoming formulas and append them to a belief base accordingly.
- After a belief is input in either option 1 or 2, the current belief base and another datastrucutre 
    with the beliefs and their weights (also previously know beliefs) will be printed.

1. Run BeliefBaseAgent.py
2. The menu is printed:
    ----------
    1. Expand KB
    2. Contract belief
    3. Quit
    ----------
3. If you choose to expand KB, you will then be prompted to enter a formula, and afterwards a given weight from 0 to 1.
This will revise the belief base according to our selection function, which uses weights to determine importance of 
beliefs.
4. If you choose to contract a belief, simply input the belief to be contracted (that is already present in the belief base)


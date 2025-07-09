from collections import deque
import copy

def select_most_constraining_variable(csp, assignment):
    unassigned = [v for v in csp.variables if v not in assignment]

    def count_constraints(var):
        count = 0
        for other in unassigned:
            if other == var:
                continue
            if (var, other) in csp.constraints or (other, var) in csp.constraints:
                count += 1
        return count

    # Return variable with the highest number of constraints on other unassigned variables
    return max(unassigned, key=count_constraints)

def order_lcv_values(var, assignment, csp, use_lcv=True):
    """Return a list of domain values for var, ordered by LCV (least constraining value first)."""
    if not use_lcv:
        return csp.domains[var]

    def count_conflicts(value):
        """Count how many values are ruled out in neighboring unassigned variables."""
        count = 0
        for other in csp.variables:
            if other != var and other not in assignment:
                if (var, other) in csp.constraints:
                    constraint = csp.constraints[(var, other)]
                    for other_val in csp.domains[other]:
                        if not constraint(value, other_val):
                            count += 1
                elif (other, var) in csp.constraints:
                    constraint = csp.constraints[(other, var)]
                    for other_val in csp.domains[other]:
                        if not constraint(other_val, value):
                            count += 1
        return count

    return sorted(csp.domains[var], key=count_conflicts)

def ac3(domains, csp, assignment):
    """Revise domains to enforce arc consistency. Return False if any domain becomes empty."""
    queue = deque()

    # Initialize queue with all arcs (var, neighbor)
    for var in csp.variables:
        for neighbor in csp.variables:
            if var != neighbor and (var, neighbor) in csp.constraints:
                queue.append((var, neighbor))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj, csp):
            if not domains[xi]:
                return False
            for xk in csp.variables:
                if xk != xi and (xk, xi) in csp.constraints:
                    queue.append((xk, xi))
    return True


def revise(domains, xi, xj, csp):
    """Remove values from domains[xi] that are inconsistent with xj."""
    revised = False
    constraint = csp.constraints.get((xi, xj), None)
    if not constraint:
        return False

    to_remove = []
    for x in domains[xi]:
        if not any(constraint(x, y) for y in domains[xj]):
            to_remove.append(x)
            revised = True

    for x in to_remove:
        domains[xi].remove(x)

    return revised


class CSP:
    def __init__(self, variables, domains, constraints):
        """
        variables: list of variable names
        domains: dict mapping variable -> list of possible values
        constraints: dict mapping (var1, var2) -> function(var1_val, var2_val) -> bool
        """
        self.variables = variables
        self.domains = domains
        self.constraints = constraints  # binary constraints

    def is_consistent(self, var, value, assignment):
        """Check if assigning value to var is consistent with assignment."""
        for other_var in assignment:
            if (var, other_var) in self.constraints:
                if not self.constraints[(var, other_var)](value, assignment[other_var]):
                    return False
            if (other_var, var) in self.constraints:
                if not self.constraints[(other_var, var)](assignment[other_var], value):
                    return False
        return True


def backtracking_search(csp, use_mcv=True, use_lcv=True, use_ac=True):
    return backtrack({}, csp, use_mcv=use_mcv, use_lcv=use_lcv, use_ac=use_ac)


def backtrack(assignment, csp, use_mcv=True, use_lcv=True, use_ac=True):
    # If assignment is complete, return it
    if len(assignment) == len(csp.variables):
        return assignment

    # Select an unassigned variable
    if use_mcv:
        unassigned = select_most_constraining_variable(csp, assignment)
    else:
         unassigned = [v for v in csp.variables if v not in assignment]
    var = unassigned[0]

    for value in order_lcv_values(var, assignment, csp, use_lcv):
        if csp.is_consistent(var, value, assignment):
            if not use_ac:
                assignment[var] = value
                result = backtrack(assignment, csp)
                if result:
                    return result
            else:
                # Tentatively assign
                assignment[var] = value

                # Deep copy domains and prune using AC-3
                local_domains = copy.deepcopy(csp.domains)
                local_domains[var] = [value]  # reduce domain to the assigned value

                if ac3(local_domains, csp, assignment):
                    # Temporarily override CSP domains for recursive call
                    original_domains = csp.domains
                    csp.domains = local_domains
                    result = backtrack(assignment, csp)
                    csp.domains = original_domains  # restore after recursion
                    if result is not None:
                        return result
                
            del assignment[var]  # backtrack

    return None

if __name__ == '__main__':
    variables = ['A', 'B', 'C']
    domains = {
        'A': ['red', 'green'],
        'B': ['red', 'green'],
        'C': ['red', 'green']
    }

    # A and B must differ, B and C must differ
    constraints = {
        ('A', 'B'): lambda a, b: a != b,
        ('B', 'C'): lambda b, c: b != c,
    }

    csp = CSP(variables, domains, constraints)
    solution = backtracking_search(csp)
    print(solution)
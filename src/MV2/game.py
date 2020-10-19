import random

##### STATIC PARAMETERS #####

# pi_v: cost of supplier submitting outputs to the Verifier
pi_v = 0.5

# pi_cc: cost of customer committing outputs to the Verifier
pi_cc = 0.5

# pi_mc: cost of Mediator committing mediation results to the blockchain
pi_mc = 0.5

# pi_m: payout to the Mediator for being available for the duration of the service
pi_m = 0.5

# pi_ve: the Mediator's electricity cost to verify outputs
pi_ve = 0.5

# pi_cg: the customer's cost of generating an output
pi_cg = 0.5

# n: ?
n = 10

# pi_a: payout to the Allocator for providing an accepted allocation
pi_a = 0.5

# pi_se: cost to process a service input
pi_se = 0.5

# theta
#theta = 0.5


##### CONSTRAINTS #####
# n < theta
# supplier_behavior > 1/e_s = pi_cg / pi_s
# theta = lam / n



##### INPUT PARAMETERS #####
# pi_s: payout to supplier for doing job
# lam: number of inputs
# b: benefit to customer for job


##### DEPENDENT PARAMETERS #####

def get_theta(lam):
    return lam / n

def get_pi_sd(pi_s, theta):
    return pi_s * theta


def get_pi_cd(pi_s, theta):
    return pi_s * theta


##### GAME FUNCTIONS #####


def get_game_outcome(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return "O1"
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return "O2"
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return "O3"
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return "04"
    else:
        return None


def check_mediation(outcome):
    # if mediation is required for this outcome return "true" otherwise return "false"
    if outcome == "O1":
        return "false"
    else:
        return "true"


def get_customer_pay(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return v['lam'] * (v['b'] - v['pi_s']) - n * (pi_cg - pi_cc) - pi_a
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return -v['lam'] * v['pi_s'] - n * (pi_cg - pi_cc) - pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return v['lam'] * (v['b'] - v['pi_s']) - n * pi_cc - get_pi_cd(v['pi_s']) - pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return -v['lam'] * v['pi_s'] - n * pi_cc - get_pi_cd(v['pi_s']) - pi_a
    else:
        return None


def get_supplier_pay(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return v['lam'] * (v['pi_s'] - pi_se) - n * pi_v - pi_a
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return -n * pi_v - get_pi_sd(v['pi_s']) - pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return v['lam'] * (v['pi_s'] - pi_se) - n * pi_v - pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return n * pi_v - get_pi_sd(v['pi_s']) - pi_a
    else:
        return None


def get_allocator_pay(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return pi_a
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return pi_a
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return pi_a
    else:
        return None


def get_mediator_pay(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return pi_m
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return pi_m - n * (pi_se - pi_ve + v['pi_s']) - pi_mc
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return pi_m - n * (pi_se - pi_ve + v['pi_s']) - pi_mc
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return pi_m - n * (pi_se - pi_ve + v['pi_s']) - pi_mc
    else:
        return None
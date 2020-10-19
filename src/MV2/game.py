import random


##### SIMULATION PARAMETERS #####


lam = 12000
n = 12
replicas = 1
theta = 1000
pi_cc = 0.1
pi_v = 0.1
pi_a = 0.0000033
pi_cg = 7e-8
pi_se = 7e-8
pi_s = 0.00002
b = 0.000035
pi_cd = pi_s * theta
pi_sd = pi_s * theta
pi_m = 0.000033

# need to confirm with scott
pi_mc = 0.1
pi_ve = 0.0


##### GAME FUNCTIONS #####


def get_game_outcome(v):
    if (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "process"):
        return "O1"
    elif (v["customerbehavior"] == "process") and (v['supplierbehavior'] == "cheat"):
        return "O2"
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "process"):
        return "O3"
    elif (v["customerbehavior"] == "cheat") and (v['supplierbehavior'] == "cheat"):
        return "O4"
    else:
        return None


def check_mediation(outcome):
    # if mediation is required for this outcome return "true" otherwise return "false"
    if outcome == "O1":
        return "false"
    else:
        return "true"


##### PAYOUT FUNCTIONS #####


def get_customer_pay(outcome):
    if outcome == "O1":
        return lam * (b - pi_s) - n * pi_cg - pi_cc - pi_a
    elif outcome == "O2":
        return -lam * pi_s - n * pi_cg - pi_cc - pi_a
    elif outcome == "O3":
        return lam * (b - pi_s) - pi_cc - pi_cd - pi_a
    elif outcome == "O4":
        return -lam * pi_s - pi_cc - pi_cd - pi_a
    else:
        return None


def get_supplier_pay(outcome):
    if outcome == "O1":
        return lam * (pi_s - pi_se) - pi_v - pi_a
    elif outcome == "O2":
        return -pi_v - pi_sd - pi_a
    elif outcome == "O3":
        return lam * (pi_s - pi_se) - pi_v - pi_a
    elif outcome == "O4":
        return -pi_v - pi_sd - pi_a
    else:
        return None


def get_allocator_pay(outcome):
    if outcome == "O1":
        return pi_a
    elif outcome == "O2":
        return pi_a
    elif outcome == "O3":
        return pi_a
    elif outcome == "O4":
        return pi_a
    else:
        return None


def get_mediator_pay(outcome):
    if outcome == "O1":
        return pi_m
    elif outcome == "O2":
        return pi_m - n * (pi_se - pi_ve + pi_s) - pi_mc
    elif outcome == "O3":
        return pi_m - n * (pi_se - pi_ve + pi_s) - pi_mc
    elif outcome == "O4":
        return pi_m - n * (pi_se - pi_ve + pi_s) - pi_mc
    else:
        return None
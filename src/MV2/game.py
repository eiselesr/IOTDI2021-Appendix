import random

##### STATIC PARAMETERS #####

# pi_se_sf: scaling factor
pi_se_sf = 0.5

# pi_mi_sf: scaling factor
pi_mi_sf = 0.5

# pi_cg: cost to customer for generating n inputs
pi_cg = 0.5

# pi_cc: cost to customer for commiting n inputs to bc
pi_cc = 0.5

# pi_a: payout to allocator
pi_a = 0.5

# pi_m: payout to mediator
pi_m = 0.5

# pi_sc: cost to supplier for sending n inputs to bc
pi_sc = 0.5

# pr: penalty rate
pr = 0.5

##### DEPENDENT PARAMETERS #####

def get_pi_se(pi_s, pi_se_sf):
    # pi_se: cost to process a service input
    return pi_s * pi_se_sf


def get_pi_mi(pi_s, pi_mi_sf):
    # pi_mi: payout to mediator for mediating
    return pi_s * pi_mi_sf


def get_pi_sd():
    # pi_sd: security deposit for supplier
    return 1


def get_pi_cd():
    # pi_cd: security deposit for customer
    return 1


##### GAME FUNCTIONS #####


def get_game_outcome():
    # returns "O1", "02", "03" or "04"
    return "O1"


def check_mediation(outcome):
    # if mediation is required for this outcome return "true" otherwise return "false"
    if outcome == "O1":
        return "false"
    else:
        return "true"


def get_customer_pay():
    return 1


def get_supplier_pay():
    return 1


def get_mediator_pay():
    return 1


def get_allocator_pay():
    return pi_a
import numpy as np


def current_tax(income):
    if income <= 150473:
        bpa = 13229
    elif income >= 214368:
        bpa = 12298
    else:
        bpa = np.interp(income, [150473, 214368], [13229, 12298])

    if income <= 48535:
        tax = income * 0.15
    elif income <= 97069:
        tax = (income - 48535) * 0.205 + 7280
    elif income <= 150473:
        tax = (income - 97069) * 0.26 + 17230
    elif income <= 214368:
        tax = (income - 150473) * 0.29 + 31115
    else:
        tax = (income - 214368) * 0.33 + 49645

    net_tax = tax - 0.15 * bpa

    if net_tax < 0:
        net_tax = 0

    return net_tax


def new_tax(income, rate, ubi):
    tax = rate * income - ubi

    return tax

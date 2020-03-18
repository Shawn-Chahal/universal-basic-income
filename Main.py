import numpy as np
import pandas as pd
from TaxCalculator import current_tax, new_tax


def round_up(num, dec):
    if round(num, dec) > num:
        return round(num, dec)
    else:
        return round(num, dec) + 10 ** (-dec)


income_distribution = pd.read_csv('income_distribution.csv').to_numpy()
percentile = income_distribution[:, 0]
income = income_distribution[:, 1]
population = 30319388  # Number of taxpayers
percentile_h = np.linspace(0, 1, population)
income_h = np.interp(percentile_h, percentile, income)
ubi = 16500
qc_abate = 0.165  # Quebec abatement
qc_prop = 0.232  # Fraction of Canadians from Quebec
tax_prop = ((1 - qc_prop) + (1 - qc_abate) * qc_prop)  # Fraction of federal tax remaining after Quebec abatement

income_total = sum(income_h)

current_taxes = np.zeros(population)
for i in range(population):
    current_taxes[i] = current_tax(income_h[i])

required_tax_total_a = tax_prop * sum(current_taxes)
rate_a = (required_tax_total_a / tax_prop + (ubi * population)) / income_total
rate_a = round_up(rate_a, 3)
new_taxes_a = new_tax(income_h, rate_a, ubi)
new_tax_total_a = tax_prop * sum(new_taxes_a)

required_tax_total_b = 169.71 * 10 ** 9
rate_b = (required_tax_total_b / tax_prop + (ubi * population)) / income_total
rate_b = round_up(rate_b, 3)
new_taxes_b = new_tax(income_h, rate_b, ubi)
new_tax_total_b = tax_prop * sum(new_taxes_b)

delta_taxes_a = new_taxes_a - current_taxes
delta_taxes_b = new_taxes_b - current_taxes

index_a = -1
index_b = -1
for i in range(population - 1):
    if delta_taxes_a[i] * delta_taxes_a[i + 1] < 0:
        index_a = i
    if delta_taxes_b[i] * delta_taxes_b[i + 1] < 0:
        index_b = i
    if index_a != -1 and index_b != -1:
        break

pd.DataFrame({'Rate A': [rate_a], 'Rate B': [rate_b]}).to_csv('rates.csv')

open('results.txt', 'w').close()

results = open('results.txt', 'a')
results.write('\n')
results.write('Universal Basic Income: $%.0f\n' % ubi)
results.write('\n')
results.write('Scenario A\n')
results.write('Tax rate:               %.3f\n' % rate_a)
results.write('Required tax revenue:   $%.1f billion\n' % (required_tax_total_a * 10 ** -9))
results.write('New tax revenue:        $%.1f billion\n' % (new_tax_total_a * 10 ** -9))
results.write('Crossover [Percentile]  %.3f\n' % percentile_h[index_a])
results.write('Crossover [Income]      $%.0f\n' % income_h[index_a])
results.write('\n')
results.write('Scenario B\n')
results.write('Tax rate:               %.3f\n' % rate_b)
results.write('Required tax revenue:   $%.1f billion\n' % (required_tax_total_b * 10 ** -9))
results.write('New tax revenue:        $%.1f billion\n' % (new_tax_total_b * 10 ** -9))
results.write('Crossover [Percentile]  %.3f\n' % percentile_h[index_b])
results.write('Crossover [Income]      $%.0f\n' % income_h[index_b])
results.write('\n')
results.close()

results = open('results.txt', 'r')
print(results.read())
results.close()

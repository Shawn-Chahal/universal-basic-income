import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from TaxCalculator import current_tax, new_tax


def ubi_figure(name, rate, ubi, override=False, preview=False):
    units = 1000
    limit = 250000
    sublimit = 100000
    resolution = int(limit / 10) + 1
    sublimit_index = int(sublimit / 10)
    income = np.linspace(0, limit, resolution)

    current_taxes = np.zeros(resolution)

    for i in range(resolution):
        current_taxes[i] = current_tax(income[i])

    new_taxes = new_tax(income, rate, ubi)
    current_at_income = income - current_taxes
    new_at_income = income - new_taxes
    delta_at_income = new_at_income - current_at_income

    font_size_axis_label = 9
    font_size_title = 2 * font_size_axis_label
    font_size_legend = 0.9 * font_size_axis_label
    font_size_tick_label = 0.85 * font_size_axis_label

    substep_x = 10000
    subrange_x = np.arange(0, income[sublimit_index] + substep_x, substep_x)
    subrange_y = np.arange(0, np.max([current_at_income[sublimit_index], new_at_income[sublimit_index]]) + substep_x,
                           substep_x)

    substep_y2 = 3000
    subrange_y2 = np.arange(np.floor(delta_at_income[sublimit_index] / substep_y2).astype(int) * substep_y2,
                            delta_at_income[0] + substep_y2, substep_y2)

    step_x = 25000
    range_x = np.arange(0, income[-1] + step_x, step_x)
    range_y = np.arange(0, np.max([current_at_income[-1], new_at_income[-1]]) + step_x, step_x)

    step_y2 = 6000
    range_y2 = np.arange(np.floor(delta_at_income[-1] / step_y2).astype(int) * step_y2, delta_at_income[0] + step_y2,
                         step_y2)

    if override:
        subrange_y2 = np.arange(-15000, 18000 + substep_y2, substep_y2)
        range_y2 = np.arange(-42000, 18000 + step_y2, step_y2)

    grid_alpha = 0.25
    fill_alpha = 0.2
    positive_fill = 'green'
    negative_fill = 'red'

    dpi = 600

    if preview:
        dpi = 200

    plt.figure(figsize=(6.5, 6.0), dpi=dpi)
    plt.suptitle(name, fontsize=font_size_title)

    plt.subplot(2, 2, 1)
    plt.plot(income, current_at_income, label='Current tax', linestyle='--', color='grey')
    plt.plot(income, new_at_income, label='New tax', linestyle='-', color='black')
    plt.ylabel('Income after federal tax [$1000]', fontsize=font_size_axis_label)
    plt.xticks(subrange_x, (subrange_x / units).astype(int), fontsize=font_size_tick_label)
    plt.yticks(subrange_y, (subrange_y / units).astype(int), fontsize=font_size_tick_label)
    plt.xlim(subrange_x[0], subrange_x[-1])
    plt.ylim(subrange_y[0], subrange_y[-1])
    plt.grid(b=True, which='both', axis='both', alpha=grid_alpha)
    plt.legend(framealpha=1, fontsize=font_size_legend)
    plt.fill_between(income[new_at_income > current_at_income], current_at_income[new_at_income > current_at_income],
                     new_at_income[new_at_income > current_at_income], color=positive_fill, alpha=fill_alpha)
    plt.fill_between(income[new_at_income < current_at_income], current_at_income[new_at_income < current_at_income],
                     new_at_income[new_at_income < current_at_income], color=negative_fill, alpha=fill_alpha)

    plt.subplot(2, 2, 2)
    plt.plot(income, current_at_income, label='Current tax', linestyle='--', color='grey')
    plt.plot(income, new_at_income, label='New tax', linestyle='-', color='black')
    plt.xticks(range_x, (range_x / units).astype(int), fontsize=font_size_tick_label)
    plt.yticks(range_y, (range_y / units).astype(int), fontsize=font_size_tick_label)
    plt.xlim(range_x[0], range_x[-1])
    plt.ylim(range_y[0], range_y[-1])
    plt.grid(b=True, which='both', axis='both', alpha=grid_alpha)
    plt.fill_between(income[new_at_income > current_at_income], current_at_income[new_at_income > current_at_income],
                     new_at_income[new_at_income > current_at_income], color=positive_fill, alpha=fill_alpha)
    plt.fill_between(income[new_at_income < current_at_income], current_at_income[new_at_income < current_at_income],
                     new_at_income[new_at_income < current_at_income], color=negative_fill, alpha=fill_alpha)

    plt.subplot(2, 2, 3)
    plt.plot(income, delta_at_income, linestyle='-', color='black')
    plt.axhline(0, linestyle='--', color='grey')
    plt.xlabel('Income [$1000]', fontsize=font_size_axis_label)
    plt.ylabel('Change in after tax income [$1000]', fontsize=font_size_axis_label)
    plt.xticks(subrange_x, (subrange_x / units).astype(int), fontsize=font_size_tick_label)
    plt.yticks(subrange_y2, (subrange_y2 / units).astype(int), fontsize=font_size_tick_label)
    plt.xlim(subrange_x[0], subrange_x[-1])
    plt.ylim(subrange_y2[0], subrange_y2[-1])
    plt.grid(b=True, which='both', axis='both', alpha=grid_alpha)
    plt.fill_between(income[delta_at_income > 0], 0, delta_at_income[delta_at_income > 0], color=positive_fill,
                     alpha=fill_alpha)
    plt.fill_between(income[delta_at_income < 0], 0, delta_at_income[delta_at_income < 0], color=negative_fill,
                     alpha=fill_alpha)

    plt.subplot(2, 2, 4)
    plt.plot(income, delta_at_income, linestyle='-', color='black')
    plt.axhline(0, linestyle='--', color='grey')
    plt.xlabel('Income [$1000]', fontsize=font_size_axis_label)
    plt.xticks(range_x, (range_x / units).astype(int), fontsize=font_size_tick_label)
    plt.yticks(range_y2, (range_y2 / units).astype(int), fontsize=font_size_tick_label)
    plt.xlim(range_x[0], range_x[-1])
    plt.ylim(range_y2[0], range_y2[-1])
    plt.grid(b=True, which='both', axis='both', alpha=grid_alpha)
    plt.fill_between(income[delta_at_income > 0], 0, delta_at_income[delta_at_income > 0], color=positive_fill,
                     alpha=fill_alpha)
    plt.fill_between(income[delta_at_income < 0], 0, delta_at_income[delta_at_income < 0], color=negative_fill,
                     alpha=fill_alpha)

    plt.tight_layout(rect=(0, 0, 1, 0.95))

    filename = name.lower().replace(' ', '_') + '.png'
    plt.savefig(fname=filename, dpi=600)


df_rates = pd.read_csv('rates.csv')
rate_a = df_rates['Rate A'].to_numpy()[0]
rate_b = df_rates['Rate B'].to_numpy()[0]
ubi = 16500

override = True
preview = False

ubi_figure('Scenario A', rate_a, ubi, override=override, preview=preview)
ubi_figure('Scenario B', rate_b, ubi, override=override, preview=preview)

if preview:
    plt.show()

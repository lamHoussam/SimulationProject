import math
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest
import argparse


def load_e(file_name, precision):
    e = 2
    with open(file_name, "r") as file:
        e = file.read().replace('\n', '')

    return e[2:precision+2]


def plot_digits_count(digit_counts, observed_frequencies, expected_frequencies):
    fig, ax = plt.subplots()
    x = list(digit_counts.keys())
    ax.bar(x, observed_frequencies, label='Fréquences observées')
    ax.plot(x, expected_frequencies, 'r-', label='Fréquences attendues')
    ax.set_xlabel('Chiffre')
    ax.set_ylabel('Fréquence')
    ax.legend()
    plt.show()


def chi_squared_test(e_value, precision):
    digit_counts = {str(i): 0 for i in range(10)}

    for digit in e_value:
        digit_counts[digit] += 1

    expected_frequency = precision / 10
    expected_frequencies = [expected_frequency] * 10

    observed_frequencies = list(digit_counts.values())

    chi_squared = sum((observed - expected) ** 2 / expected for observed,
                      expected in zip(observed_frequencies, expected_frequencies))
    sum_value = sum(observed_frequencies)

    print("Test du chi-deux :")
    print(f"Statistique du test : {chi_squared}")
    print(f"Sum value: {sum_value} and precision: {precision}")
    print(f"Dictionay: {digit_counts}")

    plot_digits_count(digit_counts, observed_frequencies, expected_frequencies)


# def kolmogorov_smirnov_test(e_value, precision):
#     digit_counts = {str(i): 0 for i in range(10)}

#     for digit in e_value:
#         digit_counts[digit] += 1

#     exp_function = np.arange(1, precision + 1) / precision
#     th_function = np.arange(1, precision + 1) / (precision + 1)
#     ks_statistic = np.max(np.abs(exp_function - th_function))

#     print("Test de Kolmogorov-Smirnov :")
#     print(f"Statistique du test : {ks_statistic}")


#     fig, ax = plt.subplots()
#     ax.step(np.arange(0, precision + 1), np.concatenate(([0], exp_function)), label='ECDF empirique')
#     ax.plot(np.arange(0, precision + 1), np.concatenate(([0], th_function)), 'r-', label='CDF théorique')
#     ax.set_xlabel('Nombre')
#     ax.set_ylabel('Probabilité')
#     ax.legend()
#     plt.show()

def evaluate_hand(hand):
    hand_set = set(hand)
    if len(hand_set) == 1:
        return 'Poker'
    elif len(hand_set) == 2 and hand.count(hand[0]) in [2, 3]:
        return 'Full'
    elif len(hand_set) == 3 and len([x for x in hand_set if hand.count(x) == 2]) == 2:
        return 'Double Paire'
    elif len(hand_set) == 3:
        return 'Brelan'
    elif len(hand_set) == 4:
        return 'Paire'
    else:
        return 'None'

# TODO: Use caching
def stirling_number(k, r):
    return 1 if r == 1 or r == k else stirling_number(k-1, r-1) + r * stirling_number(k-1, r)

def poker_test(e_value, precision):
    classes_occurences = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    expected_occurences = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    groups = [e_value[i:i+5] for i in range(0, precision, 5)]

    n = 0
    for hand in groups:
        hand_set = set(hand)
        classes_occurences[len(hand_set)] += 1
        n += 1


    d = 10
    k = 5

    for r in range(1, k+1):
        coeff = stirling_number(k, r)
        for val in range(d-r+1, d+1):
            coeff *= val
        expected_occurences[r] = n * (coeff) / (d ** k)

    chi_squared = 0
    for key in classes_occurences.keys():
        value =  ((classes_occurences[key] - expected_occurences[key]) ** 2)  / (expected_occurences[key] if expected_occurences[key] != 0 else 1)
        print(f"Value for key {key}: {value}")
        chi_squared += value

    print(f"Observed: {classes_occurences}; \nExpected: {expected_occurences}")

    print(f"Chi-square: {chi_squared}")

    fig, ax = plt.subplots()

    ax.bar(list(classes_occurences.keys()), list(classes_occurences.values()), label='Occurrences des classes de poker dans les décimales de e')
    ax.plot(list(expected_occurences.keys()), list(expected_occurences.values()), 'r-', label='Fréquences attendues')
    ax.set_xlabel('Classe de poker')
    ax.set_ylabel('Occurrences')
    plt.show()


def test_all(e_value, precision):
    test_functions = [func for func_name,
                      func in available_tests.items() if func_name != 'all']
    for func in test_functions:
        func(e_value, precision)


available_tests = {
    'chi': chi_squared_test,
    'poker': poker_test,
    'all': test_all,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', default='all',
                        help='Test to use to study randomness of e')
    parser.add_argument('--precision', type=int,
                        default=2_000_000, help='Precision value')
    parser.add_argument('--list', action='store_true',
                        help='Lists available tests', default=False)
    args = parser.parse_args()

    list_tests = args.list
    if list_tests:
        print("Availble Tests")
        print(list(available_tests.keys()))
        exit(0)

    precision = args.precision

    if precision <= 0 or precision > 2_000_000:
        print(f"Precision must be between 0 and 2_000_000")
        exit(1)

    test_to_use = args.test
    test_function = available_tests.get(test_to_use)

    if test_function is None:
        print(f"{test_to_use} is not available")
        exit(1)

    e = str(load_e("e2M.txt", precision))
    print(f"Args : {args.test} with precision {precision}")
    test_function(e, precision)
    # print(f"value : {e}")


if __name__ == '__main__':
    main()

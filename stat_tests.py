import matplotlib.pyplot as plt
from scipy.stats import kstest


def chi_squared_test(sequence, is_digit_sequence=True):
    created_sequence = list()
    if not is_digit_sequence:
        for i in sequence:
            created_sequence.append(str(int(i * 10)))
    else:
        created_sequence = list(sequence)

    digit_counts = {str(i): 0 for i in range(10)}

    for digit in created_sequence:
        digit_counts[digit] += 1

    length = len(created_sequence)

    expected_frequency = length / 10
    expected_frequencies = [expected_frequency] * 10

    observed_frequencies = list(digit_counts.values())

    chi_squared = sum((observed - expected) ** 2 / expected for observed,
                      expected in zip(observed_frequencies, expected_frequencies))
    sum_value = sum(observed_frequencies)

    print("Test du chi-deux :")
    print(f"Statistique du test : {chi_squared}")
    print(f"Sum value: {sum_value} and precision: {length}")
    print(f"Dictionay: {digit_counts}")

    _, ax = plt.subplots()
    x = list(digit_counts.keys())
    ax.bar(x, observed_frequencies, label='Fréquences observées')
    ax.plot(x, expected_frequencies, 'r-', label='Fréquences attendues')
    ax.set_xlabel('Chiffre')
    ax.set_ylabel('Fréquence')
    ax.legend()
    plt.show()


def ks_test(sequence, is_digit_sequence=True):
    sequence.sort()
    n = len(sequence)

    d_value, p_value = kstest(sequence, 'uniform')

    print("Test de Kolmogorov-Smirnov :")
    print(f"D_value : {d_value}")
    print(f"P_value : {p_value}")


# TODO: Use caching
def stirling_number(k, r):
    return 1 if r == 1 or r == k else stirling_number(k-1, r-1) + r * stirling_number(k-1, r)


def poker_test(sequence, is_digit_sequence=True):
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

    created_sequence = list()
    if not is_digit_sequence:
        for i in sequence:
            created_sequence.append(str(int(i * 10)))
    else:
        created_sequence = list(sequence)


    length = len(created_sequence)

    groups = [created_sequence[i:i+5] for i in range(0, length, 5)]

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
        value = ((classes_occurences[key] - expected_occurences[key]) ** 2) / (
            expected_occurences[key] if expected_occurences[key] != 0 else 1)
        print(f"Value for key {key}: {value}")
        chi_squared += value

    print(f"Observed: {classes_occurences}; \nExpected: {expected_occurences}")

    print(f"Chi-square: {chi_squared}")

    fig, ax = plt.subplots()

    ax.bar(list(classes_occurences.keys()), list(classes_occurences.values()),
           label='Occurrences des classes de poker dans les décimales de e')
    ax.plot(list(expected_occurences.keys()), list(
        expected_occurences.values()), 'r-', label='Fréquences attendues')
    ax.set_xlabel('Classe de poker')
    ax.set_ylabel('Occurrences')
    plt.show()

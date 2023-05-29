import math
import random
import matplotlib.pyplot as plt


def load_e(file_name, precision=2_000_000):
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


def main():
    # precision = 2_000_000
    precision = 100000
    e = str(load_e("e2M.txt", precision))
    print(f"Value : {e}")

    chi_squared_test(e, precision)


if __name__ == '__main__':
    main()

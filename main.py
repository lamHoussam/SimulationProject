import random
import argparse

import matplotlib.pyplot as plt

from stat_tests import ks_test, chi_squared_test, poker_test
from generators import ESimpleRandomGenerator, LCERandomGenerator


def load_e(file_name, precision):
    e = 2
    with open(file_name, "r") as file:
        e = file.read().replace('\n', '')

    return e[2:precision+2]


def test_all(sequence, is_digit_sequence=True):
    test_functions = [func for func_name,
                      func in available_tests.items() if (func_name != 'all' and func_name != 'ks') or (func_name == 'ks' and not is_digit_sequence)]
    for func in test_functions:
        func(sequence, is_digit_sequence)


available_tests = {
    'chi': chi_squared_test,
    'poker': poker_test,
    'ks': ks_test,
    'all': test_all,
}

available_generators = {
    'lcm': LCERandomGenerator,
    'simple': ESimpleRandomGenerator,
}


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--test', default='all',
                        help='Test to use to study randomness of e')
    parser.add_argument('--precision', type=int,
                        default=2_000_000, help='Precision value')
    parser.add_argument('--list', action='store_true',
                        help='Lists available tests and available generators', default=False)
    parser.add_argument('--generate', default=0, type=int,
                        help='Generate values using the custom random generator')
    parser.add_argument(
        '--seed', help='Seed for custom RNG', default=1, type=int)

    parser.add_argument('--generator', default='lcm',
                        help='Random number Generator to use')

    args = parser.parse_args()

    list_tests = args.list
    if list_tests:
        print("Availble Tests")
        print(list(available_tests.keys()))
        print("Available Generators")
        print(list(available_generators.keys()))
        exit(0)

    precision = args.precision

    if precision <= 19 or precision > 2_000_000:
        print(f"Precision must be between 20 and 2_000_000")
        exit(1)

    e = str(load_e("e2M.txt", precision))

    custom_random_numbers = e
    if args.generate != 0:
        if args.generate > 200_000:
            print(f"Max Generation 200_000")
            exit(1)

        generator_class = available_generators.get(args.generator)
        if generator_class is None:
            print(
                "Can't find this generator\nUse python main.py --list \nto see available generators")
            exit(1)

        generator = generator_class(args.seed, e, precision)
        python_random_numbers = list()
        custom_random_numbers = list()

        for _ in range(args.generate):
            val = generator.generate_random()
            py_val = random.random()

            custom_random_numbers.append(val)
            python_random_numbers.append(py_val)

        with open("custom_output.txt", "w") as f:
            f.write(str(custom_random_numbers))

        with open("python_output.txt", "w") as f:
            f.write(str(python_random_numbers))

        plt.hist(custom_random_numbers, bins=20,
                 alpha=0.5, label='Your Generator')
        plt.hist(python_random_numbers, bins=20,
                 alpha=0.5, label='random Module')
        plt.xlabel('Random Number')
        plt.ylabel('Frequency')
        plt.title('Comparison of Random Number Generators')
        plt.legend()
        plt.show()

        test_to_use = args.test
        test_function = available_tests.get(test_to_use)

        if test_function is None:
            print(f"{test_to_use} is not available")
            exit(1)

        test_function(custom_random_numbers, not args.generate)
        test_function(python_random_numbers, not args.generate)

        return

    if args.test == 'ks':
        print(f"Cant use ks to study decimals of e")
        exit(1)

    test_to_use = args.test
    test_function = available_tests.get(test_to_use)

    if test_function is None:
        print(f"{test_to_use} is not available")
        exit(1)

    test_function(custom_random_numbers, not args.generate)


if __name__ == '__main__':
    main()

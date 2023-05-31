import math
import random
import matplotlib.pyplot as plt
from scipy.stats import kstest
import argparse

from stat_tests import ks_test, chi_squared_test, poker_test
from generators import ESimpleRandomGenerator, LCERandomGenerator


def load_e(file_name, precision):
    e = 2
    with open(file_name, "r") as file:
        e = file.read().replace('\n', '')

    return e[2:precision+2]


def test_all(sequence):
    test_functions = [func for func_name,
                      func in available_tests.items() if func_name != 'all']
    for func in test_functions:
        func(sequence)


available_tests = {
    'chi'  : chi_squared_test,
    'poker': poker_test,
    'ks'   : ks_test,
    'all'  : test_all,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', default='all',
                        help='Test to use to study randomness of e')
    parser.add_argument('--precision', type=int,
                        default=2_000_000, help='Precision value')
    parser.add_argument('--list', action='store_true',
                        help='Lists available tests', default=False)
    parser.add_argument('--generate', action='store_true',
                        help='Generate values using the custom random generator', default=False)

    args = parser.parse_args()

    list_tests = args.list
    if list_tests:
        print("Availble Tests")
        print(list(available_tests.keys()))
        exit(0)

    precision = args.precision

    if precision <= 19 or precision > 2_000_000:
        print(f"Precision must be between 20 and 2_000_000")
        exit(1)

    e = str(load_e("e2M.txt", precision))

    data = e

    if args.generate:
        generator = LCERandomGenerator(1, e, precision)
        python_random_numbers = list()
        custom_random_numbers = list()

        for _ in range(1000):
            val = generator.generate_random()
            py_val = random.random()
            
            print(f"Py val : {py_val}")
            print(f"Cs val : {val}")

            custom_random_numbers.append(val)
            python_random_numbers.append(py_val)


    test_to_use = args.test
    test_function = available_tests.get(test_to_use)

    if test_function is None:
        print(f"{test_to_use} is not available")
        exit(1)

    # print(f"Args : {args.test} with precision {precision}")
    # print(f"value : {e}")

    test_function(e)


if __name__ == '__main__':
    main()

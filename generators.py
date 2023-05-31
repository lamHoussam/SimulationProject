from math import sqrt


def get_prime_dividers(n):
    prime_dividers = []

    while n % 2 == 0:
        prime_dividers.append(2)
        n = n // 2

    for i in range(3, int(sqrt(n)) + 1, 2):
        while n % i == 0:
            prime_dividers.append(i)
            n = n // i

    if n > 2:
        prime_dividers.append(n)

    return prime_dividers


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def are_coprime(a, b):
    return gcd(a, b) == 1


class LCERandomGenerator():
    def __init__(self, seed, e_value, precision):
        self.initial_seed = seed
        self.last_value = seed
        self.last_calculated_index = seed
        self.decimals = 10
        self.m = precision - self.decimals

        # Calculate optimal parameters to maximise cycle
        self.c = 2

        while not are_coprime(self.c, self.m) and self.c < self.m:
            self.c += 1

        dividers = get_prime_dividers(self.m)
        self.a = 1
        for p in dividers:
            self.a *= p
        self.a += 1

        if self.m % 4 == 0 and self.a % 4 != 0:
            self.a *= 4 if self.a % 4 != 2 else 2

        self.e_value = e_value

    def generate_random(self):
        calculated_index = (self.last_calculated_index *
                            self.a + self.c) % self.m
        value = int(
            self.e_value[calculated_index:calculated_index + self.decimals]) / (10 ** self.decimals)
        self.last_calculated_index = calculated_index
        self.last_value = value
        return value


class ESimpleRandomGenerator():
    def __init__(self, seed, e_value, precision):
        self.initial_seed = seed
        self.last_value = seed
        self.last_calculated_index = seed % precision
        self.e_value = e_value
        self.decimals = 10

    def generate_random(self):
        value = int(
            self.e_value[self.last_calculated_index:self.last_calculated_index + self.decimals]) / (10 ** self.decimals)

        self.last_calculated_index += self.decimals
        self.last_value = value

        return value


class EMidSquareRandomGenerator():
    pass

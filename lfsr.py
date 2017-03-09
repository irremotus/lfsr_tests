#!/usr/bin/python3
""" Linear Feedback Shift Register Test Framework
    Author:   Kevin Schmittle
    Date:     March 9, 2017
"""

import sys


class LFSR:
    """Simulates a linear feedback shift register (LFSR)"""
    def __init__(self, num_bits, polynomial, seed):
        # basic parameter error checking
        if not isinstance(num_bits, int):
            raise Exception("num_bits must be integer")
        if not isinstance(polynomial, list):
            raise Exception("polynomial must be list")
        if not isinstance(seed, list):
            raise Exception("seed must be list")
        if num_bits != len(seed):
            raise Exception("seed size must match num_bits")
        if num_bits != len(polynomial):
            raise Exception("polynomial size must match num_bits")

        self.num_bits = num_bits
        self.polynomial = polynomial
        self.seed = seed
        self.state = seed

    def next(self):
        """Generate the next value in the sequence."""
        new_val = 0
        for index, value in enumerate(self.state):
            if self.polynomial[self.num_bits - index - 1]:
                new_val ^= value
        ret_val = self.state.pop()
        self.state.insert(0, new_val)
        return ret_val

    def get_state(self):
        """Get the current state of the LFSR."""
        return self.state[:]


def get_bin(num, num_bits):
    """Format a number in binary with num_bits bits."""
    bnum = bin(num).split("b")[1]
    return "0"*(num_bits - len(bnum)) + bnum


def make_list(string):
    """Turn a binary string into a list of integers."""
    return [int(x) for x in list(string)]


def make_str(list_of_ints):
    """Turn a list of binary integers into a string."""
    return "".join([str(x) for x in list_of_ints])


def states_hash(states):
    """Generate a hash of a list of states."""
    return "|".join(sorted(states))


def main():
    """Run the tests."""
    poly = sys.argv[1]
    num_bits = len(poly)
    states_set = []
    states_data = []
    # loop through all the starting states
    for i in range(2**num_bits):
        num = get_bin(i, num_bits)
        lfsr = LFSR(num_bits, make_list(poly), make_list(num))
        states = [make_str(lfsr.get_state())]
        # loop through total number of possible values
        for _ in range(2**num_bits):
            lfsr.next()
            new_state = make_str(lfsr.get_state())
            if new_state in states:
                if states_hash(states) not in states_set:
                    states_set.append(states_hash(states))
                    states_data.append((num, states))
                break
            else:
                states.append(new_state)

    # output the results
    print("{} loops:\n".format(len(states_data)))
    for states in states_data:
        print("Seed: {}\nStates: {}\nPeriod: {}\n".format(states[0], states[1], len(states[1])))


def print_usage():
    """Print the usage info."""
    print("Usage: {} <polynomial>".format(sys.argv[0]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        exit(1)
    main()

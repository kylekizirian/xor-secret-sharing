import argparse
import random

def generate_random_share(length):
    share = []
    for _ in range(length):
        share.append(random.randint(0, 127)) # ascii char/1 byte range
    return share

def generate_naive_secret_share():
    # TODO
    pass

def generate_simple_secret_share():
    # TODO
    pass

def generate_cyclic_secret_share():
    # TODO
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XOR secret sharing parameters')
    parser.add_argument('--secret', help="Your secret string", required=True)
    parser.add_argument('--output', help="Text file to write output to", required=True)
    parser.add_argument('--n', help="Number of shares per secret", required=True)
    parser.add_argument('--m', help="Number of fake secrets", required=True)

    secret_approach = parser.add_mutually_exclusive_group(required=True)
    secret_approach.add_argument('--NAIVE', help="NAIVE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--SIMPLE', help="SIMPLE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--CYCLIC', help="CYCLIC approach to deceptive secret sharing", action='store_true')

    args = parser.parse_args()

    print("Original secret:")
    print(args.secret + "\n")

    # generate n-1 random secret shares that are same length as secret
    shares_list = []
    for _ in range(int(args.n) - 1):
        individual_share = generate_random_share(len(args.secret))
        shares_list.append(individual_share)

    secret_to_ascii = []
    for i in range(len(args.secret)):
        secret_to_ascii.append(ord(args.secret[i]))

    # generate the last share by XOR each random share with original secret
    last_share = []
    for i in range(len(args.secret)):
        val = 127
        for j in range(len(shares_list)):
            val = val ^ shares_list[j][i]
        val = val ^ secret_to_ascii[i]
        last_share.append(val)

    shares_list.append(last_share)
    recreated_secret = ""

    # recreate original secret by XOR all shares together
    for i in range(len(args.secret)):
        val = 127
        for j in range(len(shares_list)):
            val = val ^ shares_list[j][i]
        recreated_secret = recreated_secret + chr(val)
    
    print("Recreated secret:")
    print(recreated_secret)

    if args.NAIVE:
      generate_naive_secret_share()

    if args.SIMPLE:
        generate_simple_secret_share()

    if args.CYCLIC:
        generate_cyclic_secret_share()

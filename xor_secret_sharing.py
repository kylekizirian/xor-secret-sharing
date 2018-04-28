import argparse
import os
import random

def get_random_fake_secret(length):
    random_line_number = random.randint(124, 5000)
    file_path = os.path.join(os.curdir, "Frankenstein", "Frankenstein.txt")

    with open(file_path) as file:
        lines = (line.rstrip() for line in file)
        lines = list(line for line in lines if line)

    if length < len(lines[random_line_number]):
        random_string = lines[random_line_number][0:length]
    else:
        random_string = lines[random_line_number]
        for i in range(0,length-len(lines[random_line_number])):
            random_string = random_string + ' '
    return random_string

def generate_random_share(length):
    share = []
    for _ in range(length):
        share.append(random.randint(0, 127)) # ascii char/1 byte range
    return share

def generate_naive_secret_share(args):
    # TODO
    """
    With NAIVE approach, encode each secret separately. With m secrets and n
    shares per secret, requires m*n storage.
    :param args: 
    :return: 
    """

    pass

def generate_simple_secret_share(args):
    """
    With SIMPLE approach, encode m secrets with m + n - 1 shares. Generate n
    random shares, then generate m last shares to create m random secrets.
    :param args: 
    :return: 
    """
    # TODO
    pass

def generate_cyclic_secret_share(args):
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

    # print("Original secret:")
    # print(args.secret + "\n")

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
    
    # print("Recreated secret:")
    print(recreated_secret)

    rand_str = get_random_fake_secret(len(args.secret))
    print(rand_str)

    if args.NAIVE:
      generate_naive_secret_share(args)

    if args.SIMPLE:
        generate_simple_secret_share(args)

    if args.CYCLIC:
        generate_cyclic_secret_share(args)

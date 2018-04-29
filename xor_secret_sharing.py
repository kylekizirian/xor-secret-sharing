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

def convert_string_to_ascii(secret_string):
    secret_to_ascii = []
    for i in range(len(secret_string)):
        secret_to_ascii.append(ord(secret_string[i]))
    return secret_to_ascii

def convert_ascii_to_string(ascii_list):
    ascii_to_string = ""
    for ascii_val in ascii_list:
        ascii_to_string = ascii_to_string + chr(ascii_val)
    return ascii_to_string

def generate_naive_secret_share(args):
    """
    With NAIVE approach, encode each secret separately. With m secrets and n
    shares per secret, requires m*n storage.
    :param args: 
    :return: 
    """
    secret_string_length = len(args.secret)
    secret_list = []
    # plant m-1 fake secrets
    for _ in range(int(args.m) - 1):
        secret_list.append(get_random_fake_secret(secret_string_length))

    # secret_list is now length m, with m-1 fake secrets + real secret
    secret_list.append(args.secret)

    all_secret_shares = []
    for secret in secret_list:
        # generate n-1 random shares for each secret
        shares_for_one_secret = []
        for _ in range(int(args.n) - 1):
            shares_for_one_secret.append(generate_random_share(secret_string_length))

        secret_to_ascii = convert_string_to_ascii(secret)

        # XOR all shares together with secret to create last share which can
        # be used to recreate the secret
        last_share = []
        for i in range(secret_string_length):
            val = shares_for_one_secret[0][i]
            for j in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[j][i]
            val = val ^ secret_to_ascii[i]
            last_share.append(val)

        shares_for_one_secret.append(last_share)
        all_secret_shares.append(shares_for_one_secret)

    f = open(str(args.output), 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(len(args.secret)):
            val = shares_for_one_secret[0][i]
            for j in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[j][i]
            recreated_secret = recreated_secret + chr(val)

        for share in shares_for_one_secret:
            line = ""
            for value in share:
                line = line + str(value) + '\t'
            line = line + '\n'
            f.write(line)
        f.write(recreated_secret + "\n\n")

    storage_size = int(args.m) * int(args.n) * secret_string_length
    line = "Total storage size = " + str(storage_size) + " bytes"
    f.write(line)

    f.close()


def generate_simple_secret_share(args):
    """
    With SIMPLE approach, encode m secrets with m + n - 1 shares. Generate n
    random shares, then generate m last shares to create m random secrets.
    :param args: 
    :return: 
    """
    secret_string_length = len(args.secret)
    secret_list = []
    # plant m-1 fake secrets
    for _ in range(int(args.m) - 1):
        secret_list.append(get_random_fake_secret(secret_string_length))

    # secret_list is now length m, with m-1 fake secrets + real secret
    secret_list.append(args.secret)

    # generate n - 1 random shares, used by all secrets for SIMPLE
    random_shares = []
    for _ in range(int(args.n) - 1):
        random_shares.append(generate_random_share(secret_string_length))

    all_secret_shares = []
    for secret in secret_list:
        shares_for_one_secret = []
        shares_for_one_secret = shares_for_one_secret + random_shares

        secret_to_ascii = convert_string_to_ascii(secret)

        # XOR all shares together with secret to create last share which can
        # be used to recreate the secret
        last_share = []
        for i in range(secret_string_length):
            val = shares_for_one_secret[0][i]
            for j in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[j][i]
            val = val ^ secret_to_ascii[i]
            last_share.append(val)

        shares_for_one_secret.append(last_share)
        all_secret_shares.append(shares_for_one_secret)

    f = open(str(args.output), 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(len(args.secret)):
            val = shares_for_one_secret[0][i]
            for j in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[j][i]
            recreated_secret = recreated_secret + chr(val)

        # write to file
        for share in shares_for_one_secret:
            line = ""
            for value in share:
                line = line + str(value) + '\t'
            line = line + '\n'
            f.write(line)
        f.write(recreated_secret + "\n\n")

    storage_size = (int(args.m) + int(args.n)) * secret_string_length
    line = "Total storage size = " + str(storage_size) + " bytes"
    f.write(line)

    f.close()


def generate_cyclic_secret_share(args):
    """
    With CYCLIC approach, encode m secrets with n shares, reuse r random shares
    between each secret.
    :param args: 
    :return: 
    """
    secret_string_length = len(args.secret)
    secret_list = []
    # plant m-1 fake secrets
    for _ in range(int(args.m) - 1):
        secret_list.append(get_random_fake_secret(secret_string_length))

    # secret_list is now length m, with m-1 fake secrets + real secret
    secret_list.append(args.secret)

    all_secret_shares = []

    # for CYCLIC, generate n - 1 random shares for first secret
    shares_for_first_secret = []
    for _ in range(int(args.n) - 1):
        shares_for_first_secret.append(generate_random_share(secret_string_length))

    # XOR all shares together with secret to create last share which can
    # be used to recreate the secret
    secret_to_ascii = convert_string_to_ascii(secret_list[0])
    last_share = []
    for i in range(secret_string_length):
        val = shares_for_first_secret[0][i]
        for j in range(1, len(shares_for_first_secret)):
            val = val ^ shares_for_first_secret[j][i]
        val = val ^ secret_to_ascii[i]
        last_share.append(val)

    shares_for_first_secret.append(last_share)
    all_secret_shares.append(shares_for_first_secret)

    # loop to generate the 2nd through 2nd to last secrets shares
    for i in range(1, len(secret_list) - 1):
        secret = secret_list[i]

        # reuse with the last r shares from previous secret
        shares_for_one_secret = []
        for j in range(int(args.r), 0, -1):
            shares_for_one_secret.append(all_secret_shares[i-1][(j)*-1])

        # create n - r - 1 random shares
        for j in range(int(args.n) - int(args.r) - 1):
            shares_for_one_secret.append(generate_random_share(secret_string_length))

        # XOR all shares together with secret to create last share which can
        # be used to recreate the secret
        secret_to_ascii = convert_string_to_ascii(secret)
        last_share = []
        for j in range(secret_string_length):
            val = shares_for_one_secret[0][j]
            for k in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[k][j]
            val = val ^ secret_to_ascii[j]
            last_share.append(val)

        shares_for_one_secret.append(last_share)
        all_secret_shares.append(shares_for_one_secret)


    # handle generating shares for last secret separately
    shares_for_last_secret = []

    # reuse with the last r shares from previous secret
    for j in range(int(args.r), 0, -1):
        shares_for_last_secret.append(all_secret_shares[-1][(j) * -1])

    # reuse first r shares from first secret
    for j in range(int(args.r)):
        shares_for_last_secret.append(all_secret_shares[0][j])

    # add n - 2*r - 1 random shares
    for j in range(int(args.n) - (2 * int(args.r)) - 1):
        shares_for_last_secret.append(generate_random_share(secret_string_length))

    # XOR all shares together with secret to create last share which can
    # be used to recreate the secret
    secret_to_ascii = convert_string_to_ascii(secret_list[-1])
    last_share = []
    for j in range(secret_string_length):
        val = shares_for_last_secret[0][j]
        for k in range(1, len(shares_for_last_secret)):
            val = val ^ shares_for_last_secret[k][j]
        val = val ^ secret_to_ascii[j]
        last_share.append(val)

    shares_for_last_secret.append(last_share)
    all_secret_shares.append(shares_for_last_secret)

    f = open(str(args.output), 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(len(args.secret)):
            val = shares_for_one_secret[0][i]
            for j in range(1, len(shares_for_one_secret)):
                val = val ^ shares_for_one_secret[j][i]
            recreated_secret = recreated_secret + chr(val)

        for share in shares_for_one_secret:
            line = ""
            for value in share:
                line = line + str(value) + '\t'
            line = line + '\n'
            f.write(line)
        f.write(recreated_secret + "\n\n")

    storage_size = (int(args.m) * (int(args.n) - int(args.r))) * secret_string_length
    line = "Total storage size = " + str(storage_size) + " bytes"
    f.write(line)

    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XOR secret sharing parameters')
    parser.add_argument('--secret', help="Your secret string", required=True)
    parser.add_argument('--output', help="Text file to write output to", required=True)
    parser.add_argument('--n', help="Number of shares per secret", required=True)
    parser.add_argument('--m', help="Number of fake secrets", required=True)
    parser.add_argument('--r', help="Overlap in Cyclic approach")

    secret_approach = parser.add_mutually_exclusive_group(required=True)
    secret_approach.add_argument('--NAIVE', help="NAIVE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--SIMPLE', help="SIMPLE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--CYCLIC', help="CYCLIC approach to deceptive secret sharing", action='store_true')

    args = parser.parse_args()

    if args.CYCLIC and not args.r:
        raise Exception('Must provide --r argument for CYCLIC approach!')

    if args.CYCLIC and (int(args.r) > int(args.n)/2):
        raise Exception('Value for --r argument is too large!')

    if args.NAIVE:
      generate_naive_secret_share(args)

    if args.SIMPLE:
        generate_simple_secret_share(args)

    if args.CYCLIC:
        generate_cyclic_secret_share(args)

import argparse
import os
import random

def get_secret_list(secret, m):
    def get_one_fake_secret(length):
        random_line_number = random.randint(124, 5000)
        file_path = os.path.join(os.curdir, "Frankenstein", "Frankenstein.txt")

        with open(file_path) as file:
            lines = [line.rstrip() for line in file if line.rstrip()]

        if length < len(lines[random_line_number]):
            random_string = lines[random_line_number][0:length]
        else:
            random_string = lines[random_line_number]
            for i in range(0, length-len(lines[random_line_number])):
                random_string = random_string + ' '
        return random_string

    return [get_one_fake_secret(len(secret)) for _ in range(m-1)] + [secret]

def generate_random_shares(share_length, num_shares=1):
    return [[random.randint(0, 127)
        for _ in range(share_length)]
        for _ in range(num_shares)]

def convert_string_to_ascii(secret_string):
    return [ord(c) for c in secret_string]

def convert_ascii_to_string(ascii_list):
    return ''.join(map(chr, ascii_list))

# elementwise XORs a list of (lists of ints with the same length)
def XOR_all(xs):
    result = list(xs[0])
    for i in range(1, len(xs)):
        for j in range(len(result)):
            result[j] ^= xs[i][j]
    return result

def generate_naive_secret_share(secret, n, m, output="out"):
    """
    With NAIVE approach, encode each secret separately. With m secrets and n
    shares per secret, requires m*n storage.
    :param args: 
    :return: 
    """
    secret_length = len(secret)
    secret_list = get_secret_list(secret, m)
    # secret_list is now length m, with m-1 fake secrets + real secret

    all_secret_shares = []
    for secret in secret_list:
        # generate n-1 random shares for each secret
        shares_for_one_secret = generate_random_shares(
                secret_length, n - 1)

        # XOR all shares together with secret to create last share which can
        # be used to recreate the secret
        last_share = XOR_all(shares_for_one_secret +
                [convert_string_to_ascii(secret)])

        shares_for_one_secret.append(last_share)
        all_secret_shares.append(shares_for_one_secret)

    f = open(output, 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(secret_length):
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

    storage_size = m * n * secret_length
    line = "Total storage size = " + str(storage_size) + " bytes"
    f.write(line)

    f.close()


def generate_simple_secret_share(secret, n, m, output="out"):
    """
    With SIMPLE approach, encode m secrets with m + n - 1 shares. Generate n
    random shares, then generate m last shares to create m random secrets.
    :param args: 
    :return: 
    """
    secret_length = len(secret)
    secret_list = get_secret_list(secret, m)

    # secret_list is now length m, with m-1 fake secrets + real secret
    secret_list.append(secret)

    # generate n - 1 random shares, used by all secrets for SIMPLE
    random_shares = generate_random_shares(
            secret_length, n - 1)

    all_secret_shares = []
    for secret in secret_list:
        shares_for_one_secret = []
        shares_for_one_secret = shares_for_one_secret + random_shares

        # XOR all shares together with secret to create last share which can
        # be used to recreate the secret
        last_share = XOR_all(shares_for_one_secret +
                [convert_string_to_ascii(secret)])

        shares_for_one_secret.append(last_share)
        all_secret_shares.append(shares_for_one_secret)

    f = open(output, 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(secret_length):
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

    storage_size = (m + n) * secret_length
    line = "Total storage size = " + str(storage_size) + " bytes"
    f.write(line)

    f.close()


def generate_cyclic_secret_share(secret, n, m, r):
    """
    With CYCLIC approach, encode m secrets with n shares, reuse r random shares
    between each secret.
    :param args: 
    :return: 
    """
    secret_length = len(secret)
    secret_list = list(map(convert_string_to_ascii,get_secret_list(secret, m)))
    # secret_list is now length m, with m-1 fake secrets + real secret

    all_secret_shares = []

    num_shares = (n-r) * m
    shares = [None] * num_shares
    shares[0:r] = generate_random_shares(secret_length, r)
    for i in range(m): # for all secrets
        off_the_circle = False
        last_share_index = n-1
        for j in range(r, n): # for all shares after the first overlapped ones
            if not shares[(i*(n-r)+j) % num_shares]: # if the share hasn't been created already
                shares[(i*(n-r)+j) % num_shares] = generate_random_shares(secret_length)[0]
            elif j == r: # if there were no open shares to begin with then make one "off the circle"
                off_the_circle = True
                break
            else: # make the previous share the one we generate for the secret
                last_share_index = j-1
                break
        last_share = secret_list[i]
        shares_for_this_secret = []
        for j in range(n):
            if j != last_share_index:
                last_share = XOR_all(
                        [last_share, shares[(i*(n-r)+j) % num_shares]])
                shares_for_this_secret.append(
                        shares[(i*(n-r)+j) % num_shares])
        if not off_the_circle:
            shares[(i*(n-r)+last_share_index)] = last_share
        shares_for_this_secret.append(last_share)
        all_secret_shares.append(shares_for_this_secret)
            
    f = open(output, 'w+')

    # recreate secret by XOR-ing all shares together to verify correctness
    for shares_for_one_secret in all_secret_shares:
        recreated_secret = ""
        for i in range(secret_length):
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

    storage_size = m * (n - r) * secret_length
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

    secret = args.secret
    output = args.output
    n = int(args.n)
    m = int(args.m)

    if args.CYCLIC:
        if not args.r:
            raise Exception('Must provide --r argument for CYCLIC approach!')
        else:
            generate_cyclic_secret_share(secret, n, m, int(args.r))

    if args.NAIVE:
        generate_naive_secret_share(secret, n, m)

    if args.SIMPLE:
        generate_simple_secret_share(secret, n, m)

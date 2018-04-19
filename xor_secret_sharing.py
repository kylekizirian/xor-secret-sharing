import argparse

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

    if args.NAIVE:
      generate_naive_secret_share()

    if args.SIMPLE:
        generate_simple_secret_share()

    if args.CYCLIC:
        generate_cyclic_secret_share()
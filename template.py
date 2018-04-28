import argparse

def generate_naive_secret_share(args):
    # TODO
    pass

def generate_simple_secret_share(args):
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
    parser.add_argument('--r', help="Overlap in Cyclic approach")

    secret_approach = parser.add_mutually_exclusive_group(required=True)
    secret_approach.add_argument('--NAIVE', help="NAIVE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--SIMPLE', help="SIMPLE approach to deceptive secret sharing", action='store_true')
    secret_approach.add_argument('--CYCLIC', help="CYCLIC approach to deceptive secret sharing", action='store_true')

    args = parser.parse_args()

    if args.CYCLIC and not args.r:
        raise Exception('Must provide --r argument for CYCLIC approach!')

    if args.CYCLIC and (int(args.r) > int(args.m) - 1):
        raise Exception('Value for --r argument is too large!')

    if args.NAIVE:
      generate_naive_secret_share(args)

    if args.SIMPLE:
        generate_simple_secret_share(args)

    if args.CYCLIC:
        generate_cyclic_secret_share(args)
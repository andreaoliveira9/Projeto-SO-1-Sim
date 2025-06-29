import argparse
import random
import config
from simulate import simulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="Seed para aleatoriedade")
    parser.add_argument(
        "--verbose", action="store_true", help="Ativa o modo verboso de saída"
    )
    parser.add_argument(
        "--serversA", type=int, default=2, help="Número de servidores do tipo A"
    )
    parser.add_argument(
        "--serversB", type=int, default=1, help="Número de servidores do tipo B"
    )
    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)
    if args.verbose:
        config.VERBOSE = True

    config.NUM_SERVERS_A = args.serversA
    config.NUM_SERVERS_B = args.serversB

    simulate()

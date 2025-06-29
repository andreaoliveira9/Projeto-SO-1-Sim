import argparse
import config
from euler import simulate_euler
from rk4 import simulate_rk4
from plotting import plot_comparison, plot_single

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--x0", type=float, default=config.X0)
    parser.add_argument("--y0", type=float, default=config.Y0)
    parser.add_argument("--alpha", type=float, default=config.ALPHA)
    parser.add_argument("--beta", type=float, default=config.BETA)
    parser.add_argument("--delta", type=float, default=config.DELTA)
    parser.add_argument("--gamma", type=float, default=config.GAMMA)
    parser.add_argument("--dt", type=float, default=config.DT)
    parser.add_argument("--tfinal", type=float, default=config.T_FINAL)
    parser.add_argument(
        "--method",
        choices=["euler", "rk4"],
        default=config.METHOD,
        help="Integration method",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare Euler and RK4 methods on the same plot",
    )
    args = parser.parse_args()

    if args.compare:
        times_e, xs_e, ys_e = simulate_euler(
            args.x0, args.y0, args.alpha, args.beta,
            args.delta, args.gamma, args.dt, args.tfinal
        )
        times_rk, xs_rk, ys_rk = simulate_rk4(
            args.x0, args.y0, args.alpha, args.beta,
            args.delta, args.gamma, args.dt, args.tfinal
        )
        plot_comparison(times_e, xs_e, ys_e, times_rk, xs_rk, ys_rk, args.dt)
    else:
        if args.method == "euler":
            times, xs, ys = simulate_euler(
                args.x0, args.y0, args.alpha, args.beta,
                args.delta, args.gamma, args.dt, args.tfinal
            )
        else:
            times, xs, ys = simulate_rk4(
                args.x0, args.y0, args.alpha, args.beta,
                args.delta, args.gamma, args.dt, args.tfinal
            )
        plot_single(times, xs, ys, args.method, args.dt)

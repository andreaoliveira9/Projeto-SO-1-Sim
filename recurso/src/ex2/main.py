import argparse
import config
import os
from methods import simulate
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
    )
    parser.add_argument(
        "--compare",
        action="store_true",
    )
    parser.add_argument("--save_path", type=str, default=config.SAVE_PATH)
    args = parser.parse_args()

    if args.save_path:
        if not os.path.exists(args.save_path):
            os.makedirs(args.save_path)

    if args.compare:
        times_e, xs_e, ys_e = simulate(
            args.x0,
            args.y0,
            args.alpha,
            args.beta,
            args.delta,
            args.gamma,
            args.dt,
            args.tfinal,
            "euler",
        )
        times_rk, xs_rk, ys_rk = simulate(
            args.x0,
            args.y0,
            args.alpha,
            args.beta,
            args.delta,
            args.gamma,
            args.dt,
            args.tfinal,
            "rk4",
        )
        plot_comparison(
            times_e, xs_e, ys_e, times_rk, xs_rk, ys_rk, args.dt, args.save_path
        )
    else:
        times, xs, ys = simulate(
            args.x0,
            args.y0,
            args.alpha,
            args.beta,
            args.delta,
            args.gamma,
            args.dt,
            args.tfinal,
            args.method,
        )
        plot_single(times, xs, ys, args.method, args.dt, args.save_path)

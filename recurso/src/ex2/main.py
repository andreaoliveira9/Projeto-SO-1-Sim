import argparse
import config
import os
from methods import simulate
from plotting import plot_comparison, plot_single


def compute_euler(x0, y0, alpha, beta, delta, gamma, dt, tfinal):
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

    return times_e, xs_e, ys_e


def compute_rk4(x0, y0, alpha, beta, delta, gamma, dt, tfinal):
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

    return times_rk, xs_rk, ys_rk


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
        times_e, xs_e, ys_e = compute_euler(
            args.x0,
            args.y0,
            args.alpha,
            args.beta,
            args.delta,
            args.gamma,
            args.dt,
            args.tfinal,
        )
        times_rk, xs_rk, ys_rk = compute_rk4(
            args.x0,
            args.y0,
            args.alpha,
            args.beta,
            args.delta,
            args.gamma,
            args.dt,
            args.tfinal,
        )
        plot_comparison(
            times_e, xs_e, ys_e, times_rk, xs_rk, ys_rk, args.dt, args.save_path
        )
    else:
        if args.method == "euler":
            times, xs, ys = compute_euler(
                args.x0,
                args.y0,
                args.alpha,
                args.beta,
                args.delta,
                args.gamma,
                args.dt,
                args.tfinal,
            )
        elif args.method == "rk4":
            times, xs, ys = compute_rk4(
                args.x0,
                args.y0,
                args.alpha,
                args.beta,
                args.delta,
                args.gamma,
                args.dt,
                args.tfinal,
            )

        plot_single(times, xs, ys, args.method, args.dt, args.save_path)

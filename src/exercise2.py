import numpy as np
import matplotlib.pyplot as plt
import argparse

# Execution examples:
# python exercise2.py --method rk4 --x0 0 --y0 0 --vx0 50 --vy0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81
# python exercise2.py --method euler --x0 0 --y0 0 --vx0 50 --vy0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81
# python exercise2.py --compare --x0 0 --y0 0 --vx0 50 --vy0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81


class Simulation:
    """Class to simulate the projectile motion under air resistance."""

    def __init__(self, x0, y0, vx0, vy0, dt, t_final, mass, gravity, drag):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0
        self.dt = dt
        self.t_final = t_final
        self.mass = mass
        self.gravity = gravity
        self.drag = drag
        self.reset_state()

    def reset_state(self):
        """Reset the simulation state to the initial conditions."""
        self.x = self.x0
        self.y = self.y0
        self.vx = self.vx0
        self.vy = self.vy0
        self.t = 0.0
        self.t_history = [self.t]
        self.x_history = [self.x]
        self.y_history = [self.y]
        self.vx_history = [self.vx]
        self.vy_history = [self.vy]

    def observe(self):
        """Record the current state and increment time."""
        self.t += self.dt
        self.t_history.append(self.t)
        self.x_history.append(self.x)
        self.y_history.append(self.y)
        self.vx_history.append(self.vx)
        self.vy_history.append(self.vy)

    def update_euler(self):
        """Update the state using the Euler integration method."""
        ax = -(self.drag / self.mass) * self.vx * abs(self.vx)
        ay = -self.gravity - (self.drag / self.mass) * self.vy * abs(self.vy)
        self.x += self.dt * self.vx
        self.vx += self.dt * ax
        self.y += self.dt * self.vy
        self.vy += self.dt * ay

    def update_rk4(self):
        """Update the state using the fourth-order Runge-Kutta method."""
        state = np.array([self.x, self.y, self.vx, self.vy])

        def f(state):
            x, y, vx, vy = state
            ax = -(self.drag / self.mass) * vx * abs(vx)
            ay = -self.gravity - (self.drag / self.mass) * vy * abs(vy)
            return np.array([vx, vy, ax, ay])

        dt = self.dt
        k1 = f(state)
        k2 = f(state + 0.5 * dt * k1)
        k3 = f(state + 0.5 * dt * k2)
        k4 = f(state + dt * k3)
        state_next = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        self.x, self.y, self.vx, self.vy = state_next

    def run_simulation(self, method):
        """Run the simulation using the specified integration method.

        Args:
            method (str): The integration method ('euler' or 'rk4').

        Returns:
            tuple: Histories of time, x, y, vx, and vy.
        """
        self.reset_state()
        num_steps = int(self.t_final / self.dt)
        for _ in range(num_steps):
            if method.lower() == "euler":
                self.update_euler()
            elif method.lower() == "rk4":
                self.update_rk4()
            else:
                raise ValueError(f"Unknown method: {method}")
            self.observe()
        return (
            self.t_history,
            self.x_history,
            self.y_history,
            self.vx_history,
            self.vy_history,
        )


def generate_comparison_plots(
    t_euler, x_euler, y_euler, vx_euler, vy_euler, t_rk4, x_rk4, y_rk4, vx_rk4, vy_rk4
):
    """Generate plots to compare Euler and RK4 integration methods."""
    fig = plt.figure(constrained_layout=True, figsize=(12, 10))
    gs = fig.add_gridspec(3, 2)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_euler, x_euler, label="x (Euler)")
    ax1.plot(t_rk4, x_rk4, label="x (RK4)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position x (m)")
    ax1.set_title("Comparison of x(t)")
    ax1.legend()

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t_euler, vx_euler, label="vx (Euler)")
    ax2.plot(t_rk4, vx_rk4, label="vx (RK4)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity vx (m/s)")
    ax2.set_title("Comparison of vx(t)")
    ax2.legend()

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t_euler, y_euler, label="y (Euler)")
    ax3.plot(t_rk4, y_rk4, label="y (RK4)")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Position y (m)")
    ax3.set_title("Comparison of y(t)")
    ax3.legend()

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(t_euler, vy_euler, label="vy (Euler)")
    ax4.plot(t_rk4, vy_rk4, label="vy (RK4)")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Velocity vy (m/s)")
    ax4.set_title("Comparison of vy(t)")
    ax4.legend()

    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot(x_euler, y_euler, label="Trajectory (Euler)")
    ax5.plot(x_rk4, y_rk4, label="Trajectory (RK4)")
    ax5.set_xlabel("Position x (m)")
    ax5.set_ylabel("Position y (m)")
    ax5.set_title("Comparison of Trajectories")
    ax5.legend()

    plt.show()


def generate_single_method_plots(t, x, y, vx, vy):
    """Generate plots for a single integration method."""
    fig = plt.figure(constrained_layout=True, figsize=(12, 10))
    gs = fig.add_gridspec(3, 2)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t, x, label="x(t)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position x (m)")
    ax1.set_title("Position x over Time")
    ax1.legend()

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t, vx, label="vx(t)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity vx (m/s)")
    ax2.set_title("Velocity vx over Time")
    ax2.legend()

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t, y, label="y(t)")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Position y (m)")
    ax3.set_title("Position y over Time")
    ax3.legend()

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(t, vy, label="vy(t)")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Velocity vy (m/s)")
    ax4.set_title("Velocity vy over Time")
    ax4.legend()

    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot(x, y, label="Trajectory")
    ax5.set_xlabel("Position x (m)")
    ax5.set_ylabel("Position y (m)")
    ax5.set_title("Projectile Trajectory")
    ax5.legend()

    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Simulation of a projectile under air resistance"
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["euler", "rk4"],
        default="euler",
        help="Integration method: euler or rk4",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run both methods and compare the results",
    )
    parser.add_argument("--x0", type=float, default=0.0, help="Initial x position")
    parser.add_argument("--y0", type=float, default=0.0, help="Initial y position")
    parser.add_argument("--vx0", type=float, default=50.0, help="Initial x velocity")
    parser.add_argument("--vy0", type=float, default=50.0, help="Initial y velocity")
    parser.add_argument(
        "--drag",
        type=float,
        default=0.1,
        help="Air resistance coefficient",
    )
    parser.add_argument("--dt", type=float, default=0.01, help="Time step (Δt)")
    parser.add_argument(
        "--tfinal",
        type=float,
        default=10.0,
        help="Final simulation time",
    )
    parser.add_argument(
        "--mass", type=float, default=1.0, help="Mass of the projectile"
    )
    parser.add_argument(
        "--gravity",
        type=float,
        default=9.81,
        help="Gravitational acceleration",
    )

    args = parser.parse_args()

    # Create a simulation instance with the provided parameters
    sim = Simulation(
        args.x0,
        args.y0,
        args.vx0,
        args.vy0,
        args.dt,
        args.tfinal,
        args.mass,
        args.gravity,
        args.drag,
    )

    if args.compare:
        # Run simulation using Euler method
        t_euler, x_euler, y_euler, vx_euler, vy_euler = sim.run_simulation("euler")
        # Run simulation using RK4 method
        t_rk4, x_rk4, y_rk4, vx_rk4, vy_rk4 = sim.run_simulation("rk4")
        generate_comparison_plots(
            t_euler,
            x_euler,
            y_euler,
            vx_euler,
            vy_euler,
            t_rk4,
            x_rk4,
            y_rk4,
            vx_rk4,
            vy_rk4,
        )
    else:
        t_history, x_history, y_history, vx_history, vy_history = sim.run_simulation(
            args.method
        )
        generate_single_method_plots(
            t_history, x_history, y_history, vx_history, vy_history
        )


if __name__ == "__main__":
    main()

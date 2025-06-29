import numpy as np
import matplotlib.pyplot as plt
import argparse
from typing import List, Tuple


class Simulation:
    """
    Class to simulate the projectile motion under air resistance using numerical integration.

    Attributes:
        x0 (float): Initial x position.
        z0 (float): Initial z position.
        vx0 (float): Initial x velocity.
        vz0 (float): Initial z velocity.
        dt (float): Time step.
        t_final (float): Final simulation time.
        mass (float): Mass of the projectile.
        gravity (float): Gravitational acceleration.
        drag (float): Air resistance coefficient.
    """

    def __init__(
        self,
        x0: float,
        z0: float,
        vx0: float,
        vz0: float,
        dt: float,
        t_final: float,
        mass: float,
        gravity: float,
        drag: float,
    ) -> None:
        self.x0: float = x0
        self.z0: float = z0
        self.vx0: float = vx0
        self.vz0: float = vz0
        self.dt: float = dt
        self.t_final: float = t_final
        self.mass: float = mass
        self.gravity: float = gravity
        self.drag: float = drag
        self.initialize()

    def initialize(self) -> None:
        """Reset the simulation state to the initial conditions."""
        self.x: float = self.x0
        self.z: float = self.z0
        self.vx: float = self.vx0
        self.vz: float = self.vz0
        self.t: float = 0.0

        self.t_history: List[float] = [self.t]
        self.x_history: List[float] = [self.x]
        self.z_history: List[float] = [self.z]
        self.vx_history: List[float] = [self.vx]
        self.vz_history: List[float] = [self.vz]

    def observe(self) -> None:
        """
        Record the current state of the simulation and increment time by dt.
        """
        self.t += self.dt
        self.t_history.append(self.t)
        self.x_history.append(self.x)
        self.z_history.append(self.z)
        self.vx_history.append(self.vx)
        self.vz_history.append(self.vz)

    def update_euler(self) -> None:
        """
        Update the simulation state using the Euler integration method.
        """
        ax: float = -(self.drag / self.mass) * self.vx * abs(self.vx)
        az: float = -self.gravity - (self.drag / self.mass) * self.vz * abs(self.vz)
        self.x += self.dt * self.vx
        self.vx += self.dt * ax
        self.z += self.dt * self.vz
        self.vz += self.dt * az

    def update_rk4(self) -> None:
        """
        Update the simulation state using the fourth-order Runge-Kutta (RK4) method.
        """
        state: np.ndarray = np.array([self.x, self.z, self.vx, self.vz])

        def f(state: np.ndarray) -> np.ndarray:
            """
            Compute the derivatives of the state.

            Args:
                state (np.ndarray): Array containing [x, z, vx, vz].

            Returns:
                np.ndarray: Derivatives [vx, vz, ax, az].
            """
            x, z, vx, vz = state
            ax: float = -(self.drag / self.mass) * vx * abs(vx)
            az: float = -self.gravity - (self.drag / self.mass) * vz * abs(vz)
            return np.array([vx, vz, ax, az])

        dt: float = self.dt
        k1: np.ndarray = f(state)
        k2: np.ndarray = f(state + 0.5 * dt * k1)
        k3: np.ndarray = f(state + 0.5 * dt * k2)
        k4: np.ndarray = f(state + dt * k3)
        state_next: np.ndarray = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        self.x, self.z, self.vx, self.vz = state_next

    def run_simulation(
        self, method: str
    ) -> Tuple[List[float], List[float], List[float], List[float], List[float]]:
        """
        Run the simulation using the specified integration method.

        Args:
            method (str): Integration method ('euler' or 'rk4').

        Returns:
            Tuple containing histories: time, x, z, vx, and vz.
        """
        self.initialize()
        num_steps: int = int(self.t_final / self.dt)

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
            self.z_history,
            self.vx_history,
            self.vz_history,
        )


def generate_comparison_plots(
    t_euler: List[float],
    x_euler: List[float],
    z_euler: List[float],
    vx_euler: List[float],
    vz_euler: List[float],
    t_rk4: List[float],
    x_rk4: List[float],
    z_rk4: List[float],
    vx_rk4: List[float],
    vz_rk4: List[float],
    dt: float,
) -> None:
    """
    Generate plots to compare the Euler and RK4 integration methods.

    Args:
        t_euler, x_euler, z_euler, vx_euler, vz_euler (List[float]): Histories from Euler method.
        t_rk4, x_rk4, z_rk4, vx_rk4, vz_rk4 (List[float]): Histories from RK4 method.
    """
    fig = plt.figure(constrained_layout=True, figsize=(12, 10))
    fig.suptitle(f"Comparison of Euler and RK4 methods (dt = {dt}s)", fontsize=16)
    gs = fig.add_gridspec(3, 2)

    # Plot for x(t)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_euler, x_euler, label="Euler")
    ax1.plot(t_rk4, x_rk4, label="RK4")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position x (m)")
    ax1.set_title("Position x over Time")
    ax1.legend()

    # Plot for vx(t)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t_euler, vx_euler, label="Euler")
    ax2.plot(t_rk4, vx_rk4, label="RK4")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity x (m/s)")
    ax2.set_title("Velocity x over Time")
    ax2.legend()

    # Plot for z(t)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t_euler, z_euler, label="Euler")
    ax3.plot(t_rk4, z_rk4, label="RK4")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Position z (m)")
    ax3.set_title("Position z over Time")
    ax3.legend()

    # Plot for vz(t)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(t_euler, vz_euler, label="Euler")
    ax4.plot(t_rk4, vz_rk4, label="RK4")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Velocity z (m/s)")
    ax4.set_title("Velocity z over Time")
    ax4.legend()

    # Trajectory plot
    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot(x_euler, z_euler, label="Euler")
    ax5.plot(x_rk4, z_rk4, label="RK4")
    ax5.set_xlabel("Position x (m)")
    ax5.set_ylabel("Position z (m)")
    ax5.set_title("Projectile Trajectory")
    ax5.legend()

    plt.show()


def generate_single_method_plots(
    t: List[float],
    x: List[float],
    z: List[float],
    vx: List[float],
    vz: List[float],
    dt: float,
    method: str,
) -> None:
    """
    Generate plots for a single integration method.

    Args:
        t, x, z, vx, vz (List[float]): Histories of time, x, z, vx, and vz.
    """
    fig = plt.figure(constrained_layout=True, figsize=(12, 10))
    fig.suptitle(
        f"Projectile Motion using {method.upper()} method (dt = {dt}s)", fontsize=16
    )
    gs = fig.add_gridspec(3, 2)

    # Plot for x(t)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t, x)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position x (m)")
    ax1.set_title("Position x over Time")

    # Plot for vx(t)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t, vx)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity x (m/s)")
    ax2.set_title("Velocity x over Time")

    # Plot for z(t)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t, z)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Position z (m)")
    ax3.set_title("Position z over Time")

    # Plot for vz(t)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(t, vz)
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Velocity z (m/s)")
    ax4.set_title("Velocity z over Time")

    # Trajectory plot
    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot(x, z)
    ax5.set_xlabel("Position x (m)")
    ax5.set_ylabel("Position z (m)")
    ax5.set_title("Projectile Trajectory")

    plt.show()


def main() -> None:
    """
    Parse command line arguments and execute the simulation.
    """
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
    parser.add_argument("--z0", type=float, default=0.0, help="Initial z position")
    parser.add_argument("--vx0", type=float, default=50.0, help="Initial x velocity")
    parser.add_argument("--vz0", type=float, default=50.0, help="Initial z velocity")
    parser.add_argument(
        "--drag", type=float, default=0.1, help="Air resistance coefficient"
    )
    parser.add_argument("--dt", type=float, default=0.01, help="Time step (Δt)")
    parser.add_argument(
        "--tfinal", type=float, default=10.0, help="Final simulation time"
    )
    parser.add_argument(
        "--mass", type=float, default=1.0, help="Mass of the projectile"
    )
    parser.add_argument(
        "--gravity", type=float, default=9.81, help="Gravitational acceleration"
    )

    args = parser.parse_args()

    # Create a simulation instance with the provided parameters
    sim = Simulation(
        args.x0,
        args.z0,
        args.vx0,
        args.vz0,
        args.dt,
        args.tfinal,
        args.mass,
        args.gravity,
        args.drag,
    )

    if args.compare:
        # Run simulation using both Euler and RK4 methods
        t_euler, x_euler, z_euler, vx_euler, vz_euler = sim.run_simulation("euler")
        t_rk4, x_rk4, z_rk4, vx_rk4, vz_rk4 = sim.run_simulation("rk4")
        generate_comparison_plots(
            t_euler,
            x_euler,
            z_euler,
            vx_euler,
            vz_euler,
            t_rk4,
            x_rk4,
            z_rk4,
            vx_rk4,
            vz_rk4,
            args.dt,
        )
    else:
        t_history, x_history, z_history, vx_history, vz_history = sim.run_simulation(
            args.method
        )
        generate_single_method_plots(
            t_history,
            x_history,
            z_history,
            vx_history,
            vz_history,
            args.dt,
            args.method,
        )


if __name__ == "__main__":
    main()

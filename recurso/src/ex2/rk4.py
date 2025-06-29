def initialize(x0, y0):
    """Initialize simulation state."""
    t = 0.0
    times = [t]
    xs = [x0]
    ys = [y0]
    return t, x0, y0, times, xs, ys


def observe(t, x, y, times, xs, ys):
    """Record state into time series."""
    times.append(t)
    xs.append(x)
    ys.append(y)


def rk4_step(x, y, alpha, beta, delta, gamma, dt):
    """Perform a single RK4 update step."""

    def dx(x, y, alpha, beta):
        """Compute dx/dt for Lotka-Volterra."""
        return alpha * x - beta * x * y

    def dy(x, y, delta, gamma):
        """Compute dy/dt for Lotka-Volterra."""
        return delta * x * y - gamma * y

    k1x = dx(x, y, alpha, beta)
    k1y = dy(x, y, delta, gamma)

    k2x = dx(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, alpha, beta)
    k2y = dy(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, delta, gamma)

    k3x = dx(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, alpha, beta)
    k3y = dy(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, delta, gamma)

    k4x = dx(x + dt * k3x, y + dt * k3y, alpha, beta)
    k4y = dy(x + dt * k3x, y + dt * k3y, delta, gamma)

    x_new = x + (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
    y_new = y + (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)

    return x_new, y_new


def simulate_rk4(x0, y0, alpha, beta, delta, gamma, dt, t_final):
    """
    Simulates the Lotka-Volterra system using the Runge-Kutta 4th order method.
    """
    t, x, y, times, xs, ys = initialize(x0, y0)

    while t < t_final:
        x, y = rk4_step(x, y, alpha, beta, delta, gamma, dt)
        t += dt
        observe(t, x, y, times, xs, ys)

    return times, xs, ys

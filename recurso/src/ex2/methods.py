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


def dx(x, y, alpha, beta):
    """Compute dx/dt for Lotka-Volterra."""
    return alpha * x - beta * x * y


def dy(x, y, delta, gamma):
    """Compute dy/dt for Lotka-Volterra."""
    return delta * x * y - gamma * y


def update_euler(x, y, alpha, beta, delta, gamma, dt):
    """Computes the next state using the Euler method."""
    x_new = x + dx(x, y, alpha, beta) * dt
    y_new = y + dy(x, y, delta, gamma) * dt
    return x_new, y_new


def update_rk4(x, y, alpha, beta, delta, gamma, dt):
    """Perform a single RK4 update step."""
    k1x = dt * dx(x, y, alpha, beta)
    k1y = dt * dy(x, y, delta, gamma)

    k2x = dt * dx(x + k1x / 2, y + k1y / 2, alpha, beta)
    k2y = dt * dy(x + k1x / 2, y + k1y / 2, delta, gamma)

    k3x = dt * dx(x + k2x / 2, y + k2y / 2, alpha, beta)
    k3y = dt * dy(x + k2x / 2, y + k2y / 2, delta, gamma)

    k4x = dt * dx(x + k3x, y + k3y, alpha, beta)
    k4y = dt * dy(x + k3x, y + k3y, delta, gamma)

    x_new = x + (k1x + 2 * k2x + 2 * k3x + k4x) / 6
    y_new = y + (k1y + 2 * k2y + 2 * k3y + k4y) / 6

    return x_new, y_new


def simulate(x0, y0, alpha, beta, delta, gamma, dt, t_final, method):
    """
    Simulates the Lotka-Volterra system using the specified method.
    
    method: "euler" or "rk4"
    """
    t, x, y, times, xs, ys = initialize(x0, y0)

    while t < t_final:
        if method == "euler":
            x, y = update_euler(x, y, alpha, beta, delta, gamma, dt)
        elif method == "rk4":
            x, y = update_rk4(x, y, alpha, beta, delta, gamma, dt)
        else:
            raise ValueError("Método inválido. Use 'euler' ou 'rk4'.")
        t += dt
        observe(t, x, y, times, xs, ys)

    return times, xs, ys
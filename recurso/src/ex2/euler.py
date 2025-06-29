import config


def initialize(x0, y0):
    """
    Initializes the simulation state and result lists.
    """
    t = 0.0
    times = [t]
    xs = [x0]
    ys = [y0]
    return t, x0, y0, times, xs, ys


def update(x, y, alpha, beta, delta, gamma, dt):
    """
    Computes the next state using the Euler update.
    """
    dx = alpha * x - beta * x * y
    dy = delta * x * y - gamma * y
    x_new = x + dx * dt
    y_new = y + dy * dt
    return x_new, y_new


def observe(t, x, y, times, xs, ys):
    """
    Records the current state into the result lists.
    """
    times.append(t)
    xs.append(x)
    ys.append(y)


def simulate_euler(x0, y0, alpha, beta, delta, gamma, dt, t_final):
    """
    Simulates the Lotka-Volterra system using the Forward Euler method.

    Parameters:
    - x0, y0: Initial populations of prey and predators
    - alpha, beta, delta, gamma: Model parameters
    - dt: Time step size
    - t_final: Total simulation time

    Returns:
    - times: List of time values
    - xs: List of prey population over time
    - ys: List of predator population over time
    """
    t, x, y, times, xs, ys = initialize(x0, y0)

    while t < t_final:
        x, y = update(x, y, alpha, beta, delta, gamma, dt)
        t += dt
        observe(t, x, y, times, xs, ys)

    return times, xs, ys

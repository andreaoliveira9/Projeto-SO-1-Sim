import config


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
    t = 0.0
    x, y = x0, y0
    times = [t]
    xs = [x]
    ys = [y]

    while t < t_final:
        dx = alpha * x - beta * x * y
        dy = delta * x * y - gamma * y
        x += dx * dt
        y += dy * dt
        t += dt
        times.append(t)
        xs.append(x)
        ys.append(y)

    return times, xs, ys

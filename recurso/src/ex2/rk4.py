def simulate_rk4(x0, y0, alpha, beta, delta, gamma, dt, t_final):
    """
    Simulates the Lotka-Volterra system using the Runge-Kutta 4th order method.

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

    def dx(x, y):
        return alpha * x - beta * x * y

    def dy(x, y):
        return delta * x * y - gamma * y

    t = 0.0
    x, y = x0, y0
    times = [t]
    xs = [x]
    ys = [y]

    while t < t_final:
        k1x = dx(x, y)
        k1y = dy(x, y)

        k2x = dx(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y)
        k2y = dy(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y)

        k3x = dx(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y)
        k3y = dy(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y)

        k4x = dx(x + dt * k3x, y + dt * k3y)
        k4y = dy(x + dt * k3x, y + dt * k3y)

        x += (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
        y += (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)

        t += dt
        times.append(t)
        xs.append(x)
        ys.append(y)

    return times, xs, ys

def initialize(x0, y0):
    """
    Inicializa o estado da simulação com os valores iniciais.
    Inputs:
        x0: população inicial das presas
        y0: população inicial dos predadores
    Returns:
        t: tempo inicial
        x, y: populações iniciais
        times, xs, ys: listas para armazenar a evolução temporal
    """
    t = 0.0
    times = [t]
    xs = [x0]
    ys = [y0]
    return t, x0, y0, times, xs, ys


def observe(t, x, y, times, xs, ys):
    """
    Regista o estado atual nas listas de séries temporais.
    Inputs:
        t: tempo atual
        x: população atual das presas
        y: população atual dos predadores
        times: lista de tempos registados
        xs: lista de populações de presas registadas
        ys: lista de populações de predadores registadas
    Returns:
        None
    """
    times.append(t)
    xs.append(x)
    ys.append(y)


def dx(x, y, alpha, beta):
    """
    Calcula a taxa de variação da população de presas (dx/dt) no modelo Lotka-Volterra adaptado.
    Inputs:
        x: população atual das presas
        y: população atual dos predadores
        alpha: taxa de crescimento das presas
        beta: taxa de predação
    Returns:
        valor da derivada dx/dt
    """
    return alpha * x - beta * x * y


def dy(x, y, delta, gamma):
    """
    Calcula a taxa de variação da população de predadores (dy/dt) no modelo Lotka-Volterra adaptado.
    Inputs:
        x: população atual das presas
        y: população atual dos predadores
        delta: taxa de crescimento dos predadores proporcional à predação
        gamma: taxa de mortalidade dos predadores
    Returns:
        valor da derivada dy/dt
    """
    return delta * x * y - gamma * y


def update_euler(x, y, alpha, beta, delta, gamma, dt):
    """
    Calcula o próximo estado do sistema usando o método de Euler.
    Inputs:
        x, y: populações atuais
        alpha, beta, delta, gamma: parâmetros do modelo Lotka-Volterra adaptado
        dt: passo de tempo
    Returns:
        x_new, y_new: populações atualizadas após o passo dt
    """
    x_new = x + dx(x, y, alpha, beta) * dt
    y_new = y + dy(x, y, delta, gamma) * dt
    return x_new, y_new


def update_rk4(x, y, alpha, beta, delta, gamma, dt):
    """
    Realiza um passo de atualização usando o método Runge-Kutta de ordem 4 (RK4).
    Inputs:
        x, y: populações atuais
        alpha, beta, delta, gamma: parâmetros do modelo Lotka-Volterra adaptado
        dt: passo de tempo
    Returns:
        x_new, y_new: populações atualizadas após o passo dt
    """
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
    Simula o sistema Lotka-Volterra adaptado usando o método especificado.
    Inputs:
        x0, y0: populações iniciais
        alpha, beta, delta, gamma: parâmetros do modelo
        dt: passo de tempo
        t_final: tempo final da simulação
        method: método numérico ("euler" ou "rk4")
    Returns:
        times: lista de tempos simulados
        xs: lista de populações de presas ao longo do tempo
        ys: lista de populações de predadores ao longo do tempo
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

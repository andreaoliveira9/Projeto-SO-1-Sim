import matplotlib.pyplot as plt


def plot_comparison(times_e, xs_e, ys_e, times_rk, xs_rk, ys_rk, dt, save_path=None):
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])

    # Presas (gráfico superior esquerdo)
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.plot(times_e, xs_e, label="Euler", linestyle="--")
    ax0.plot(times_rk, xs_rk, label="RK4")
    ax0.set_title("Evolução da População de Presas ao Longo do Tempo")
    ax0.set_xlabel("Tempo (s)")
    ax0.set_ylabel("Presas")
    ax0.legend()
    ax0.grid(True)

    # Predadores (gráfico superior direito)
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.plot(times_e, ys_e, label="Euler", linestyle="--")
    ax1.plot(times_rk, ys_rk, label="RK4")
    ax1.set_title("Evolução da População de Predadores ao Longo do Tempo")
    ax1.set_xlabel("Tempo (s)")
    ax1.set_ylabel("Predadores")
    ax1.legend()
    ax1.grid(True)

    # Combinado (gráfico inferior)
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(times_e, xs_e, label="Presas (Euler)", linestyle="--")
    ax2.plot(times_rk, xs_rk, label="Presas (RK4)")
    ax2.plot(times_e, ys_e, label="Predadores (Euler)", linestyle="--")
    ax2.plot(times_rk, ys_rk, label="Predadores (RK4)")
    ax2.set_title("Populações de Presas e Predadores ao Longo do Tempo")
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("População")
    ax2.legend()
    ax2.grid(True)

    plt.suptitle(f"Comparação dos métodos de Euler e RK4 (dt = {dt}s)")
    plt.tight_layout()
    if save_path:
        plt.savefig(f"{save_path}/comparacao_euler_rk4_{dt}.png")
    else:
        plt.show()


def plot_single(times, xs, ys, method, dt, save_path=None):
    plt.plot(times, xs, label="Presas")
    plt.plot(times, ys, label="Predadores")
    plt.xlabel("Tempo (s)")
    plt.ylabel("População")
    plt.title(f"Método de {method.upper()} (dt = {dt})")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(f"{save_path}/metodo_{method.lower()}_{dt}.png")
    else:
        plt.show()

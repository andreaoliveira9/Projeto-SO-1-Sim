import numpy as np
import matplotlib.pyplot as plt
import argparse

# Exemplos de execução:
# python exercise2.py --method rk4 --x0 0 --z0 0 --vx0 50 --vz0 50 --u 0.1 --dt 0.01 --tfinal 3
# python exercise2.py --method euler --x0 0 --z0 0 --vx0 50 --vz0 50 --u 0.1 --dt 0.01 --tfinal 3
# python exercise2.py --compare --x0 0 --z0 0 --vx0 50 --vz0 50 --u 0.1 --dt 0.01 --tfinal 3

def simulate_euler(x0, z0, vx0, vz0, u, dt, t_final, m=1.0, g=9.81):
    t_values = np.arange(0, t_final + dt, dt)
    x  = np.zeros_like(t_values)
    z  = np.zeros_like(t_values)
    vx = np.zeros_like(t_values)
    vz = np.zeros_like(t_values)
    
    # Condições iniciais
    x[0]  = x0
    z[0]  = z0
    vx[0] = vx0
    vz[0] = vz0
    
    for i in range(len(t_values) - 1):
        # Calcula as acelerações considerando o sinal da velocidade:
        ax = - (u/m) * vx[i] * abs(vx[i])
        az = - g - (u/m) * vz[i] * abs(vz[i])
        
        # Atualização pelo método de Euler
        x[i+1]  = x[i]  + dt * vx[i]
        vx[i+1] = vx[i] + dt * ax
        z[i+1]  = z[i]  + dt * vz[i]
        vz[i+1] = vz[i] + dt * az
        
    return t_values, x, z, vx, vz

def simulate_rk4(x0, z0, vx0, vz0, u, dt, t_final, m=1.0, g=9.81):
    t_values = np.arange(0, t_final + dt, dt)
    x  = np.zeros_like(t_values)
    z  = np.zeros_like(t_values)
    vx = np.zeros_like(t_values)
    vz = np.zeros_like(t_values)
    
    # Condições iniciais
    x[0]  = x0
    z[0]  = z0
    vx[0] = vx0
    vz[0] = vz0
    
    for i in range(len(t_values) - 1):
        # Função que retorna as derivadas
        def f(state):
            x_val, z_val, vx_val, vz_val = state
            return np.array([
                vx_val,                         # dx/dt
                vz_val,                         # dz/dt
                - (u/m) * vx_val * abs(vx_val),   # dvx/dt
                - g - (u/m) * vz_val * abs(vz_val) # dvz/dt
            ])
        
        state = np.array([x[i], z[i], vx[i], vz[i]])
        k1 = f(state)
        k2 = f(state + 0.5 * dt * k1)
        k3 = f(state + 0.5 * dt * k2)
        k4 = f(state + dt * k3)
        state_next = state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)
        x[i+1], z[i+1], vx[i+1], vz[i+1] = state_next
        
    return t_values, x, z, vx, vz

def main():
    parser = argparse.ArgumentParser(description="Simulação do movimento de um projétil com resistência do ar")
    parser.add_argument("--method", type=str, choices=["euler", "rk4"], default="euler",
                        help="Método de integração: euler ou rk4")
    parser.add_argument("--compare", action="store_true",
                        help="Executa ambos os métodos e compara os resultados")
    parser.add_argument("--x0", type=float, default=0.0, help="Posição inicial x")
    parser.add_argument("--z0", type=float, default=0.0, help="Posição inicial z")
    parser.add_argument("--vx0", type=float, default=50.0, help="Velocidade inicial em x")
    parser.add_argument("--vz0", type=float, default=50.0, help="Velocidade inicial em z")
    parser.add_argument("--u", type=float, default=0.1, help="Coeficiente de resistência do ar")
    parser.add_argument("--dt", type=float, default=0.01, help="Intervalo de tempo (Δt)")
    parser.add_argument("--tfinal", type=float, default=10.0, help="Tempo final da simulação")
    args = parser.parse_args()

    if args.compare:
        # Executa ambos os métodos com os mesmos parâmetros
        t_euler, x_euler, z_euler, vx_euler, vz_euler = simulate_euler(
            args.x0, args.z0, args.vx0, args.vz0, args.u, args.dt, args.tfinal)
        t_rk4, x_rk4, z_rk4, vx_rk4, vz_rk4 = simulate_rk4(
            args.x0, args.z0, args.vx0, args.vz0, args.u, args.dt, args.tfinal)
        
        print("=== Comparação entre os métodos Euler e RK4 ===")
        print(f"Erro em x (|x_euler - x_rk4|): {abs(x_euler[-1]-x_rk4[-1]):.4f}")
        print(f"Erro em z (|z_euler - z_rk4|): {abs(z_euler[-1]-z_rk4[-1]):.4f}")
        print(f"Erro em vx (|vx_euler - vx_rk4|): {abs(vx_euler[-1]-vx_rk4[-1]):.4f}")
        print(f"Erro em vz (|vz_euler - vz_rk4|): {abs(vz_euler[-1]-vz_rk4[-1]):.4f}")
        
        # Plota a comparação das trajetórias
        plt.figure()
        plt.plot(t_euler, x_euler, label="x (Euler)")
        plt.plot(t_rk4, x_rk4, label="x (RK4)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Posição x")
        plt.title("Comparação de x(t)")
        plt.legend()
        
        plt.figure()
        plt.plot(t_euler, z_euler, label="z (Euler)")
        plt.plot(t_rk4, z_rk4, label="z (RK4)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Posição z")
        plt.title("Comparação de z(t)")
        plt.legend()

        plt.figure()
        plt.plot(x_euler, z_euler, label="Trajetória (Euler)")
        plt.plot(x_rk4, z_rk4, label="Trajetória (RK4)")
        plt.xlabel("Posição x")
        plt.ylabel("Posição z")
        plt.title("Comparação das trajetórias")
        plt.legend()
        
        plt.show()
    else:
        # Executa o método selecionado
        if args.method == "euler":
            t, x, z, vx, vz = simulate_euler(
                args.x0, args.z0, args.vx0, args.vz0, args.u, args.dt, args.tfinal)
        else:
            t, x, z, vx, vz = simulate_rk4(
                args.x0, args.z0, args.vx0, args.vz0, args.u, args.dt, args.tfinal)
        
        plt.figure()
        plt.plot(t, x, label="x(t)")
        plt.plot(t, z, label="z(t)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Posição")
        plt.title(f"Trajetória usando o método {args.method.upper()}")
        plt.legend()
        plt.show()

        plt.figure()
        plt.plot(x, z, label="Trajetória")
        plt.xlabel("Posição x")
        plt.ylabel("Posição z")
        plt.title(f"Trajetória usando o método {args.method.upper()}")
        plt.legend()
        plt.show()
        
        print("=== Resultados da Simulação ===")
        print(f"Tempo final: {t[-1]:.2f} s")
        print(f"x(t_final): {x[-1]:.2f}")
        print(f"z(t_final): {z[-1]:.2f}")
        print(f"vx(t_final): {vx[-1]:.2f}")
        print(f"vz(t_final): {vz[-1]:.2f}")

if __name__ == '__main__':
    main()
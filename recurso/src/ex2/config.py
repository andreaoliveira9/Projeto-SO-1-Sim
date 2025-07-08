X0 = 10.0         # Número inicial de presas
Y0 = 10.0         # Número inicial de predadores
ALPHA = 0.1       # Taxa máxima de crescimento per capita das presas
BETA = 0.02       # Efeito da presença de predadores na taxa de crescimento das presas
DELTA = 0.02      # Efeito da presença de presas na taxa de crescimento dos predadores
GAMMA = 0.4       # Taxa de mortalidade per capita dos predadores
DT = 0.1          # Intervalo de tempo
T_FINAL = 1000    # Tempo total da simulação
METHOD = "rk4"    # Método de variação de Lotka-Volterra
SAVE_PATH = ""    # Caminho para salvar os resultados
COMPARE = False   # Flag para comparar métodos


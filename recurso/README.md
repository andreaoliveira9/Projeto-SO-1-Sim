# Projeto-SO-Sim-Rec

Primeiro projeto Simulação e Otimização de Recurso

Nota:

## How to run

1. Clone the repository

```bash
git clone git@github.com:andreaoliveira9/Projeto-SO-Sim.git
cd Projeto-SO-Sim/recurso
```

2. Create a virtual environment and activate it

```bash
python3.9 -m venv venv
source venv/bin/activate
```

3. Install the requirements

```bash
pip install -r src/requirements.txt
```

### Exercise 1

```bash
python src/ex1/main.py
```

**Note:** Default parameters can be modified in `src/ex1/config.py`.

#### With custom parameters

```bash
python src/ex1/main.py --serversA 3 --serversB 2 --seed 42 --verbose
```

#### Command-line parameters

| Parameter    | Description                                | Default |
| ------------ | ------------------------------------------ | ------- |
| `--serversA` | Number of type A servers                   | 2       |
| `--serversB` | Number of type B servers                   | 1       |
| `--seed`     | Random seed for reproducible results       | None    |
| `--verbose`  | Enable verbose output for detailed logging | False   |
| `--simpy`    | Use SimPy for simulation                   | False   |

### Exercise 2

```bash
python src/ex2/main.py
```

**Note:** Default parameters can be modified in `src/ex2/config.py`.

#### Using the Runge-Kutta 4th-order method (RK4)

```bash
python src/ex2/main.py --method rk4 --x0 10.0 --y0 10.0 --alpha 0.1 --beta 0.02 --delta 0.02 --gamma 0.4 --dt 0.1 --tfinal 1000
```

#### Using the Euler method

```bash
python src/ex2/main.py --method euler --x0 10.0 --y0 10.0 --alpha 0.1 --beta 0.02 --delta 0.02 --gamma 0.4 --dt 0.1 --tfinal 1000
```

#### Comparing both methods

```bash
python src/ex2/main.py --compare --x0 10.0 --y0 10.0 --alpha 0.1 --beta 0.02 --delta 0.02 --gamma 0.4 --dt 0.1 --tfinal 1000
```

#### With custom save path

```bash
python src/ex2/main.py --compare --x0 10.0 --y0 10.0 --alpha 0.1 --beta 0.02 --delta 0.02 --gamma 0.4 --dt 0.1 --save_path docs/ex2
```

#### Command-line parameters

| Parameter     | Description                                | Default |
| ------------- | ------------------------------------------ | ------- |
| `--method`    | Numerical method to use (`euler` or `rk4`) | `rk4`   |
| `--compare`   | Runs and compares both methods             | False   |
| `--x0`        | Initial number of preys                    | 10.0    |
| `--y0`        | Initial number of predators                | 10.0    |
| `--alpha`     | Maximum prey per capita growth rate        | 0.1     |
| `--beta`      | Effect of predators on prey growth rate    | 0.02    |
| `--delta`     | Effect of prey on predator's growth rate   | 0.02    |
| `--gamma`     | Predator's per capita death rate           | 0.4     |
| `--dt`        | Time step interval                         | 0.1     |
| `--tfinal`    | Total simulation time                      | 1000    |
| `--save_path` | Directory path to save generated plots     | ""      |

# Projeto-SO-Sim
Primeiro projeto Simulação e Otimização

## How to run

1. Clone the repository

```bash
git clone git@github.com:andreaoliveira9/Projeto-SimOpt-1.git
cd Projeto-SimOpt-1
```

1. Create a virtual environment and activate it
   
```bash
python3.13 -m venv venv
source venv/bin/activate
```

3. Install the requirements

```bash
pip install -r src/requirements.txt
```

### Exercise 1

```bash
python src/exercise1.py
```

This script runs the same simulation using an implementation with SimPy, also without any command-line parameters.

### Exercise 1 (no SimPy)

```bash
python src/exercise1_nosimpy.py
```

This script runs a basic simulation using a method without SimPy and does not require any command-line parameters.

### Exercise 2

#### Using the Runge-Kutta 4th-order method (RK4)

```bash
python src/exercise2.py --method rk4 --x0 0 --z0 0 --vx0 50 --vz0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81
```

#### Using the Euler method

```bash
python src/exercise2.py --method euler --x0 0 --z0 0 --vx0 50 --vz0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81
```

#### Comparing both methods

```bash
python src/exercise2.py --compare --x0 0 --z0 0 --vx0 50 --vz0 50 --drag 0.1 --dt 0.01 --tfinal 3 --mass 1.0 --gravity 9.81
```

#### Command-line parameters

| Parameter     | Description                                               |
|---------------|-----------------------------------------------------------|
| `--method`    | Numerical method to use (`euler` or `rk4`)                |
| `--compare`   | Runs and compares both methods                            |
| `--x0`        | Initial position in the x-axis (in meters)                |
| `--z0`        | Initial position in the z-axis (in meters)                |
| `--vx0`       | Initial velocity in the x-axis (in m/s)                   |
| `--vz0`       | Initial velocity in the z-axis (in m/s)                   |
| `--drag`      | Drag coefficient (air resistance)                         |
| `--dt`        | Time step of the simulation (in seconds)                  |
| `--tfinal`    | Total simulation time (in seconds)                        |
| `--mass`      | Mass of the object (in kg)                                |
| `--gravity`   | Acceleration due to gravity (in m/s²)                     |

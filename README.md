# Marine Engine Critical RPM — Torsional Vibration Analysis

## Project Overview

This project is a Python-based engineering analysis of **torsional vibration and critical rotational speeds** for a representative slow-speed, two-stroke marine main engine.

The model represents a:

* Sulzer-class slow-speed marine diesel engine
* 6-cylinder configuration
* 2-stroke operating cycle
* 12,000 HP rated power
* 105 RPM rated speed
* Four lumped rotational inertias
* Three torsional shaft stiffnesses

The project demonstrates how engine excitation orders can interact with torsional natural frequencies and produce critical-speed conditions.

The analysis progresses from the basic mechanical model through natural-frequency calculation, critical RPM identification, forced response, torsional torque, shaft stress, and shaft-diameter sensitivity.

---

## Important Engineering Note

This project is an **educational and representative engineering model**.

It is intended to demonstrate the principles and computational workflow of torsional vibration analysis.

It is **not** a certified marine shafting calculation and must not be used as a substitute for:

* Classification Society calculations
* Manufacturer's engine data
* Propeller manufacturer's calculations
* Detailed crankshaft analysis
* Detailed shaft-line analysis
* Approved torsional vibration calculations
* Fatigue calculations
* Actual material properties
* Classification Society acceptance criteria

The engine is described as **Sulzer-class representative** rather than as a model of a specific production engine.

---

# 1. Project Objectives

The main objectives are to:

1. Build a simplified multi-degree-of-freedom torsional model.
2. Define representative engine and shaft inertias.
3. Define torsional shaft stiffnesses.
4. Calculate torsional natural frequencies.
5. Identify excitation-order intersections.
6. Calculate candidate critical RPMs.
7. Produce a critical-speed diagram.
8. Calculate a simplified forced torsional response.
9. Calculate alternating torsional torque.
10. Estimate torsional shear stress.
11. Investigate the influence of shaft diameter on torsional stress.

---

# 2. Engineering Model

The shafting system is represented by four rotational inertias connected by three torsional springs.

Simplified arrangement:

```text
   Engine       Intermediate       Tail Shaft       Propeller
     J1              J2                J3               J4
     |               |                 |                |
     O------ k1 -----O------ k2 -------O------ k3 ------O
```

Where:

* `J1` = engine equivalent rotational inertia
* `J2` = intermediate shaft equivalent inertia
* `J3` = tail shaft equivalent inertia
* `J4` = propeller equivalent inertia
* `k1` = torsional stiffness between engine and intermediate shaft
* `k2` = torsional stiffness between intermediate and tail shaft
* `k3` = torsional stiffness between tail shaft and propeller

---

# 3. Representative Engine Data

| Parameter       |                       Value |
| --------------- | --------------------------: |
| Engine type     | Sulzer-class representative |
| Cylinders       |                           6 |
| Cycle           |                    2-stroke |
| Rated power     |                   12,000 HP |
| Rated speed     |                     105 RPM |
| Operating range |                  50–105 RPM |

For a six-cylinder two-stroke engine, the main firing excitation was represented by the **6th order**.

The analysis also investigates:

```text
6th
12th
18th
24th
30th
```

excitation orders.

---

# 4. Rotational Inertias

The model uses the following representative inertias:

| Component          |      Inertia |
| ------------------ | -----------: |
| Engine             | 12,000 kg·m² |
| Intermediate shaft |  2,000 kg·m² |
| Tail shaft         |  2,500 kg·m² |
| Propeller          | 18,000 kg·m² |

Therefore:

```text
J1 = 12000 kg·m²
J2 =  2000 kg·m²
J3 =  2500 kg·m²
J4 = 18000 kg·m²
```

---

# 5. Torsional Stiffness

The representative shaft stiffnesses are:

| Shaft section |      Stiffness |
| ------------- | -------------: |
| k1            | 23.30 MN·m/rad |
| k2            | 40.80 MN·m/rad |
| k3            | 40.80 MN·m/rad |

In SI units:

```text
k1 = 23,300,000 N·m/rad
k2 = 40,800,000 N·m/rad
k3 = 40,800,000 N·m/rad
```

---

# 6. Mathematical Model

The torsional vibration system is represented by:

```text
M θ¨ + K θ = 0
```

where:

* `M` = inertia matrix
* `K` = torsional stiffness matrix
* `θ` = vector of angular displacements

The mass/inertia matrix is:

```text
M =

[12000     0       0       0]
[    0  2000       0       0]
[    0     0    2500       0]
[    0     0       0   18000]
```

The stiffness matrix is:

```text
K =

[ 23300000  -23300000         0         0]
[-23300000   64100000 -40800000         0]
[        0  -40800000  81600000 -40800000]
[        0          0 -40800000  40800000]
```

The natural frequencies are obtained from the generalized eigenvalue problem:

```text
K φ = λ M φ
```

and:

```text
ω = sqrt(λ)
```

with:

```text
f = ω / (2π)
```

---

# 7. Natural Frequencies

The calculated natural frequencies were:

| Mode                  |          Frequency |
| --------------------- | -----------------: |
| Rigid-body mode       | approximately 0 Hz |
| First torsional mode  |          6.1509 Hz |
| Second torsional mode |         20.2574 Hz |
| Third torsional mode  |         36.0141 Hz |

The rigid-body mode is expected because the complete shafting system is free to rotate as a whole.

The engineering torsional modes are therefore:

```text
6.1509 Hz
20.2574 Hz
36.0141 Hz
```

---

# 8. Critical RPM Calculation

For an excitation order `n`:

```text
f_excitation = n × RPM / 60
```

Therefore:

```text
RPM_critical = 60 × f_n / n
```

For the principal 6th-order excitation:

### First torsional mode

```text
f = 6.1509 Hz

RPM = 60 × 6.1509 / 6

RPM ≈ 61.51 RPM
```

This lies inside the representative operating range of:

```text
50–105 RPM
```

Therefore the simplified model identifies:

```text
61.51 RPM
```

as a candidate critical speed for the 6th-order excitation.

---

# 9. Excitation-Order Intersections

The calculated mathematical intersections inside the 50–105 RPM operating range include approximately:

| Natural frequency | Excitation order |    RPM |
| ----------------: | ---------------: | -----: |
|         6.1509 Hz |              6th |  61.51 |
|        20.2574 Hz |             12th | 101.29 |
|        20.2574 Hz |             18th |  67.52 |
|        20.2574 Hz |             24th |  50.64 |
|        36.0141 Hz |             24th |  90.04 |
|        36.0141 Hz |             30th |  72.03 |

These are **mathematical frequency intersections**.

An intersection by itself does not establish that a dangerous torsional vibration condition exists.

Actual vibration severity depends on factors including:

* excitation torque amplitude
* modal participation
* damping
* shaft geometry
* crankshaft characteristics
* coupling characteristics
* propeller characteristics
* material properties
* operating condition

---

# 10. Critical-Speed Diagram

The project generates a critical-speed diagram showing:

* Engine RPM
* Excitation-order lines
* Torsional natural frequencies
* Frequency intersections
* Operating speed range

The diagram provides a visual representation of where excitation frequencies can coincide with torsional natural frequencies.

---

# 11. Forced Torsional Response

A simplified forced-response calculation was performed using:

```text
Damping ratio              = 0.030
Excitation torque          = 1,000,000 N·m
```

The static torsional angle was calculated as:

```text
θ_static = T / k1
```

giving:

```text
θ_static = 0.042918 rad
```

or:

```text
θ_static = 2.459046°
```

The simplified forced-response calculation produced a maximum response at:

```text
Engine speed = 61.45 RPM
```

with:

```text
Torsional angle amplitude = 41.002531°
```

This is very close to the calculated 6th-order critical speed of:

```text
61.51 RPM
```

This demonstrates the resonance mechanism in the simplified model.

---

# 12. Important Interpretation of the Forced Response

The calculated:

```text
41.002531°
```

torsional angle should **not** be interpreted as an actual predicted shaft angle for a real marine engine.

It results from deliberately simplified assumptions:

```text
Excitation torque = 1,000,000 N·m
Damping ratio     = 3%
Simplified modal response
```

A real marine torsional vibration calculation would require detailed excitation harmonics, modal participation factors, damping, shaft geometry, crankshaft properties, coupling characteristics, propeller characteristics, and other system data.

The purpose of this calculation is to demonstrate the relationship:

```text
Excitation
    ↓
Natural frequency
    ↓
Resonance
    ↓
Large dynamic response
```

---

# 13. Torsional Vibration Stress

The maximum simplified torsional angle was converted to radians:

```text
θmax = 0.715629 rad
```

The alternating torque was estimated using:

```text
T = k1 × θ
```

giving:

```text
Alternating torque = 16,674,160 N·m
```

or:

```text
Alternating torque = 16.674 MN·m
```

For a representative solid circular shaft:

```text
τ = 16T / (πd³)
```

Using:

```text
d = 0.800 m
```

the calculated torsional shear stress was:

```text
τ = 165.861 MPa
```

This is again a result of the simplified model and should not be treated as a certified design stress.

---

# 14. Shaft Diameter Sensitivity

The project investigates the effect of shaft diameter on torsional shear stress.

The relationship is:

```text
τ = 16T / (πd³)
```

Therefore:

```text
τ ∝ 1/d³
```

Using the calculated alternating torque of approximately:

```text
16.674 MN·m
```

the following values were obtained:

| Shaft diameter | Torsional stress |
| -------------: | ---------------: |
|         0.60 m |      393.152 MPa |
|         0.65 m |      309.225 MPa |
|         0.70 m |      247.583 MPa |
|         0.75 m |      201.294 MPa |
|         0.80 m |      165.861 MPa |
|         0.85 m |      138.279 MPa |
|         0.90 m |      116.489 MPa |
|         0.95 m |       99.047 MPa |
|         1.00 m |       84.921 MPa |

This demonstrates the strong influence of shaft diameter on torsional shear stress.

---

# 15. Project Workflow

The complete analysis follows this sequence:

```text
Engine data
     ↓
Rotational inertias
     ↓
Torsional stiffness
     ↓
Mass and stiffness matrices
     ↓
Natural frequencies
     ↓
Excitation orders
     ↓
Critical RPMs
     ↓
Critical-speed diagram
     ↓
Forced torsional response
     ↓
Alternating torsional torque
     ↓
Torsional shear stress
     ↓
Shaft diameter sensitivity
```

---

# 16. Software Requirements

The project uses Python.

Recommended environment:

```text
Python 3.x
NumPy
Matplotlib
```

The project was developed and tested on Windows using a Python virtual environment.

---

# 17. Installation

Open PowerShell and navigate to the project:

```powershell
cd C:\dev1\marine-engine-critical-rpm
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install required packages if necessary:

```powershell
python -m pip install numpy matplotlib
```

---

# 18. Running the Program

With the virtual environment activated:

```powershell
python torsional_model.py
```

The program performs the complete analysis and produces the numerical results and engineering plots.

---

# 19. Opening the Project in Notepad++

The project file can be opened using:

```powershell
& "C:\Program Files\Notepad++\notepad++.exe" "C:\dev1\marine-engine-critical-rpm\torsional_model.py"
```

---

# 20. Project Structure

The main project directory is:

```text
C:\dev1\marine-engine-critical-rpm
```

The main Python program is:

```text
torsional_model.py
```

A typical project structure is:

```text
marine-engine-critical-rpm/
│
├── .venv/
│
├── torsional_model.py
│
└── README.md
```

The `.venv` directory contains the local Python virtual environment and normally should not be committed to Git.

---

# 21. Main Engineering Assumptions

The model uses several simplifications:

1. The engine is represented by lumped rotational inertias.
2. Shaft sections are represented by linear torsional springs.
3. The shafting model has four rotational degrees of freedom.
4. The engine is represented by six cylinders.
5. The main firing excitation is represented by the 6th order.
6. Higher excitation orders are investigated as mathematical harmonics.
7. Damping is represented by a simplified damping ratio.
8. The forced response uses a simplified frequency-response formulation.
9. A representative excitation torque is assumed.
10. Shaft stress is calculated using a solid circular shaft equation.
11. The shaft diameter sensitivity analysis keeps the calculated alternating torque constant.
12. The model does not perform a full nonlinear or transient torsional analysis.

---

# 22. Limitations

The following are outside the scope of this project:

* Detailed crankshaft geometry
* Individual cylinder gas-pressure harmonics
* Fuel injection variations
* Crankshaft flexibility
* Bearing dynamics
* Propeller hydrodynamic excitation
* Gearbox dynamics
* Flexible couplings
* Viscous torsional dampers
* Nonlinear stiffness
* Nonlinear damping
* Temperature-dependent material properties
* Fatigue-life calculations
* Classification Society acceptance calculations
* Actual manufacturer shafting data
* Finite-element analysis
* Experimental validation

Consequently, the numerical results should be considered **representative engineering calculations for learning and software development**.

---

# 23. Engineering Significance

Despite the simplifications, the project demonstrates several important principles of marine torsional vibration analysis.

The most important relationship is:

```text
Excitation frequency ≈ Natural frequency
                    ↓
                 Resonance
                    ↓
          Increased vibration response
                    ↓
          Increased alternating torque
                    ↓
          Increased torsional stress
```

The project also demonstrates that critical RPM is not simply a property of engine speed.

It depends on the interaction between:

```text
Engine excitation orders
        +
Shafting natural frequencies
```

Therefore, changing shafting characteristics can change the locations of critical speeds.

---

# 24. Final Project Results

The completed representative model produced:

```text
Rated engine speed             : 105 RPM

Torsional natural frequencies:
    Mode 1                     : 6.1509 Hz
    Mode 2                     : 20.2574 Hz
    Mode 3                     : 36.0141 Hz

Main 6th-order critical speed:
                                61.51 RPM

Simplified forced-response peak:
                                61.45 RPM

Maximum simplified angle:
                                41.002531°

Alternating torque:
                                16.674 MN·m

Stress at 0.800 m shaft:
                                165.861 MPa
```

The close agreement between the 6th-order critical-speed calculation and the forced-response peak demonstrates the expected resonance behavior of the simplified model.

---

# 25. Conclusion

This project provides a complete introductory computational workflow for investigating torsional vibration in a representative slow-speed marine diesel engine.

It connects:

```text
Mechanical engineering theory
            +
Matrix mathematics
            +
Python programming
            +
Numerical analysis
            +
Engineering visualization
```

The completed model demonstrates how a marine engine's excitation orders can interact with shafting natural frequencies and produce candidate critical speeds, and how a simplified resonance calculation can be extended to estimate alternating torque and torsional shear stress.

The project is intended as a foundation for future improvements such as:

* detailed harmonic excitation,
* full damped multi-degree-of-freedom forced response,
* mode-shape parti

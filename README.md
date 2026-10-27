# Marine Engine Critical RPM --- Torsional Vibration Analysis

## Project Overview

This Python project investigates torsional vibration and candidate
critical rotational speeds for a **representative slow-speed, two-stroke
marine diesel engine**.

The model is inspired by a Sulzer-class engine arrangement for
educational purposes. It is not a model of a specific production engine
and does not use verified manufacturer shafting data.

The project progresses through:

-   a four-inertia, three-shaft-section torsional model;
-   natural-frequency calculation;
-   excitation-order and critical-RPM calculations;
-   critical-speed visualization;
-   simplified forced-response estimation;
-   alternating torque and torsional shear-stress calculations;
-   shaft-diameter sensitivity;
-   shaft geometry and stiffness estimates;
-   comparison of the original and geometry-based models;
-   a consolidated critical-RPM visualization.

## Important Engineering Disclaimer

**This is an educational, representative calculation---not an approved
marine-engine torsional-vibration analysis.**

Do not use these results to select an operating-speed restriction,
approve a shaft line, establish a safe operating range, or make a
vessel-safety decision. Real approval requires validated engine and
shafting data, the actual excitation harmonics, propeller and coupling
characteristics, damping, detailed analysis, and review by the engine
manufacturer and relevant classification society.

A mathematical intersection between an excitation order and a natural
frequency is a **candidate critical speed**. An intersection alone does
not prove that harmful resonance will occur.

## 1. Representative Engine Data

  Parameter                                         Model value
  ------------------------------- -----------------------------
  Engine class                      Sulzer-class representative
  Cylinders                                                   6
  Cycle                                              Two-stroke
  Representative rated power                          12,000 HP
  Representative rated speed                            105 RPM
  Investigated operating range                      50--105 RPM
  Rotational degrees of freedom                               4
  Shaft sections                                              3

For this simplified six-cylinder, two-stroke example, the main firing
excitation is represented by the 6th order. The model also examines the
12th, 18th, 24th, and 30th orders as mathematical harmonics.

## 2. Mechanical Model

The system is represented by four lumped rotational inertias connected
by three torsional springs:

``` text
   Engine       Intermediate       Tail Shaft       Propeller
     J1              J2                J3               J4
     O------ k1 -----O------ k2 -------O------ k3 ------O
```

The representative inertias are:

  Inertia            Value
  --------- --------------
  J1          12,000 kg·m²
  J2           2,000 kg·m²
  J3           2,500 kg·m²
  J4          18,000 kg·m²

The original shaft stiffnesses are:

  Shaft section          Stiffness
  --------------- ----------------
  k1                23.30 MN·m/rad
  k2                40.80 MN·m/rad
  k3                40.80 MN·m/rad

These are representative model inputs, not verified dimensions or
properties from an actual engine.

## 3. Mathematical Formulation

The undamped free-vibration model is:

\[ M`\ddot{\theta}`{=tex}+K`\theta=0`{=tex} \]

where (M) is the inertia matrix, (K) is the torsional stiffness matrix,
and (`\theta`{=tex}) is the vector of angular displacements.

The natural modes are calculated from the generalized eigenvalue
problem:

\[ K`\phi`{=tex}=`\lambda `{=tex}M`\phi`{=tex} \]

For each eigenvalue, the angular natural frequency and frequency in
hertz are:

\[
`\omega`{=tex}\_n=`\sqrt{\lambda_n}`{=tex},`\qquad `{=tex}f_n=`\frac{\omega_n}{2\pi}`{=tex}
\]

The complete free-free system has a rigid-body mode near 0 Hz. The
remaining three modes are the flexible torsional modes.

## 4. Critical RPM Calculation

For excitation order (q), engine speed (N) in RPM, and excitation
frequency (f_e) in hertz:

\[ f_e=`\frac{qN}{60}`{=tex} \]

Equating the excitation frequency to a natural frequency gives the
candidate critical speed:

\[ N_c=`\frac{60f_n}{q}`{=tex} \]

The program calculates intersections for orders 6, 12, 18, 24, and 30
and identifies those falling within the representative 50--105 RPM
range.

## 5. Original-Model Natural Frequencies

The original stiffness model gives the following flexible torsional
frequencies:

  Flexible mode     Natural frequency
  --------------- -------------------
  Mode 1                    6.1509 Hz
  Mode 2                   20.2574 Hz
  Mode 3                   36.0141 Hz

The rigid-body mode is approximately 0 Hz and is not included in the
flexible-mode table.

## 6. Original-Model Candidate Critical Speeds

The candidate intersections within the 50--105 RPM range are:

  Mode       Excitation order   Candidate speed
  -------- ------------------ -----------------
  Mode 1                  6th         61.51 RPM
  Mode 2                 12th        101.29 RPM
  Mode 2                 18th         67.52 RPM
  Mode 2                 24th         50.64 RPM
  Mode 3                 24th         90.04 RPM
  Mode 3                 30th         72.03 RPM

These are mathematical candidates, not confirmed harmful resonance
speeds.

## 7. Simplified Forced Response, Torque, and Stress

The project includes an illustrative forced-response calculation using a
simplified damping assumption and representative excitation torque. The
resulting angular response is used to estimate alternating shaft torque
and torsional shear stress.

The calculation is intended to demonstrate the workflow, not to predict
the response of a real engine. Its output depends strongly on the
assumed torque distribution, damping, shaft parameters, and
simplifications in the response formulation.

For a solid circular shaft, the nominal maximum torsional shear stress
is estimated from:

\[ `\tau`{=tex}\_{`\max`{=tex}}=`\frac{16T}{\pi d^3}`{=tex} \]

where (T) is the alternating torque and (d) is the shaft diameter. This
equation does not account for stress concentrations, keyways, fillets,
material fatigue, or other real shaft-design details.

**Important:** Forced-response values in this educational model should
be read directly from the output of the saved `torsional_model.py`. They
are not design allowables or validated predictions.

## 8. Shaft-Diameter Sensitivity

The project examines how the nominal torsional shear-stress estimate
changes with shaft diameter while holding the calculated alternating
torque constant.

For the solid circular shaft equation, stress varies inversely with the
cube of diameter:

\[ `\tau`{=tex}\_{`\max`{=tex}}`\propto`{=tex}`\frac{1}{d^3}`{=tex} \]

This is a sensitivity demonstration only. In a real system, changing
shaft diameter also changes torsional stiffness and may therefore change
natural frequencies and response.

## 9. Geometry-Based Shaft Stiffness

A later project stage estimates torsional stiffness from illustrative
shaft dimensions using:

\[ k=`\frac{GJ_p}{L}`{=tex} \]

For a solid circular shaft:

\[ J_p=`\frac{\pi d^4}{32}`{=tex} \]

where (G) is the assumed shear modulus, (J_p) is the polar second moment
of area, (L) is shaft length, and (d) is shaft diameter.

The illustrative geometry uses:

  -----------------------------------------------------------------------
  Parameter               Section 1          Section 2          Section 3
  -------------- ------------------ ------------------ ------------------
  Diameter                  0.400 m            0.450 m            0.450 m

  Length                      8.0 m              8.0 m              8.0 m

  Assumed shear              80 GPa             80 GPa             80 GPa
  modulus                                              

  Calculated        25.133 MN·m/rad    40.258 MN·m/rad    40.258 MN·m/rad
  stiffness                                            
  -----------------------------------------------------------------------

These dimensions and material assumptions are illustrative. They are not
actual Sulzer engine or vessel shafting dimensions.

The geometry-based stiffnesses are compared with the original stiffness
values. The geometry-based model is a separate sensitivity case; it does
not establish the correct shaft geometry for a real vessel.

## 10. Geometry-Based Natural Frequencies

Using the illustrative geometry-derived stiffnesses, the calculated
flexible frequencies are:

  Flexible mode     Original model   Geometry-based model
  --------------- ---------------- ----------------------
  Mode 1                 6.1509 Hz              6.2326 Hz
  Mode 2                20.2574 Hz             20.5097 Hz
  Mode 3                36.0141 Hz             35.9748 Hz

The small changes demonstrate how changing shaft stiffness can shift the
system's natural frequencies. These values describe the two assumed
mathematical models, not a validated physical shaft line.

## 11. Original vs. Geometry-Based Candidate Speeds

The candidate speeds within 50--105 RPM compare as follows:

  Mode       Order   Original model   Geometry-based model               Change
  -------- ------- ---------------- ---------------------- --------------------
  Mode 1       6th        61.51 RPM              62.33 RPM   +0.82 RPM (+1.33%)
  Mode 2      12th       101.29 RPM             102.55 RPM   +1.26 RPM (+1.25%)
  Mode 2      18th        67.52 RPM              68.37 RPM   +0.84 RPM (+1.25%)
  Mode 2      24th        50.64 RPM              51.27 RPM   +0.63 RPM (+1.25%)
  Mode 3      24th        90.04 RPM              89.94 RPM   −0.10 RPM (−0.11%)
  Mode 3      30th        72.03 RPM              71.95 RPM   −0.08 RPM (−0.11%)

The comparison shows that the predicted change depends on the mode and
excitation order. It does not, by itself, indicate whether a particular
speed is safe or unsafe.

## 12. Visualizations

The program includes visualizations for the critical-speed diagram and a
comparison of the original and geometry-based candidate speeds.

The comparison plot uses:

-   circle markers for the original model;
-   X markers for the geometry-based model;
-   connecting lines to show the change between the two predictions;
-   the representative 50--105 RPM operating range.

Plots are explanatory aids. They do not replace a formal
torsional-vibration report or an approved barred-speed-range assessment.

## 13. Software Requirements

The project uses Python with the following packages:

-   NumPy --- numerical arrays and matrix operations;
-   SciPy --- generalized eigenvalue calculation;
-   Matplotlib --- plots and visualizations.

The script uses `scipy.linalg.eigh` for the generalized symmetric
eigenvalue problem.

## 14. Running the Project on Windows

Open PowerShell and run:

``` powershell
cd C:\dev1\marine-engine-critical-rpm
.\.venv\Scripts\Activate.ps1
python -m py_compile torsional_model.py
python torsional_model.py
```

The compile command checks Python syntax. If it returns to the
PowerShell prompt without an error message, the syntax check passed.

To run the program, execute `python torsional_model.py`. Read the
console output for the calculated results and completion messages.
Matplotlib may display figures in separate windows, depending on the
local plotting environment.

If the virtual environment does not exist, create it and install the
required packages:

``` powershell
cd C:\dev1\marine-engine-critical-rpm
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib
```

Then run the syntax check and program commands above.

## 15. Main Engineering Assumptions

The model makes the following simplifications:

1.  The engine and propeller system is represented by four lumped
    rotational inertias.
2.  Shaft sections are represented by linear torsional springs.
3.  The model has four rotational degrees of freedom.
4.  The engine is represented as a six-cylinder, two-stroke example.
5.  The main firing excitation is represented by the 6th order.
6.  Higher excitation orders are examined as mathematical harmonics.
7.  Damping is represented by a simplified damping ratio.
8.  Forced response uses a simplified frequency-response formulation.
9.  A representative excitation torque is assumed.
10. Shaft stress is estimated using a solid circular shaft equation.
11. The shaft-diameter sensitivity study holds the calculated
    alternating torque constant.
12. Geometry-based shaft dimensions and shear modulus are illustrative.
13. The model does not perform a full nonlinear or transient torsional
    analysis.

## 16. Limitations

The project does not include:

-   detailed crankshaft geometry;
-   individual cylinder gas-pressure harmonics;
-   cylinder-to-cylinder firing variations;
-   crankshaft flexibility;
-   bearing dynamics;
-   propeller hydrodynamic excitation;
-   gearbox dynamics;
-   flexible couplings;
-   viscous torsional dampers;
-   nonlinear stiffness or damping;
-   temperature-dependent material properties;
-   fatigue-life calculations;
-   classification-society acceptance calculations;
-   actual manufacturer shafting data;
-   finite-element analysis;
-   experimental validation.

Consequently, the numerical results should be treated as representative
engineering calculations for learning and software development.

## 17. Engineering Significance

The project demonstrates the relationship:

``` text
Excitation frequency approaches a natural frequency
                     ↓
          Potential resonance condition
                     ↓
       Potentially increased vibration response
                     ↓
        Potentially increased alternating torque
                     ↓
        Potentially increased torsional stress
```

Critical RPM depends on the interaction between engine excitation orders
and shafting natural frequencies. Changes to inertia or shaft stiffness
can change the natural frequencies and therefore shift candidate
critical speeds.

## 18. Final Project Summary

The completed project demonstrates the following workflow:

1.  Define a simplified multi-inertia torsional system.
2.  Calculate its flexible natural frequencies.
3.  Calculate candidate critical speeds for several excitation orders.
4.  identify intersections within the representative operating range.
5.  Visualize the critical-speed relationships.
6.  Estimate a simplified forced torsional response.
7.  Use the response to demonstrate alternating torque and nominal
    shear-stress calculations.
8.  Explore the effect of shaft diameter on nominal stress.
9.  Calculate illustrative shaft stiffness from assumed geometry.
10. Compare the original and geometry-based models.
11. Plot the candidate-speed changes between the models.

Key reference results for the original model are 6.1509 Hz, 20.2574 Hz,
and 36.0141 Hz for its three flexible torsional modes. The first-mode,
6th-order intersection is approximately 61.51 RPM. The illustrative
geometry-based model gives flexible frequencies of 6.2326 Hz, 20.5097
Hz, and 35.9748 Hz, with six candidate intersections in the 50--105 RPM
range for both models.

## 19. Conclusion

This project provides an introductory computational workflow connecting
mechanical engineering theory, matrix mathematics, Python programming,
numerical analysis, and engineering visualization.

It demonstrates how excitation orders can intersect shafting natural
frequencies, how those intersections produce candidate critical speeds,
and how a simplified response can be used to illustrate alternating
torque and torsional shear stress.

**Project status:** The educational workflow and the
original-versus-geometry-based comparison are complete through the
critical-RPM visualization stage. Further development is optional and is
not required to understand or present the completed work.

The results remain illustrative and must not be interpreted as an
approved analysis of a real marine engine or shaft line.

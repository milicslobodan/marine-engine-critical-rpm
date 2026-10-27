# USER INSTRUCTIONS --- Marine Engine Critical RPM

## 1. Purpose of This Project

This project performs a simplified torsional-vibration analysis of a
representative slow-speed, two-stroke marine main engine.

The program demonstrates:

-   torsional natural frequencies;
-   excitation orders and candidate critical RPMs;
-   critical-speed diagrams;
-   simplified forced torsional response;
-   alternating torsional torque and nominal torsional shear stress;
-   shaft-diameter sensitivity;
-   illustrative shaft geometry and geometry-based stiffness;
-   comparison of the original and geometry-based models;
-   a final critical-RPM comparison visualization.

This is an **educational engineering model**, not an approved marine
shafting or torsional-vibration calculation.

## 2. System Requirements

The project is designed for Windows.

Required software and Python packages:

-   Windows 10 or Windows 11;
-   Python 3.x;
-   PowerShell;
-   NumPy;
-   SciPy;
-   Matplotlib.

Notepad++ is optional but recommended for editing the Python program.

## 3. Project Location

The project folder is:

``` text
C:\dev1\marine-engine-critical-rpm
```

The main Python program is:

``` text
C:\dev1\marine-engine-critical-rpm\torsional_model.py
```

The documentation files are:

``` text
C:\dev1\marine-engine-critical-rpm\README.md
C:\dev1\marine-engine-critical-rpm\USER_INSTRUCTIONS.md
```

## 4. Open PowerShell

Open Windows PowerShell from the Start menu, or search for `PowerShell`.

## 5. Go to the Project Directory

Enter:

``` powershell
cd C:\dev1\marine-engine-critical-rpm
```

The prompt should look similar to:

``` text
PS C:\dev1\marine-engine-critical-rpm>
```

## 6. Activate the Python Virtual Environment

Activate the project's local virtual environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

The prompt should now contain `(.venv)`, for example:

``` text
(.venv) PS C:\dev1\marine-engine-critical-rpm>
```

This indicates that the project environment is active.

## 7. Check Python

Run:

``` powershell
python --version
python -c "import sys; print(sys.executable)"
```

The executable path should point to:

``` text
C:\dev1\marine-engine-critical-rpm\.venv\Scripts\python.exe
```

## 8. Check Required Python Packages

Check the packages:

``` powershell
python -c "import numpy; print('NumPy', numpy.__version__)"
python -c "import scipy; print('SciPy', scipy.__version__)"
python -c "import matplotlib; print('Matplotlib', matplotlib.__version__)"
```

The project uses NumPy for numerical arrays and matrix operations, SciPy
for the generalized eigenvalue calculation, and Matplotlib for plots.

If a package is missing, install all required packages in the active
virtual environment:

``` powershell
python -m pip install numpy scipy matplotlib
```

## 9. Check the Python File and Run the Analysis

First, check the program's syntax:

``` powershell
python -m py_compile torsional_model.py
```

If this command returns to the prompt without an error message, the
syntax check passed.

Then run the complete analysis:

``` powershell
python torsional_model.py
```

Read the console output and completion messages. Matplotlib figures may
appear in separate windows depending on the local plotting environment.

## 10. What the Program Covers

The completed program has been developed through Step 20:

``` text
Steps 1–10
Engine and shafting inputs, matrices, verification,
natural frequencies, mode shapes, and critical RPMs
             ↓
Step 11
Critical-speed diagram
             ↓
Step 12
Simplified forced torsional response
             ↓
Step 13
Alternating torque and torsional stress
             ↓
Step 14
Shaft-diameter sensitivity
             ↓
Step 15
Shaft stiffness and implied length calculations
             ↓
Step 16
Illustrative shaft geometry and geometry-based stiffness
             ↓
Step 17
Geometry-based natural frequencies and candidate speeds
             ↓
Step 18
Original-versus-geometry-based comparison
             ↓
Step 19
Consolidated model summary
             ↓
Step 20
Critical-RPM comparison visualization
```

## 11. Representative Engine and Original Model

The example uses:

``` text
Engine class:      Sulzer-class representative
Cylinders:         6
Cycle:             2-stroke
Representative power: 12,000 HP
Rated speed:       105 RPM
Operating range:   50–105 RPM
```

Representative rotational inertias:

``` text
J1 = 12,000 kg·m²
J2 =  2,000 kg·m²
J3 =  2,500 kg·m²
J4 = 18,000 kg·m²
```

Original shaft stiffnesses:

``` text
k1 = 23.30 MN·m/rad
k2 = 40.80 MN·m/rad
k3 = 40.80 MN·m/rad
```

These are representative assumptions, not verified data from a
particular production engine.

## 12. Original-Model Natural Frequencies

The three flexible torsional natural frequencies are:

``` text
Mode 1:  6.1509 Hz
Mode 2: 20.2574 Hz
Mode 3: 36.0141 Hz
```

The model also has a rigid-body mode with a frequency effectively equal
to zero.

## 13. Original-Model Candidate Critical RPMs

The program examines excitation orders 6, 12, 18, 24, and 30. Candidate
intersections inside the representative 50--105 RPM operating range are:

  Mode       Order   Candidate speed
  -------- ------- -----------------
  Mode 1       6th         61.51 RPM
  Mode 2      12th        101.29 RPM
  Mode 2      18th         67.52 RPM
  Mode 2      24th         50.64 RPM
  Mode 3      24th         90.04 RPM
  Mode 3      30th         72.03 RPM

A mathematical intersection is a candidate critical speed. It does not,
by itself, prove that harmful resonance will occur.

## 14. Forced Response, Torque, and Stress

The forced-response and stress sections use simplified assumptions,
including representative excitation torque and damping. Their numerical
results depend on those assumptions.

For the most reliable values, run the current saved `torsional_model.py`
and refer to its console output. Do not rely on numbers copied from an
older version of this document if they differ from the current program.

The nominal stress formula used for a solid circular shaft is:

``` text
τ = 16T / (πd³)
```

This is an educational estimate. It is not a fatigue assessment or an
approved shaft-design calculation.

## 15. Shaft-Diameter Sensitivity

Step 14 investigates how the nominal torsional shear-stress estimate
changes with shaft diameter while holding the calculated alternating
torque constant.

The relationship is:

``` text
τ ∝ 1/d³
```

A larger diameter reduces the calculated nominal stress under this
fixed-torque assumption. In a real system, changing diameter also
changes shaft stiffness and may shift natural frequencies and response.

## 16. Step 15 --- Shaft Stiffness and Implied Lengths

Step 15 relates torsional stiffness to shaft geometry using:

``` text
k = GJp / L
Jp = πd⁴ / 32
```

Here, `G` is the shear modulus, `Jp` is the polar second moment of area,
`L` is shaft length, and `d` is the diameter for a solid circular shaft.

The calculated lengths are implied by the selected stiffness, material
modulus, and diameter. They are not confirmed physical lengths of an
actual engine or vessel shaft line.

## 17. Step 16 --- Illustrative Shaft Geometry

Step 16 introduces an illustrative geometry-based case using an assumed
shear modulus of 80 GPa:

  Shaft section     Diameter   Length   Calculated stiffness
  --------------- ---------- -------- ----------------------
  Section 1          0.400 m    8.0 m        25.133 MN·m/rad
  Section 2          0.450 m    8.0 m        40.258 MN·m/rad
  Section 3          0.450 m    8.0 m        40.258 MN·m/rad

These are assumed dimensions for demonstrating the method, not actual
manufacturer data.

## 18. Step 17 --- Geometry-Based Natural Frequencies

The geometry-based case produces these flexible natural frequencies:

``` text
Mode 1:  6.2326 Hz
Mode 2: 20.5097 Hz
Mode 3: 35.9748 Hz
```

The corresponding candidate speeds inside 50--105 RPM are approximately:

``` text
Mode 1,  6th order: 62.33 RPM
Mode 2, 12th order: 102.55 RPM
Mode 2, 18th order: 68.37 RPM
Mode 2, 24th order: 51.27 RPM
Mode 3, 24th order: 89.94 RPM
Mode 3, 30th order: 71.95 RPM
```

These results belong to the illustrative geometry-based model.

## 19. Steps 18--20 --- Comparison and Visualization

Step 18 compares the candidate speeds from the original and
geometry-based models:

  Mode       Order     Original   Geometry-based
  -------- ------- ------------ ----------------
  Mode 1       6th    61.51 RPM        62.33 RPM
  Mode 2      12th   101.29 RPM       102.55 RPM
  Mode 2      18th    67.52 RPM        68.37 RPM
  Mode 2      24th    50.64 RPM        51.27 RPM
  Mode 3      24th    90.04 RPM        89.94 RPM
  Mode 3      30th    72.03 RPM        71.95 RPM

Step 19 consolidates the results. Step 20 creates a visualization of the
critical-RPM comparison.

The Step 20 plot uses circle markers for the original model, X markers
for the geometry-based model, and connecting lines to show the
differences between their predictions. The representative operating
range is 50--105 RPM.

If the plot window does not appear, check the console output first. The
program may have completed without the figure being visible, depending
on the plotting environment. Follow any plot-display instructions
already included in the current program; do not paste Python statements
directly into PowerShell as if they were PowerShell commands.

## 20. Open the Program in Notepad++

If Notepad++ is installed in the standard location, open the program
with:

``` powershell
& "C:\Program Files\Notepad++\notepad++.exe" "C:\dev1\marine-engine-critical-rpm\torsional_model.py"
```

Typing `notepad++ torsional_model.py` may not work unless Notepad++ has
been added to the Windows PATH.

## 21. Editing the Program

If you decide to modify the model:

1.  Make a backup of `torsional_model.py`.
2.  Open the file in Notepad++.
3.  Make the intended changes.
4.  Save with **Ctrl + S**.
5.  Return to PowerShell.
6.  Run the syntax check and then the program:

``` powershell
python -m py_compile torsional_model.py
python torsional_model.py
```

For the completed project, further code changes are optional.

## 22. If PowerShell Blocks Activation

If PowerShell reports an execution-policy error when activating `.venv`,
run:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

This policy change applies only to the current PowerShell session.

## 23. If a Python Package Is Missing

If an error says `ModuleNotFoundError` for NumPy, SciPy, or Matplotlib,
make sure `.venv` is activated and install the packages:

``` powershell
python -m pip install numpy scipy matplotlib
```

Then verify imports:

``` powershell
python -c "import numpy, scipy, matplotlib; print('Required packages are available')"
```

Run the program again:

``` powershell
python torsional_model.py
```

## 24. Stop the Program

To interrupt a running program in PowerShell, press:

``` text
Ctrl + C
```

## 25. Deactivate the Virtual Environment

When finished, you may deactivate the environment:

``` powershell
deactivate
```

This is optional. Closing PowerShell also ends the active terminal
session.

## 26. Recommended Startup Procedure

For an ordinary future session, run these commands in PowerShell:

``` powershell
cd C:\dev1\marine-engine-critical-rpm
.\.venv\Scripts\Activate.ps1
python torsional_model.py
```

To check syntax before running, use:

``` powershell
python -m py_compile torsional_model.py
```

## 27. Engineering Caution

The model uses assumed or representative values for inertias,
stiffnesses, excitation torque, damping, shaft diameter, and
illustrative shaft geometry. Changing these inputs changes the results.

The calculated intersections are candidate critical speeds only. The
project does not validate a real engine or vessel shaft line and must
not be used to establish safe operating limits.

A real marine torsional-vibration study requires actual manufacturer
data, a suitable detailed analysis, and appropriate professional review.

## 28. Project Completion

The educational project is complete through:

``` text
STEP 20 — CRITICAL RPM COMPARISON VISUALIZATION
```

The completed workflow covers:

``` text
✓ Engine and shafting model
✓ Inertia and stiffness matrices
✓ System verification
✓ Natural frequencies and mode shapes
✓ Critical RPM and excitation-order analysis
✓ Critical-speed diagram
✓ Simplified forced response
✓ Alternating torque and nominal torsional stress
✓ Shaft-diameter sensitivity
✓ Implied shaft-length calculation
✓ Illustrative geometry-based stiffness
✓ Geometry-based natural frequencies and candidate speeds
✓ Original-versus-geometry-based comparison
✓ Consolidated summary
✓ Critical-RPM comparison visualization
```

No additional programming step is required just to document the current
educational project.

## 29. Final Command

To run the completed project:

``` powershell
cd C:\dev1\marine-engine-critical-rpm
.\.venv\Scripts\Activate.ps1
python torsional_model.py
```

To perform the syntax check first:

``` powershell
python -m py_compile torsional_model.py
```

Remember: these are educational model results, not approved
marine-engine safety calculations.

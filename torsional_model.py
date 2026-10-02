import numpy as np
from scipy.linalg import eigh


# ============================================================
# MARINE ENGINE TORSIONAL VIBRATION MODEL
# Representative Sulzer-class 2-stroke engine
# ============================================================

print("=" * 70)
print("MARINE ENGINE TORSIONAL VIBRATION MODEL")
print("=" * 70)


# ------------------------------------------------------------
# ENGINE DATA
# ------------------------------------------------------------

engine_name = "Sulzer-class representative engine"

number_of_cylinders = 6
engine_cycle = "2-stroke"

rated_power_hp = 12000
rated_speed_rpm = 105

print("\nENGINE DATA")
print("-" * 70)

print(f"Engine type       : {engine_name}")
print(f"Cylinders         : {number_of_cylinders}")
print(f"Cycle             : {engine_cycle}")
print(f"Rated power       : {rated_power_hp} HP")
print(f"Rated speed       : {rated_speed_rpm} RPM")


# ------------------------------------------------------------
# ROTATIONAL INERTIAS
# ------------------------------------------------------------

J1 = 12000.0     # Engine crankshaft + flywheel
J2 = 2000.0      # Intermediate shaft
J3 = 2500.0      # Tail shaft
J4 = 18000.0     # Propeller + added water inertia


# ------------------------------------------------------------
# TORSIONAL SHAFT STIFFNESSES
# ------------------------------------------------------------

k1 = 23.3e6      # Engine/intermediate shaft connection
k2 = 40.8e6      # Intermediate/tail shaft
k3 = 40.8e6      # Tail shaft/propeller connection


# ------------------------------------------------------------
# DISPLAY MODEL DATA
# ------------------------------------------------------------

print("\nROTATIONAL INERTIAS")
print("-" * 70)

print(f"J1 Engine       : {J1:,.1f} kg*m^2")
print(f"J2 Intermediate : {J2:,.1f} kg*m^2")
print(f"J3 Tail shaft   : {J3:,.1f} kg*m^2")
print(f"J4 Propeller    : {J4:,.1f} kg*m^2")


print("\nTORSIONAL STIFFNESSES")
print("-" * 70)

print(f"k1 : {k1 / 1e6:.2f} MN*m/rad")
print(f"k2 : {k2 / 1e6:.2f} MN*m/rad")
print(f"k3 : {k3 / 1e6:.2f} MN*m/rad")


# ------------------------------------------------------------
# MASS MATRIX
# ------------------------------------------------------------

M = np.array([
    [J1, 0,  0,  0],
    [0,  J2, 0,  0],
    [0,  0,  J3, 0],
    [0,  0,  0,  J4]
])


# ------------------------------------------------------------
# STIFFNESS MATRIX
# ------------------------------------------------------------

K = np.array([
    [ k1,       -k1,          0,          0],
    [-k1,   k1 + k2,        -k2,          0],
    [  0,       -k2,   k2 + k3,        -k3],
    [  0,         0,        -k3,         k3]
])


# ------------------------------------------------------------
# DISPLAY MATRICES
# ------------------------------------------------------------

print("\nMASS MATRIX M")
print("-" * 70)
print(M)


print("\nSTIFFNESS MATRIX K")
print("-" * 70)
print(K)


# ------------------------------------------------------------
# EIGENVALUE SOLUTION
#
#     K * phi = omega^2 * M * phi
#
# eigh() solves the generalized symmetric eigenvalue problem.
# ------------------------------------------------------------

eigenvalues, eigenvectors = eigh(K, M)


# Numerical round-off can produce a tiny negative value
# for the rigid-body eigenvalue, so protect the square root.

eigenvalues = np.maximum(eigenvalues, 0.0)


# Natural angular frequencies
omega = np.sqrt(eigenvalues)


# Natural frequencies in Hz
frequency_hz = omega / (2.0 * np.pi)


# ------------------------------------------------------------
# DISPLAY NATURAL FREQUENCIES
# ------------------------------------------------------------

print("\nNATURAL FREQUENCIES")
print("-" * 70)

for i, frequency in enumerate(frequency_hz):

    if frequency < 0.001:
        print(f"Mode {i + 1}: rigid-body mode")
        print(f"         frequency = {frequency:.6e} Hz")

    else:
        print(f"Mode {i + 1}: torsional mode")
        print(f"         frequency = {frequency:.4f} Hz")


# ------------------------------------------------------------
# DISPLAY MODE SHAPES
# ------------------------------------------------------------

print("\nMODE SHAPES")
print("-" * 70)

for mode in range(len(frequency_hz)):

    print(f"\nMode {mode + 1}:")

    for mass in range(4):
        print(
            f"  J{mass + 1}: "
            f"{eigenvectors[mass, mode]: .6f}"
        )


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Rated engine speed : {rated_speed_rpm} RPM")

print("\nNon-zero torsional natural frequencies:")

for i, frequency in enumerate(frequency_hz):

    if frequency >= 0.001:
        print(
            f"  Mode {i}: "
            f"{frequency:.4f} Hz"
        )

print("\nTorsional model calculation complete.")
print("=" * 70)

# ============================================================
# STEP 9
# CRITICAL RPM CALCULATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 9 - CRITICAL RPM CALCULATION")
print("=" * 70)

# ------------------------------------------------------------
# ENGINE OPERATING DATA
# ------------------------------------------------------------

number_of_cylinders = 6
rated_rpm = 105.0
minimum_rpm = 50.0

# For a 2-stroke engine:
# one firing event per cylinder per revolution.
#
# Therefore the main firing excitation order is equal
# to the number of cylinders.

firing_order = number_of_cylinders

print("\nENGINE EXCITATION")
print("-" * 70)

print(f"Number of cylinders : {number_of_cylinders}")
print("Engine cycle        : 2-stroke")
print(f"Main firing order   : {firing_order}th order")
print(f"Operating range     : {minimum_rpm:.1f} - {rated_rpm:.1f} RPM")


# ------------------------------------------------------------
# CALCULATE CRITICAL RPM
# ------------------------------------------------------------

print("\nCRITICAL RPM RESULTS")
print("-" * 70)

critical_rpms = []

for i, fn in enumerate(frequency_hz):

    if fn < 0.01:
        continue

    critical_rpm = 60.0 * fn / firing_order

    critical_rpms.append((i + 1, fn, critical_rpm))

    print(
        f"Mode {i + 1}: "
        f"natural frequency = {fn:.4f} Hz, "
        f"critical RPM = {critical_rpm:.2f} RPM"
    )


# ------------------------------------------------------------
# CHECK WHETHER CRITICAL RPM IS INSIDE OPERATING RANGE
# ------------------------------------------------------------

print("\nOPERATING RANGE CHECK")
print("-" * 70)

for mode, fn, critical_rpm in critical_rpms:

    if minimum_rpm <= critical_rpm <= rated_rpm:

        print(
            f"Mode {mode}: "
            f"{critical_rpm:.2f} RPM "
            f"--> INSIDE operating range"
        )

    elif critical_rpm < minimum_rpm:

        print(
            f"Mode {mode}: "
            f"{critical_rpm:.2f} RPM "
            f"--> BELOW operating range"
        )

    else:

        print(
            f"Mode {mode}: "
            f"{critical_rpm:.2f} RPM "
            f"--> ABOVE operating range"
        )


# ------------------------------------------------------------
# FINAL ENGINEERING RESULT
# ------------------------------------------------------------

print("\nENGINEERING RESULT")
print("-" * 70)

for mode, fn, critical_rpm in critical_rpms:

    if minimum_rpm <= critical_rpm <= rated_rpm:

        print(
            f"Candidate critical speed: "
            f"{critical_rpm:.2f} RPM "
            f"(Mode {mode}, {firing_order}th order)"
        )

print("\n" + "=" * 70)
print("STEP 9 COMPLETE")
print("=" * 70)

# ============================================================
# STEP 10
# MULTIPLE TORSIONAL EXCITATION ORDERS
# ============================================================

print("\n" + "=" * 70)
print("STEP 10 - MULTIPLE TORSIONAL EXCITATION ORDERS")
print("=" * 70)


# ------------------------------------------------------------
# EXCITATION ORDERS TO INVESTIGATE
# ------------------------------------------------------------

excitation_orders = [6, 12, 18, 24, 30]


# ------------------------------------------------------------
# DISPLAY EXCITATION ORDERS
# ------------------------------------------------------------

print("\nEXCITATION ORDERS")
print("-" * 70)

print(
    "For a 6-cylinder, 2-stroke engine, "
    "the main firing order is 6."
)

print(
    "Higher harmonics are also examined because "
    "the engine torque waveform is not perfectly sinusoidal."
)

print(f"\nOrders investigated: {excitation_orders}")


# ------------------------------------------------------------
# CALCULATE ALL CRITICAL RPM INTERSECTIONS
# ------------------------------------------------------------

print("\nCRITICAL RPM TABLE")
print("-" * 70)

print(
    f"{'Mode':>6} "
    f"{'Natural Hz':>14} "
    f"{'Order':>8} "
    f"{'Critical RPM':>16} "
    f"{'Operating Range':>20}"
)

print("-" * 70)


critical_intersections = []


for mode, fn, _ in critical_rpms:

    for order in excitation_orders:

        critical_rpm = 60.0 * fn / order

        if minimum_rpm <= critical_rpm <= rated_rpm:
            range_status = "INSIDE"

        elif critical_rpm < minimum_rpm:
            range_status = "BELOW"

        else:
            range_status = "ABOVE"

        critical_intersections.append(
            (mode, fn, order, critical_rpm, range_status)
        )

        print(
            f"{mode:>6} "
            f"{fn:>14.4f} "
            f"{order:>8} "
            f"{critical_rpm:>16.2f} "
            f"{range_status:>20}"
        )


# ------------------------------------------------------------
# FIND INTERSECTIONS INSIDE OPERATING RANGE
# ------------------------------------------------------------

print("\nCRITICAL SPEEDS INSIDE ENGINE OPERATING RANGE")
print("-" * 70)

inside_range = []

for mode, fn, order, critical_rpm, range_status in critical_intersections:

    if range_status == "INSIDE":

        inside_range.append(
            (mode, fn, order, critical_rpm)
        )

        print(
            f"Mode {mode}, "
            f"{order}th order: "
            f"{critical_rpm:.2f} RPM"
        )


# ------------------------------------------------------------
# COUNT POSSIBLE INTERSECTIONS
# ------------------------------------------------------------

print("\nSUMMARY OF OPERATING-RANGE INTERSECTIONS")
print("-" * 70)

print(
    f"Number of mathematical intersections "
    f"inside {minimum_rpm:.0f}-{rated_rpm:.0f} RPM: "
    f"{len(inside_range)}"
)


# ------------------------------------------------------------
# ENGINEERING WARNING
# ------------------------------------------------------------

if len(inside_range) > 0:

    print("\nIMPORTANT ENGINEERING NOTE")
    print("-" * 70)

    print(
        "The intersections listed above are candidate "
        "torsional critical speeds."
    )

    print(
        "An intersection does NOT by itself prove that "
        "dangerous resonance will occur."
    )

    print(
        "Actual vibration severity depends on excitation "
        "torque, damping, mode shape, shaft geometry, "
        "and engine operating conditions."
    )


# ------------------------------------------------------------
# STEP 10 COMPLETE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 10 COMPLETE")
print("=" * 70)

# ============================================================
# STEP 11
# CRITICAL-SPEED DIAGRAM
# ============================================================

import matplotlib.pyplot as plt


print("\n" + "=" * 70)
print("STEP 11 - CRITICAL-SPEED DIAGRAM")
print("=" * 70)


# ------------------------------------------------------------
# ENGINE SPEED RANGE
# ------------------------------------------------------------

rpm_values = np.linspace(
    minimum_rpm,
    rated_rpm,
    500
)


# ------------------------------------------------------------
# CREATE FIGURE
# ------------------------------------------------------------

plt.figure(figsize=(11, 7))


# ------------------------------------------------------------
# PLOT EXCITATION ORDERS
# ------------------------------------------------------------

for order in excitation_orders:

    excitation_frequency = (
        order * rpm_values / 60.0
    )

    plt.plot(
        rpm_values,
        excitation_frequency,
        label=f"{order}th order"
    )


# ------------------------------------------------------------
# PLOT NATURAL FREQUENCIES
# ------------------------------------------------------------

for mode, fn, _ in critical_rpms:

    plt.axhline(
        y=fn,
        linestyle="--",
        label=f"Mode {mode}: {fn:.2f} Hz"
    )


# ------------------------------------------------------------
# MARK CRITICAL INTERSECTIONS
# ------------------------------------------------------------

for mode, fn, order, critical_rpm, range_status in critical_intersections:

    if range_status == "INSIDE":

        plt.plot(
            critical_rpm,
            fn,
            marker="o",
            markersize=7
        )

        plt.annotate(
            f"{critical_rpm:.1f} RPM",
            (critical_rpm, fn),
            xytext=(5, 8),
            textcoords="offset points"
        )


# ------------------------------------------------------------
# AXIS LABELS
# ------------------------------------------------------------

plt.xlabel("Engine Speed [RPM]")

plt.ylabel("Excitation Frequency [Hz]")

plt.title(
    "Marine Engine Torsional Critical-Speed Diagram"
)


# ------------------------------------------------------------
# GRID AND LIMITS
# ------------------------------------------------------------

plt.grid(True)

plt.xlim(
    minimum_rpm,
    rated_rpm
)

plt.ylim(
    0,
    40
)


# ------------------------------------------------------------
# LEGEND
# ------------------------------------------------------------

plt.legend(
    loc="upper left",
    fontsize=9
)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

plt.tight_layout()

plt.show()


print("\nCritical-speed diagram displayed.")

print("\n" + "=" * 70)
print("STEP 11 COMPLETE")
print("=" * 70)

# ============================================================
# STEP 12
# FORCED TORSIONAL VIBRATION RESPONSE
# ============================================================

print("\n" + "=" * 70)
print("STEP 12 - FORCED TORSIONAL VIBRATION RESPONSE")
print("=" * 70)


# ------------------------------------------------------------
# SIMPLIFIED DAMPING
# ------------------------------------------------------------
#
# We use a small damping ratio for this educational
# engineering model.
#
# This is NOT measured damping for a real Sulzer engine.
# ------------------------------------------------------------

damping_ratio = 0.03


# ------------------------------------------------------------
# EXCITATION TORQUE
# ------------------------------------------------------------
#
# Simplified harmonic torque amplitude.
#
# The value is illustrative and is used to demonstrate
# the resonance response.
# ------------------------------------------------------------

excitation_torque = 1.0e6       # N*m


# ------------------------------------------------------------
# SELECT FIRST TORSIONAL MODE
# ------------------------------------------------------------

first_mode_frequency = critical_rpms[0][1]

first_mode_omega = (
    2.0 * np.pi * first_mode_frequency
)


# ------------------------------------------------------------
# SPEED RANGE
# ------------------------------------------------------------

rpm_response = np.linspace(
    minimum_rpm,
    rated_rpm,
    1000
)


# ------------------------------------------------------------
# EXCITATION FREQUENCY
# ------------------------------------------------------------

excitation_frequency = (
    firing_order * rpm_response / 60.0
)

excitation_omega = (
    2.0 * np.pi * excitation_frequency
)


# ------------------------------------------------------------
# FREQUENCY RATIO
# ------------------------------------------------------------

frequency_ratio = (
    excitation_omega /
    first_mode_omega
)


# ------------------------------------------------------------
# SIMPLIFIED SINGLE-MODE RESPONSE
# ------------------------------------------------------------
#
# Dynamic magnification factor:
#
#       1
# ----------------
# sqrt((1-r^2)^2 + (2*zeta*r)^2)
#
# ------------------------------------------------------------

dynamic_magnification = (
    1.0 /
    np.sqrt(
        (1.0 - frequency_ratio**2)**2
        +
        (2.0 * damping_ratio * frequency_ratio)**2
    )
)


# ------------------------------------------------------------
# STATIC TORSIONAL ANGLE
# ------------------------------------------------------------

static_angle = (
    excitation_torque /
    k1
)


# ------------------------------------------------------------
# DYNAMIC TORSIONAL ANGLE
# ------------------------------------------------------------

torsional_angle = (
    static_angle *
    dynamic_magnification
)


# ------------------------------------------------------------
# CONVERT TO DEGREES
# ------------------------------------------------------------

torsional_angle_deg = (
    torsional_angle *
    180.0 /
    np.pi
)


# ------------------------------------------------------------
# FIND MAXIMUM RESPONSE
# ------------------------------------------------------------

maximum_index = np.argmax(
    torsional_angle_deg
)

maximum_rpm = (
    rpm_response[maximum_index]
)

maximum_angle = (
    torsional_angle_deg[maximum_index]
)


# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------

print("\nFORCED RESPONSE PARAMETERS")
print("-" * 70)

print(
    f"Damping ratio              : "
    f"{damping_ratio:.3f}"
)

print(
    f"Excitation torque amplitude: "
    f"{excitation_torque:,.0f} N*m"
)

print(
    f"Static torsional angle     : "
    f"{static_angle:.6f} rad"
)

print(
    f"Static torsional angle     : "
    f"{static_angle * 180.0 / np.pi:.6f} deg"
)


print("\nMAXIMUM SIMPLIFIED RESPONSE")
print("-" * 70)

print(
    f"Engine speed               : "
    f"{maximum_rpm:.2f} RPM"
)

print(
    f"Torsional angle amplitude : "
    f"{maximum_angle:.6f} deg"
)


# ------------------------------------------------------------
# PLOT FORCED RESPONSE
# ------------------------------------------------------------

plt.figure(figsize=(11, 7))

plt.plot(
    rpm_response,
    torsional_angle_deg
)

plt.axvline(
    61.51,
    linestyle="--",
    label="Candidate critical speed: 61.51 RPM"
)

plt.xlabel(
    "Engine Speed [RPM]"
)

plt.ylabel(
    "Torsional Angle Amplitude [deg]"
)

plt.title(
    "Simplified 6th-Order Forced Torsional Response"
)

plt.grid(True)

plt.xlim(
    minimum_rpm,
    rated_rpm
)

plt.legend()

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# STEP 12 COMPLETE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 12 COMPLETE")
print("=" * 70)

# ============================================================
# ============================================================
# STEP 13 - TORSIONAL VIBRATION STRESS
# ============================================================

print()
print("=" * 70)
print("STEP 13 - TORSIONAL VIBRATION STRESS")
print("=" * 70)

# ------------------------------------------------------------
# Representative shaft diameter
# ------------------------------------------------------------

shaft_diameter = 0.800       # m

# ------------------------------------------------------------
# Find maximum torsional angle directly from Step 12 data
# ------------------------------------------------------------

max_response_index = np.argmax(torsional_angle_deg)

maximum_torsional_angle_deg = torsional_angle_deg[max_response_index]

maximum_angle_rad = np.deg2rad(maximum_torsional_angle_deg)

# ------------------------------------------------------------
# Alternating torsional torque
#
# T = k * theta
# ------------------------------------------------------------

alternating_torque = k1 * maximum_angle_rad

# ------------------------------------------------------------
# Torsional shear stress for a solid circular shaft
#
# tau = 16*T / (pi*d^3)
# ------------------------------------------------------------

torsional_stress = (
    16.0 * alternating_torque
    / (np.pi * shaft_diameter**3)
)

torsional_stress_mpa = torsional_stress / 1.0e6

# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print()
print("SHAFT STRESS PARAMETERS")
print("-" * 70)

print(f"Shaft diameter             : {shaft_diameter:.3f} m")
print(f"Maximum torsional angle    : {maximum_torsional_angle_deg:.6f} deg")
print(f"Maximum torsional angle    : {maximum_angle_rad:.6f} rad")

print()
print("ALTERNATING TORSIONAL TORQUE")
print("-" * 70)

print(f"Alternating torque         : {alternating_torque:,.0f} N*m")
print(f"Alternating torque         : {alternating_torque / 1.0e6:.3f} MN*m")

print()
print("TORSIONAL SHEAR STRESS")
print("-" * 70)

print(f"Shear stress               : {torsional_stress:,.0f} Pa")
print(f"Shear stress               : {torsional_stress_mpa:.3f} MPa")

print()
print("=" * 70)
print("STEP 13 COMPLETE")
print("=" * 70)

# ============================================================
# STEP 14 - SHAFT DIAMETER SENSITIVITY ANALYSIS
# ============================================================

print()
print("=" * 70)
print("STEP 14 - SHAFT DIAMETER SENSITIVITY ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# Shaft diameters to investigate
# ------------------------------------------------------------

diameters = np.arange(0.60, 1.01, 0.05)

# ------------------------------------------------------------
# Calculate torsional shear stress for each diameter
#
# tau = 16*T / (pi*d^3)
# ------------------------------------------------------------

stress_values = (
    16.0 * alternating_torque
    / (np.pi * diameters**3)
)

stress_values_mpa = stress_values / 1.0e6

# ------------------------------------------------------------
# Print results table
# ------------------------------------------------------------

print()
print("SHAFT DIAMETER / TORSIONAL STRESS")
print("-" * 70)

print(f"{'Diameter (m)':>15} {'Stress (MPa)':>20}")
print("-" * 70)

for diameter, stress in zip(diameters, stress_values_mpa):
    print(f"{diameter:>15.2f} {stress:>20.3f}")

# ------------------------------------------------------------
# Plot stress versus shaft diameter
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    diameters,
    stress_values_mpa,
    linewidth=2
)

plt.scatter(
    [shaft_diameter],
    [torsional_stress_mpa],
    s=80,
    label="Step 13 shaft"
)

plt.xlabel("Shaft diameter (m)")
plt.ylabel("Torsional shear stress (MPa)")
plt.title("Torsional Shear Stress vs Shaft Diameter")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Step 14 complete
# ------------------------------------------------------------

print()
print("=" * 70)
print("STEP 14 COMPLETE")
print("=" * 70)
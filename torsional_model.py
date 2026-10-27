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
# FOUR-INERTIA MODAL FORCED TORSIONAL VIBRATION RESPONSE
# ============================================================

print("\n" + "=" * 70)
print("STEP 12 - FOUR-INERTIA MODAL FORCED RESPONSE")
print("=" * 70)

# ------------------------------------------------------------
# MODAL DAMPING
# ------------------------------------------------------------
# Illustrative damping ratio for every flexible torsional mode.
# This is not measured damping data for a real engine.
# ------------------------------------------------------------

damping_ratio = 0.03

# ------------------------------------------------------------
# ILLUSTRATIVE HARMONIC EXCITATION TORQUE
# ------------------------------------------------------------
# Assumed torque amplitudes:
#   +T at inertia J1 (engine end)
#   -T at inertia J4 (propeller end)
#    0 at the two intermediate inertias
#
# The equal and opposite torques give zero net external torque,
# avoiding excitation of the free rigid-body rotation mode.
#
# This is an illustrative excitation pattern, not a measured
# engine torque distribution.
# ------------------------------------------------------------

excitation_torque = 1.0e6  # N*m

force_vector = np.array([
    excitation_torque,
    0.0,
    0.0,
    -excitation_torque
])

# ------------------------------------------------------------
# SELECT FLEXIBLE TORSIONAL MODES
# ------------------------------------------------------------
# The eigenvalue solution contains a near-zero rigid-body mode.
# Exclude that mode from the forced flexible-mode calculation.
# ------------------------------------------------------------

nonzero_modes = np.where(frequency_hz >= 0.001)[0]

Phi = eigenvectors[:, nonzero_modes]
omega_n = omega[nonzero_modes]

modal_force = Phi.T @ force_vector

print("\nMODAL RESPONSE PARAMETERS")
print("-" * 70)

print(f"Modal damping ratio        : {damping_ratio:.3f}")
print(f"Excitation torque amplitude: {excitation_torque:,.0f} N*m")
print(f"Flexible modes included    : {len(nonzero_modes)}")

# ------------------------------------------------------------
# ENGINE SPEED RANGE
# ------------------------------------------------------------

rpm_response = np.linspace(
    minimum_rpm,
    rated_rpm,
    1000
)

# ------------------------------------------------------------
# EXCITATION FREQUENCY
# ------------------------------------------------------------
# The selected excitation is the engine firing order.
# For the current six-cylinder, two-stroke example, the
# firing order is six if firing_order = 6 in the earlier code.
# ------------------------------------------------------------

excitation_frequency = (
    firing_order * rpm_response / 60.0
)

excitation_omega = (
    2.0 * np.pi * excitation_frequency
)

# ------------------------------------------------------------
# COMPLEX MODAL RESPONSE
# ------------------------------------------------------------
# For each flexible mode:
#
# q_i = Q_i /
#       (omega_n_i^2 - omega_exc^2
#        + j * 2 * zeta * omega_n_i * omega_exc)
#
# The eigenvectors returned by scipy.linalg.eigh(K, M) are
# mass-normalized, so this expression uses modal mass = 1.
# ------------------------------------------------------------

response_complex = np.zeros(
    (4, len(rpm_response)),
    dtype=complex
)

for j, omega_exc in enumerate(excitation_omega):

    denominator = (
        omega_n**2
        - omega_exc**2
        + 1j
        * 2.0
        * damping_ratio
        * omega_n
        * omega_exc
    )

    modal_response = modal_force / denominator

    response_complex[:, j] = Phi @ modal_response

# ------------------------------------------------------------
# RELATIVE TWIST ACROSS EACH SHAFT SECTION
# ------------------------------------------------------------
# Absolute angular displacement is not the same as shaft twist.
# Shaft twist is the difference between adjacent inertias.
# ------------------------------------------------------------

relative_twist_1 = (
    response_complex[0, :]
    - response_complex[1, :]
)

relative_twist_2 = (
    response_complex[1, :]
    - response_complex[2, :]
)

relative_twist_3 = (
    response_complex[2, :]
    - response_complex[3, :]
)

relative_twist_1_deg = np.rad2deg(
    np.abs(relative_twist_1)
)

relative_twist_2_deg = np.rad2deg(
    np.abs(relative_twist_2)
)

relative_twist_3_deg = np.rad2deg(
    np.abs(relative_twist_3)
)

# Preserve this variable name because Step 13 uses it.
# It now represents twist across shaft section 1 (J1-J2).
torsional_angle_deg = relative_twist_1_deg

# ------------------------------------------------------------
# FIND MAXIMUM TWIST IN SHAFT SECTION 1
# ------------------------------------------------------------

maximum_index = np.argmax(torsional_angle_deg)

maximum_rpm = rpm_response[maximum_index]

maximum_angle = torsional_angle_deg[maximum_index]

# First flexible-mode crossing for the selected firing order.
first_mode_critical_rpm = (
    60.0
    * omega_n[0]
    / (2.0 * np.pi * firing_order)
)

# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------

print("\nMAXIMUM RELATIVE TWIST - SHAFT SECTION 1 (J1-J2)")
print("-" * 70)

print(f"Engine speed               : {maximum_rpm:.2f} RPM")
print(f"Twist amplitude             : {maximum_angle:.6f} deg")
print(f"Twist amplitude             : {np.deg2rad(maximum_angle):.8f} rad")

print("\nMAXIMUM TWIST BY SHAFT SECTION")
print("-" * 70)

print(
    f"Section 1 (J1-J2): "
    f"{np.max(relative_twist_1_deg):.6f} deg"
)

print(
    f"Section 2 (J2-J3): "
    f"{np.max(relative_twist_2_deg):.6f} deg"
)

print(
    f"Section 3 (J3-J4): "
    f"{np.max(relative_twist_3_deg):.6f} deg"
)

print("\nFIRST FLEXIBLE-MODE CROSSING")
print("-" * 70)

print(
    f"Candidate speed for the selected firing order: "
    f"{first_mode_critical_rpm:.2f} RPM"
)

# ------------------------------------------------------------
# PLOT RELATIVE TWIST RESPONSE
# ------------------------------------------------------------

plt.figure(figsize=(11, 7))

plt.plot(
    rpm_response,
    relative_twist_1_deg,
    label="Shaft section 1 (J1-J2)"
)

plt.plot(
    rpm_response,
    relative_twist_2_deg,
    label="Shaft section 2 (J2-J3)"
)

plt.plot(
    rpm_response,
    relative_twist_3_deg,
    label="Shaft section 3 (J3-J4)"
)

plt.axvline(
    first_mode_critical_rpm,
    linestyle="--",
    label=(
        f"First-mode crossing: "
        f"{first_mode_critical_rpm:.2f} RPM"
    )
)

plt.xlabel("Engine Speed [RPM]")

plt.ylabel("Relative Twist Amplitude [deg]")

plt.title(
    "Four-Inertia Modal Forced Torsional Response"
)

plt.grid(True)

plt.xlim(minimum_rpm, rated_rpm)

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

# ============================================================
# STEP 15 - SHAFT STIFFNESS AND GEOMETRY CONSISTENCY CHECK
# ============================================================

print("\n" + "=" * 70)
print("STEP 15 - SHAFT STIFFNESS AND GEOMETRY CONSISTENCY")
print("=" * 70)

# ------------------------------------------------------------
# ASSUMED MATERIAL AND SHAFT DIAMETER
# ------------------------------------------------------------
# Illustrative assumptions, not verified data for a real engine.
# ------------------------------------------------------------

shear_modulus = 80.0e9       # Pa = 80 GPa
reference_diameter = 0.800   # m; diameter assumed in Step 13

# Torsional stiffness values from the four-inertia model.
shaft_stiffnesses = {
    "Section 1 (J1-J2)": 23.30e6,
    "Section 2 (J2-J3)": 40.80e6,
    "Section 3 (J3-J4)": 40.80e6,
}

# ------------------------------------------------------------
# POLAR SECOND MOMENT OF AREA
# ------------------------------------------------------------
# For a solid circular shaft:
# Jp = pi * d^4 / 32
# ------------------------------------------------------------

polar_moment = (
    np.pi * reference_diameter**4 / 32.0
)

# ------------------------------------------------------------
# IMPLIED SHAFT LENGTH
# ------------------------------------------------------------
# From k = G * Jp / L:
# L = G * Jp / k
#
# The same reference diameter is used for all three sections
# solely to compare the assumed stiffness values.
# ------------------------------------------------------------

print("\nASSUMPTIONS")
print("-" * 70)

print(f"Shear modulus             : {shear_modulus / 1e9:.1f} GPa")
print(f"Reference shaft diameter  : {reference_diameter:.3f} m")
print(f"Polar second moment Jp    : {polar_moment:.6f} m^4")

print("\nIMPLIED LENGTH FOR EACH STIFFNESS")
print("-" * 70)

print(
    f"{'Shaft section':<25}"
    f"{'Stiffness (MN*m/rad)':>24}"
    f"{'Implied length (m)':>23}"
)

print("-" * 72)

for section, stiffness in shaft_stiffnesses.items():

    implied_length = (
        shear_modulus
        * polar_moment
        / stiffness
    )

    print(
        f"{section:<25}"
        f"{stiffness / 1e6:>24.2f}"
        f"{implied_length:>23.2f}"
    )

# ------------------------------------------------------------
# ENGINEERING INTERPRETATION
# ------------------------------------------------------------

print("\nENGINEERING INTERPRETATION")
print("-" * 70)

print(
    "The calculated lengths follow from the assumed diameter,"
)

print(
    "material shear modulus, and torsional stiffness."
)

print(
    "They are implied lengths, not actual shaft dimensions."
)

print(
    "Actual shaft diameters, effective lengths, material"
)

print(
    "properties, and coupling details must be established"
)

print(
    "before the model can be validated against a real engine."
)

print(
    "Do not use these results alone to approve shaft strength"
)

print(
    "or determine safe operating speeds."
)

print("\n" + "=" * 70)
print("STEP 15 COMPLETE")
print("=" * 70)



# ============================================================
# STEP 16 - ILLUSTRATIVE SHAFT GEOMETRY MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 16 - ILLUSTRATIVE SHAFT GEOMETRY MODEL")
print("=" * 70)

# ------------------------------------------------------------
# EDUCATIONAL ASSUMPTIONS ONLY
# ------------------------------------------------------------
# These dimensions do NOT represent verified Sulzer engine data.
#
# Each entry contains:
# section name, diameter (m), length (m), existing stiffness
# (N*m/rad) from the original four-inertia model.
# ------------------------------------------------------------

geometry_shear_modulus = 80.0e9  # Pa; illustrative steel value

illustrative_sections = [
    {
        "name": "Section 1 (J1-J2)",
        "diameter": 0.400,
        "length": 8.0,
        "existing_stiffness": 23.30e6,
    },
    {
        "name": "Section 2 (J2-J3)",
        "diameter": 0.450,
        "length": 8.0,
        "existing_stiffness": 40.80e6,
    },
    {
        "name": "Section 3 (J3-J4)",
        "diameter": 0.450,
        "length": 8.0,
        "existing_stiffness": 40.80e6,
    },
]

# ------------------------------------------------------------
# CALCULATE GEOMETRY-BASED TORSIONAL STIFFNESS
# ------------------------------------------------------------
# For a solid circular shaft:
#
# Jp = pi * d^4 / 32
# k  = G * Jp / L
#
# These calculations assume uniform, solid circular shafts.
# They do not include couplings, flanges, hollow sections,
# crankshaft geometry, or other local flexibility.
# ------------------------------------------------------------

print("\nILLUSTRATIVE MATERIAL AND GEOMETRY")
print("-" * 70)

print(
    f"Assumed shear modulus: "
    f"{geometry_shear_modulus / 1e9:.1f} GPa"
)

print("Assumed shaft material: steel")
print("Assumed shaft type    : solid circular sections")

print("\nGEOMETRY-BASED STIFFNESS COMPARISON")
print("-" * 70)

print(
    f"{'Section':<22}"
    f"{'Diameter (m)':>14}"
    f"{'Length (m)':>13}"
    f"{'Calculated k':>18}"
    f"{'Difference':>14}"
)

print("-" * 81)

geometry_stiffnesses = []

for section in illustrative_sections:

    diameter = section["diameter"]
    length = section["length"]

    polar_moment_geometry = (
        np.pi * diameter**4 / 32.0
    )

    calculated_stiffness = (
        geometry_shear_modulus
        * polar_moment_geometry
        / length
    )

    existing_stiffness = section["existing_stiffness"]

    difference_percent = (
        (calculated_stiffness - existing_stiffness)
        / existing_stiffness
        * 100.0
    )

    geometry_stiffnesses.append(calculated_stiffness)

    print(
        f"{section['name']:<22}"
        f"{diameter:>14.3f}"
        f"{length:>13.2f}"
        f"{calculated_stiffness / 1e6:>15.3f} MN"
        f"{difference_percent:>+12.2f}%"
    )

# ------------------------------------------------------------
# ENGINEERING INTERPRETATION
# ------------------------------------------------------------

print("\nENGINEERING INTERPRETATION")
print("-" * 70)

print(
    "The calculated stiffnesses follow from the assumed"
)

print(
    "diameters, lengths, and material shear modulus."
)

print(
    "The percentage difference compares them with the"
)

print(
    "original model's assumed stiffness values."
)

print(
    "The original mass and stiffness matrices have NOT been"
)

print(
    "changed by this step; earlier modal results are unchanged."
)

print(
    "These illustrative dimensions are not verified engine data."
)

print("\n" + "=" * 70)
print("STEP 16 COMPLETE")
print("=" * 70)


# ================================================================
# STEP 17: NATURAL FREQUENCIES AND CRITICAL RPM USING GEOMETRY-BASED
#          SHAFT STIFFNESSES
# ================================================================

print("\n" + "=" * 72)
print("STEP 17: GEOMETRY-BASED NATURAL FREQUENCIES AND CRITICAL RPM")
print("=" * 72)

# These stiffnesses were calculated in Step 16 from illustrative
# shaft diameters, lengths, and the assumed shear modulus.
# They are NOT verified dimensions or stiffnesses for a real engine.

k1_geometry = geometry_stiffnesses[0]
k2_geometry = geometry_stiffnesses[1]
k3_geometry = geometry_stiffnesses[2]

# Build a NEW stiffness matrix.
# Do not modify the original matrix K.

K_geometry = np.array([
    [k1_geometry, -k1_geometry, 0.0, 0.0],
    [-k1_geometry, k1_geometry + k2_geometry, -k2_geometry, 0.0],
    [0.0, -k2_geometry, k2_geometry + k3_geometry, -k3_geometry],
    [0.0, 0.0, -k3_geometry, k3_geometry]
], dtype=float)

# Solve the generalized eigenvalue problem using the existing
# mass matrix M and the new geometry-based stiffness matrix.

eigenvalues_geometry, eigenvectors_geometry = eigh(K_geometry, M)

# Convert eigenvalues to angular frequencies and then to Hz.
# Clipping protects against tiny negative numerical round-off
# values for the theoretical zero-frequency rigid-body mode.

omega_geometry = np.sqrt(np.clip(eigenvalues_geometry, 0.0, None))
frequency_hz_geometry = omega_geometry / (2.0 * np.pi)

# Exclude the rigid-body mode from the flexible-mode comparison.
flexible_frequencies_geometry = frequency_hz_geometry[
    frequency_hz_geometry > 0.001
]

print("\n1. GEOMETRY-BASED SHAFT STIFFNESSES")
print("-" * 72)
print(f"Section 1 stiffness: {k1_geometry / 1e6:.3f} MN*m/rad")
print(f"Section 2 stiffness: {k2_geometry / 1e6:.3f} MN*m/rad")
print(f"Section 3 stiffness: {k3_geometry / 1e6:.3f} MN*m/rad")

print("\n2. NATURAL FREQUENCIES: ORIGINAL MODEL VS GEOMETRY-BASED MODEL")
print("-" * 72)
print(f"{'Flexible mode':<18}{'Original (Hz)':>18}{'Geometry-based (Hz)':>25}")

# The original frequency_hz array was calculated earlier in the script.
flexible_frequencies_original = np.asarray(frequency_hz)
flexible_frequencies_original = flexible_frequencies_original[
    flexible_frequencies_original > 0.001
]

number_of_modes = min(
    len(flexible_frequencies_original),
    len(flexible_frequencies_geometry)
)

for i in range(number_of_modes):
    print(
        f"{i + 1:<18}"
        f"{flexible_frequencies_original[i]:>18.4f}"
        f"{flexible_frequencies_geometry[i]:>25.4f}"
    )

# Calculate possible critical RPM values for several engine-order
# excitations. Only show values within the 50–105 RPM operating range.
# Formula: critical RPM = natural frequency (Hz) * 60 / engine order.

geometry_excitation_orders = [6, 12, 18, 24, 30]
geometry_minimum_rpm = 50.0
geometry_rated_rpm = 105.0

print("\n3. POSSIBLE CRITICAL RPM VALUES")
print("-" * 72)
print(f"Operating range: {geometry_minimum_rpm:.1f}–{geometry_rated_rpm:.1f} RPM")
print("Only intersections inside this range are listed.")
print(f"{'Mode':<8}{'Frequency (Hz)':>18}{'Order':>12}{'Critical RPM':>18}")

geometry_critical_count = 0

for mode_index, natural_frequency in enumerate(
    flexible_frequencies_geometry, start=1
):
    for order in geometry_excitation_orders:
        critical_rpm = 60.0 * natural_frequency / order

        if geometry_minimum_rpm <= critical_rpm <= geometry_rated_rpm:
            print(
                f"{mode_index:<8}"
                f"{natural_frequency:>18.4f}"
                f"{order:>12}"
                f"{critical_rpm:>18.2f}"
            )
            geometry_critical_count += 1

if geometry_critical_count == 0:
    print("No calculated intersections fall inside the specified range.")

print("\n4. IMPORTANT INTERPRETATION")
print("-" * 72)
print("These are theoretical calculations using illustrative shaft geometry.")
print("A calculated critical RPM is a candidate for further investigation,")
print("not proof that harmful resonance will occur at that speed.")
print("Real-engine assessment requires verified inertias, shaft geometry,")
print("excitation torques, damping, and validation by a qualified engineer.")

print("\nSTEP 17 COMPLETE")
print("=" * 72)


# ================================================================
# STEP 18: COMPARE ORIGINAL AND GEOMETRY-BASED CRITICAL RPM VALUES
# ================================================================

print("\n" + "=" * 78)
print("STEP 18: COMPARISON OF CRITICAL RPM VALUES")
print("=" * 78)

# Use the flexible-mode natural frequencies calculated earlier.
# The rigid-body mode is excluded from both frequency lists.

original_frequencies_step18 = np.asarray(flexible_frequencies_original)
geometry_frequencies_step18 = np.asarray(flexible_frequencies_geometry)

# Use the same excitation orders and operating range as Step 17.
orders_step18 = [6, 12, 18, 24, 30]
minimum_rpm_step18 = 50.0
maximum_rpm_step18 = 105.0

print("\nOperating range: "
      f"{minimum_rpm_step18:.1f}–{maximum_rpm_step18:.1f} RPM")

print("\nCandidate critical speeds within the operating range")
print("-" * 78)
print(
    f"{'Mode':<7}"
    f"{'Order':>8}"
    f"{'Original RPM':>16}"
    f"{'Geometry RPM':>16}"
    f"{'Change RPM':>13}"
    f"{'Change (%)':>12}"
)

comparison_count_step18 = 0

number_of_modes_step18 = min(
    len(original_frequencies_step18),
    len(geometry_frequencies_step18)
)

for mode_index in range(number_of_modes_step18):
    original_frequency = original_frequencies_step18[mode_index]
    geometry_frequency = geometry_frequencies_step18[mode_index]

    for order in orders_step18:
        original_rpm = 60.0 * original_frequency / order
        geometry_rpm = 60.0 * geometry_frequency / order

        original_in_range = (
            minimum_rpm_step18 <= original_rpm <= maximum_rpm_step18
        )
        geometry_in_range = (
            minimum_rpm_step18 <= geometry_rpm <= maximum_rpm_step18
        )

        # Display a pair if either result falls inside the operating range.
        if original_in_range or geometry_in_range:
            change_rpm = geometry_rpm - original_rpm
            change_percent = 100.0 * change_rpm / original_rpm

            print(
                f"{mode_index + 1:<7}"
                f"{order:>8}"
                f"{original_rpm:>16.2f}"
                f"{geometry_rpm:>16.2f}"
                f"{change_rpm:>+13.2f}"
                f"{change_percent:>+11.2f}%"
            )

            comparison_count_step18 += 1

if comparison_count_step18 == 0:
    print("No candidate critical speeds fall within the operating range.")

print("\nINTERPRETATION")
print("-" * 78)
print("Positive changes mean the geometry-based RPM is higher.")
print("Negative changes mean the geometry-based RPM is lower.")
print("Percentage change is relative to the original RPM.")

print("\nIMPORTANT LIMITATIONS")
print("-" * 78)
print("The shaft dimensions and model inputs are illustrative assumptions.")
print("These calculations do not establish safe or unsafe engine speeds.")
print("Real-engine conclusions require verified engineering data and validation.")

print("\nSTEP 18 COMPLETE")
print("=" * 78)


# ================================================================
# STEP 19: CONSOLIDATED CRITICAL RPM SUMMARY
# ================================================================

print("\n" + "=" * 104)
print("STEP 19: CONSOLIDATED CRITICAL RPM SUMMARY")
print("=" * 104)

# Use the natural frequencies calculated in the earlier steps.
# The original and geometry-based models remain separate.

orders_step19 = [6, 12, 18, 24, 30]
minimum_rpm_step19 = 50.0
maximum_rpm_step19 = 105.0

print(f"\nAssumed operating range: "
      f"{minimum_rpm_step19:.1f}–{maximum_rpm_step19:.1f} RPM")

print("\nCRITICAL RPM COMPARISON")
print("-" * 104)

print(
    f"{'Mode':<7}"
    f"{'Order':>7}"
    f"{'Original RPM':>15}"
    f"{'Geometry RPM':>16}"
    f"{'Change RPM':>13}"
    f"{'Change (%)':>12}"
    f"{'Original in range':>18}"
    f"{'Geometry in range':>19}"
)

print("-" * 104)

count_original_step19 = 0
count_geometry_step19 = 0
count_comparisons_step19 = 0

number_of_modes_step19 = min(
    len(flexible_frequencies_original),
    len(flexible_frequencies_geometry)
)

for mode_index in range(number_of_modes_step19):
    original_frequency = flexible_frequencies_original[mode_index]
    geometry_frequency = flexible_frequencies_geometry[mode_index]

    for order in orders_step19:
        original_rpm = 60.0 * original_frequency / order
        geometry_rpm = 60.0 * geometry_frequency / order

        original_in_range = (
            minimum_rpm_step19 <= original_rpm <= maximum_rpm_step19
        )
        geometry_in_range = (
            minimum_rpm_step19 <= geometry_rpm <= maximum_rpm_step19
        )

        # Include a row when either model predicts a value
        # inside the assumed operating range.
        if original_in_range or geometry_in_range:
            change_rpm = geometry_rpm - original_rpm
            change_percent = 100.0 * change_rpm / original_rpm

            original_status = "YES" if original_in_range else "NO"
            geometry_status = "YES" if geometry_in_range else "NO"

            print(
                f"{mode_index + 1:<7}"
                f"{order:>7}"
                f"{original_rpm:>15.2f}"
                f"{geometry_rpm:>16.2f}"
                f"{change_rpm:>+13.2f}"
                f"{change_percent:>+11.2f}%"
                f"{original_status:>18}"
                f"{geometry_status:>19}"
            )

            count_comparisons_step19 += 1

            if original_in_range:
                count_original_step19 += 1

            if geometry_in_range:
                count_geometry_step19 += 1

print("-" * 104)

print("\nSUMMARY")
print("-" * 50)
print(f"Candidate values in original model: "
      f"{count_original_step19}")
print(f"Candidate values in geometry-based model: "
      f"{count_geometry_step19}")
print(f"Rows included in comparison table: "
      f"{count_comparisons_step19}")

print("\nHOW TO READ THIS TABLE")
print("-" * 50)
print("YES means the calculated RPM is inside the assumed operating range.")
print("NO means the calculated RPM is outside that range.")
print("A positive change means the geometry-based RPM is higher.")
print("A negative change means the geometry-based RPM is lower.")

print("\nENGINEERING LIMITATIONS")
print("-" * 50)
print("These results use illustrative shaft geometry and model assumptions.")
print("They identify mathematical candidates, not confirmed harmful resonance.")
print("Do not use this table to establish safe operating speeds.")
print("Real-engine assessment requires verified data and qualified validation.")

print("\nSTEP 19 COMPLETE")
print("=" * 104)


# ================================================================
# STEP 20: VISUALIZE CANDIDATE CRITICAL RPM VALUES
# ================================================================

import matplotlib.pyplot as plt

print("\n" + "=" * 72)
print("STEP 20: CRITICAL RPM VISUALIZATION")
print("=" * 72)

# Use the natural frequencies calculated in earlier steps.
# The rigid-body mode has already been excluded from these arrays.

orders_step20 = [6, 12, 18, 24, 30]
minimum_rpm_step20 = 50.0
maximum_rpm_step20 = 105.0

# Prepare the plot.
fig_step20, ax_step20 = plt.subplots(figsize=(11, 6.5))

# Shade the assumed operating range.
ax_step20.axvspan(
    minimum_rpm_step20,
    maximum_rpm_step20,
    alpha=0.15,
    label="Assumed operating range: 50–105 RPM"
)

# Add one row for each candidate comparison.
plot_labels_step20 = []
plot_row_step20 = 0
original_legend_added_step20 = False
geometry_legend_added_step20 = False

number_of_modes_step20 = min(
    len(flexible_frequencies_original),
    len(flexible_frequencies_geometry)
)

for mode_index in range(number_of_modes_step20):
    original_frequency = flexible_frequencies_original[mode_index]
    geometry_frequency = flexible_frequencies_geometry[mode_index]

    for order in orders_step20:
        original_rpm = 60.0 * original_frequency / order
        geometry_rpm = 60.0 * geometry_frequency / order

        original_in_range = (
            minimum_rpm_step20 <= original_rpm <= maximum_rpm_step20
        )
        geometry_in_range = (
            minimum_rpm_step20 <= geometry_rpm <= maximum_rpm_step20
        )

        # Plot candidates where either model's result is in range.
        if original_in_range or geometry_in_range:
            y_position = plot_row_step20

            # Connect the two predictions for visual comparison.
            ax_step20.plot(
                [original_rpm, geometry_rpm],
                [y_position, y_position],
                linestyle="-",
                linewidth=1,
                alpha=0.7
            )

            # Original-model prediction.
            original_label = (
                "Original model"
                if not original_legend_added_step20
                else None
            )

            ax_step20.plot(
                original_rpm,
                y_position,
                marker="o",
                linestyle="None",
                markersize=8,
                label=original_label
            )
            original_legend_added_step20 = True

            # Geometry-based prediction.
            geometry_label = (
                "Geometry-based model"
                if not geometry_legend_added_step20
                else None
            )

            ax_step20.plot(
                geometry_rpm,
                y_position,
                marker="x",
                linestyle="None",
                markersize=9,
                markeredgewidth=2,
                label=geometry_label
            )
            geometry_legend_added_step20 = True

            plot_labels_step20.append(
                f"Mode {mode_index + 1}, order {order}"
            )

            plot_row_step20 += 1

# Configure axes and title.
ax_step20.set_yticks(range(len(plot_labels_step20)))
ax_step20.set_yticklabels(plot_labels_step20)
ax_step20.invert_yaxis()

ax_step20.set_xlim(45, 110)
ax_step20.set_xlabel("Engine speed (RPM)")
ax_step20.set_ylabel("Vibration mode and excitation order")
ax_step20.set_title(
    "Candidate Critical RPM Values\n"
    "Original Model vs Geometry-Based Model"
)

ax_step20.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_step20.legend(loc="best")
fig_step20.tight_layout()

print("Operating range shown: 50–105 RPM")
print("Circle markers: original model")
print("X markers: geometry-based model")
print("Connecting lines: change between model predictions")
print("Displaying the critical RPM comparison plot.")

plt.show()

print("\nIMPORTANT:")
print("This is an educational visualization, not a safety chart.")
print("The candidate speeds are not confirmed harmful resonance speeds.")
print("\nSTEP 20 COMPLETE")
print("=" * 72)




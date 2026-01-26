import vs

# CONFIGURATION
# ---------------------------------------------------------------------
# Set to True if you want "L" to be negative X (Stage Left = -X)
# Set to False if you want "L" to be positive X
CARTESIAN_LEFT_IS_L = False

# The User Field to overwrite
TARGET_FIELD = 'User Field 6'


# ---------------------------------------------------------------------

def get_feet_inch_str(val_in_feet):
    """
    Converts a decimal foot value (e.g. 5.5) to a string "5'-6\""
    Does NOT handle signs (+/-) or suffixes.
    """
    # Work with absolute positive value for math
    abs_val = abs(val_in_feet)

    # Calculate feet and inches
    feet = int(abs_val)
    # Get remainder, multiply by 12, round to nearest whole inch
    inches = round((abs_val - feet) * 12)

    # Handle the rollover case (e.g., 11.9 inches rounds to 12)
    if inches == 12:
        feet += 1
        inches = 0

    return f"{feet}'-{inches}\""


def format_coords(h_focus):
    # Get coordinates (returns tuple in document units)
    # We assume these are in Feet (standard for Spotlight Feet & Inch files)
    pt = vs.GetSymLoc3D(h_focus)
    x, y, z = pt

    # --- FORMAT X (Stage Left/Right) ---
    # 1. Get base string (e.g. 5'-6")
    x_base = get_feet_inch_str(x)

    # 2. Determine Suffix
    suffix = ""
    if x < 0:
        suffix = "L" if CARTESIAN_LEFT_IS_L else "R"
    elif x > 0:
        suffix = "R" if CARTESIAN_LEFT_IS_L else "L"
    else:
        suffix = ""

    x_final = f"{x_base}{suffix}"

    # --- FORMAT Y (Up/Down Stage) ---
    # Requirements: Always show sign (+ or -)
    y_base = get_feet_inch_str(y)

    if y > 0:
        y_final = f"+{y_base}"
    elif y < 0:
        y_final = f"-{y_base}"
    else:
        y_final = y_base  # Zero has no sign usually, or use "+0'-0"" if preferred

    # --- FORMAT Z (Height) ---
    # Requirements: Always show sign (+ or -)
    z_base = get_feet_inch_str(z)

    if z > 0:
        z_final = f"+{z_base}"
    elif z < 0:
        z_final = f"-{z_base}"
    else:
        z_final = z_base

    return x_final, y_final, z_final


def update_light(h):
    # 1. Check for Focus Record
    focus_name = vs.GetRField(h, 'Lighting Device', 'Focus')

    # 2. Clean up if empty
    if not focus_name:
        vs.SetRField(h, 'Lighting Device', TARGET_FIELD, '')
        return

    # 3. Find object
    h_focus = vs.GetObject(focus_name)
    if h_focus == vs.Handle(0):
        return

    # 4. Get Strings
    x_str, y_str, z_str = format_coords(h_focus)

    # 5. Combine: 5'-6"R, -6'-3", +7'-2"
    final_data = f"{x_str}, {y_str}, {z_str}"

    # 6. Write and Reset
    vs.SetRField(h, 'Lighting Device', TARGET_FIELD, final_data)
    vs.ResetObject(h)


def main():
    # Only run on Lighting Devices
    criteria = "(R IN ['Lighting Device'])"
    vs.ForEachObject(update_light, criteria)

    vs.AlrtDialog(f"Update Complete! Data written to {TARGET_FIELD}.")


if __name__ == "__main__":
    main()
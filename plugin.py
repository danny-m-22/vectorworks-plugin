import vs

# FIX 0 FEET ISSUE



# NOTE: This will not run in an IDE because of import vs
# It should run in VectorWorks, though

# CONFIGURATION
# ---------------------------------------------------------------------
# Change this to True if your Stage Left is on the Negative X side.
# Change to False if your Stage Left is on the Positive X side.
CARTESIAN_LEFT_IS_L = False

# Change this to 'User Field #', with # being your desired output column number
TARGET_FIELD = 'User Field 6'
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def unit_conversion(feet, inches):
    is_negative = feet < 0 or inches < 0

    if inches == 12 and not is_negative:
        feet += 1
        inches = 0
    elif inches == 12 and is_negative:
        feet -= 1
        inches = 0
    return str(feet), str(inches)


def format_coordinates(h_focus):
    """
    Returns the X, Y, Z tuple formatted as strings.
    """
    # Get the Focus Point object
    focus_point = vs.GetSymLoc3D(h_focus)
    x, y, z = focus_point

    # Format Y and Z using document units (feet/inches handled automatically)
    # Use abs() to remove the negative sign so L/R can be manually added

    y_string = vs.Num2StrF(y).strip()
    z_string = vs.Num2StrF(z).strip()
    x_abs_string = vs.Num2StrF(abs(x)).strip()


    # Split feet and inches for formatting
    try:
        x_split = x_abs_string.split("'")
        x_ft = x_split[0]
        x_in = x_split[1]
        x_in = x_in[0:-1]
        x_in = str(round(float(x_in)))
        x_ft, x_in = unit_conversion(int(x_ft), int(x_in))
        x_ft = x_ft + "'"
        x_in = x_in + '"'
    except IndexError:
        x_ft = "1'"
        x_in = '0"'

    try:
        y_split = y_string.split("'")
        y_ft = y_split[0]
        y_in = y_split[1]
        y_in = y_in[0:-1]
        y_in = str(round(float(y_in)))
        y_ft, y_in = unit_conversion(int(y_ft), int(y_in))
        if int(y_ft) >= 0:
            y_ft = "+" + y_ft
        y_ft = y_ft + "'"
        y_in = y_in + '"'
    except IndexError:
        y_in = "0'"
        y_num = y_string.split('"')
        y_num = round(int(y_num[0])/12)
        if y_num == 0:
            y_ft = "0'"
        elif y_num == 1:
            y_ft = "+1'"
        else:
            y_ft = "-1'"

    try:
        z_split = z_string.split("'")
        z_ft = z_split[0]
        z_in = z_split[1]
        z_in = z_in[0:-1]
        z_in = str(round(float(z_in)))
        z_ft, z_in = unit_conversion(int(z_ft), int(z_in))
        if int(z_ft) >= 0:
            z_ft = "+" + z_ft
        z_ft = z_ft + "'"
        z_in = z_in + '"'
    except IndexError:
        z_in = "0'"
        z_num = z_string.split('"')
        z_num = round(int(z_num[0])/12)
        if z_num == 0:
            z_ft = "0'"
        elif z_num == 1:
            z_ft = "+1'"
        else:
            z_ft = "-1'"

    # Determine L/R for X based on configuration
    # Note: at the Configuration section at the top, you can reverse this
    # by setting CARTESIAN_LEFT_IS_L = False
    suffix = ""

    if x < 0:
        suffix = "L" if CARTESIAN_LEFT_IS_L else "R"
    elif x > 0:
        suffix = "R" if CARTESIAN_LEFT_IS_L else "L"
    else:
        suffix = ""  # Center Line (0)


    # Add dash between feet and inches as well as ' and " symbols
    x_string = x_ft + "-" + x_in + suffix
    y_string = y_ft + "-" + y_in
    z_string = z_ft + "-" + z_in


    return x_string, y_string, z_string


def update_light(h):
    """
    Function that runs on every Lighting Device.
    """
    # 1. Get the name of the focus point from the Light's data
    focus_name = vs.GetRField(h, 'Lighting Device', 'Focus')

    # 2. If no focus is assigned, clear the field and exit
    if not focus_name:
        vs.SetRField(h, 'Lighting Device', TARGET_FIELD, '')
        return

    # 3. Find the actual Focus Point object in the drawing
    h_focus = vs.GetObject(focus_name)

    # If the focus point name is text but the object doesn't exist, exit
    if h_focus == vs.Handle(0):
        return

    # 4. Get formatted coordinates
    x_string, y_string, z_string = format_coordinates(h_focus)

    # 5. Concatenate into one string.
    # Example of format: 5'-0"L, 10'-0", 12'-0"
    final_data = f"{x_string}, {y_string}, {z_string}"

    # 6. Write to the Lighting Device in the specified User Field column
    vs.SetRField(h, 'Lighting Device', TARGET_FIELD, final_data)

    # 7. Reset object to ensure OIP updates visually (optional, but good safety)
    vs.ResetObject(h)


def main():
    # Select all objects that have the 'Lighting Device' record attached
    criteria = "(R IN ['Lighting Device'])"
    vs.ForEachObject(update_light, criteria)

    # Notify user when done
    vs.AlrtDialog(f"Update Complete! Check {TARGET_FIELD}.")


if __name__ == "__main__":
    main()
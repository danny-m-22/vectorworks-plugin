import vs

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

def format_coordinates(h_focus):
    """
    Returns the X, Y, Z tuple formatted as strings.
    """
    # Get the Focus Point object
    focus_point = vs.GetSymLoc3D(h_focus)
    x, y, z = focus_point

    # Format Y and Z using document units (feet/inches handled automatically)
    y_string = vs.Num2StrF(y).strip()
    z_string = vs.Num2StrF(z).strip()

    # Format X with L/R ending
    # Use abs() to remove the negative sign so L/R can be manually added
    # x value will still have inch and feet units
    x_abs_string = vs.Num2StrF(abs(x)).strip()

    suffix = ""

    # Determine L/R based on configuration
    # Note: at the Configuration section at the top, you can reverse this
    # by setting CARTESIAN_LEFT_IS_L = False

    if x < 0:
        suffix = "L" if CARTESIAN_LEFT_IS_L else "R"
    elif x > 0:
        suffix = "R" if CARTESIAN_LEFT_IS_L else "L"
    else:
        suffix = ""  # Center Line (0)

    x_string = f"{x_abs_string}{suffix}"

    # Split feet and inches for final formatting touches
    x_split = x_string.split("'")
    y_split = y_string.split("'")
    z_split = z_string.split("'")

    # Round decimal of inches
    x_split[1] = str(round(float(x_split[1].replace('"',"")))) + '"'
    y_split[1] = str(round(float(y_split[1].replace('"', "")))) + '"'
    z_split[1] = str(round(float(z_split[1].replace('"', "")))) + '"'

    # Add + sign to y and z values that are positive
    if int(y_split[1]) > 0:
        y_split[1] =  "+" + y_split[1]

    if int(z_split[1]) > 0:
        z_split[1] =  "+" + z_split[1]

    # Add dash between feet and inches
    x_string = x_split[0] + "-" + x_split[1]
    y_string = y_split[0] + "-" + y_split[1]
    z_string = z_split[0] + "-" + z_split[1]

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
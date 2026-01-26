
"""
Hello! Please read these notes even if you do not know Python:

NOTE 1: I do not have Vectorworks and have not tested this extensively.
Please ensure that the values you get are accurate:
I am not responsible for any errors this may cause, 
but please let me know if you are getting errors. 
A screenshot of the error message or incorrect string 
output would help me fix any issues.

# Note 2: to use this code, you must copy the code
(no need to download it) and paste it in a VS script.
MAKE SURE YOU SWITCH THE SCRIPT LANGUAGE TO PYTHON;
it will not run if you don't.

NOTE 3: this file does NOT handle fractions:
1 3/4" won't work but 1.75" will.
Change your Vectorworks settings so it will work.
I can add functionality for this if needed,
but it is much easier to just change this setting.

NOTE 4: ensure your origin is accurate (0,0,0),
or you will get errors where at least
one coordinate value is off by the same amount
every time. This error has nothing to do with this plugin.

NOTE 5: here is an example of the expected output, as
specified by H.A.G.:

6'-0"R, -3'-6", +4'-0"

- feet and inches have a hyphen between them,
- X will have L or R at the end,
- Y and Z will have + or - at the beginning,
- and ft will have ' and in will have "
"""

# This code will not run in an IDE because of this import statement;
# it will only run in Vectorworks
import vs

# CONFIGURATION
# ----------------
# Swap this to True if your L and R are reversed for your X values
CARTESIAN_LEFT_IS_L = False

# Change the number in the string below to change the desired output column
TARGET_FIELD = 'User Field 6'
# ----------------


# You will not need to change anything within this helper function
def unit_conversion(feet, inches):
    if inches == 12:
        feet += 1
        inches = 0
    return str(feet), str(inches)



def format_coordinates(h_focus):
    """
    All of the string reformatting happens in this function here.
    If an error occurs, it will probably be here.

    Args:
        h_focus: a VS focus object
    Returns:
        x, y, and z strings in the required format for a given focus object
    """
    # Get the raw, unformatted coordinates
    focus_point = vs.GetSymLoc3D(h_focus)
    x, y, z = focus_point

    # Use abs() to make reformatting easier;
    # +/- signs get handled at the end using x, y, and z variables from above
    x_abs_string = vs.Num2StrF(abs(x)).strip()
    y_abs_string = vs.Num2StrF(abs(y)).strip()
    z_abs_string = vs.Num2StrF(abs(z)).strip()

    # REFORMATTING LOGIC
    # Handle x, y, and z separately.
    # Attempt to split ft and in;
    # if this works, round inches and add ' and "
    # as well as make sure 12 in + changes ft value.
    # OTHERWISE: if only inches, round to nearest foot (0 or 1).

    # --- X LOOP ---
    try:
        x_split = x_abs_string.split("'")
        x_ft = x_split[0]
        x_in = x_split[1]
        x_in = x_in[0:-1]
        x_in = str(round(float(x_in)))
        x_ft, x_in = unit_conversion(int(float(x_ft)), int(float(x_in)))
        x_ft = x_ft + "'"
        x_in = x_in + '"'
    except IndexError:
        x_in = '0"'
        try:
            val = float(x_abs_string.replace('"', ''))
            x_num = round(val / 12)
        except ValueError:
            x_num = 0

        if x_num == 0:
            x_ft = "0'"
        else:
            x_ft = "1'"

    # --- Y LOOP ---
    try:
        y_split = y_abs_string.split("'")
        y_ft = y_split[0]
        y_in = y_split[1]
        y_in = y_in[0:-1]
        y_in = str(round(float(y_in)))
        y_ft, y_in = unit_conversion(int(float(y_ft)), int(float(y_in)))
    except IndexError:
        # Inches only case
        y_in = "0"
        try:
            val = float(y_abs_string.replace('"', ''))
            y_ft = str(round(val / 12))
        except ValueError:
            y_ft = "0"

    # Y FORMATTING & SIGNS
    y_in = y_in + '"'
    # Check the RAW coordinate 'y' for the sign
    if y >= 0:
        y_ft = "+" + y_ft + "'"
    else:
        y_ft = "-" + y_ft + "'"

    # --- Z LOOP ---
    try:
        z_split = z_abs_string.split("'")
        z_ft = z_split[0]
        z_in = z_split[1]
        z_in = z_in[0:-1]
        z_in = str(round(float(z_in)))
        z_ft, z_in = unit_conversion(int(float(z_ft)), int(float(z_in)))
    except IndexError:
        z_in = "0"
        try:
            val = float(z_abs_string.replace('"', ''))
            z_ft = str(round(val / 12))
        except ValueError:
            z_ft = "0"

    # Z FORMATTING & SIGNS
    z_in = z_in + '"'
    # Check the RAW coordinate 'z' for the sign
    if z >= 0:
        z_ft = "+" + z_ft + "'"
    else:
        z_ft = "-" + z_ft + "'"

    # L/R Logic for X value using the RAW coordinate 'x';
    # again, X will not have + or -, only L or R.
    # Logic here will never need to be updated;
    # update CARTESIAN_LEFT_IS_L at the top if needed
    suffix = ""
    if x < 0:
        suffix = "L" if CARTESIAN_LEFT_IS_L else "R"
    elif x > 0:
        suffix = "R" if CARTESIAN_LEFT_IS_L else "L"

    # Assemble final reformatted strings
    x_string = x_ft + "-" + x_in.replace('"', '') + '"' + suffix
    y_string = y_ft + "-" + y_in.replace('"', '') + '"'
    z_string = z_ft + "-" + z_in.replace('"', '') + '"'

    return x_string, y_string, z_string

# This function should not need changing
def update_light(h):
    focus_name = vs.GetRField(h, 'Lighting Device', 'Focus')
    if not focus_name:
        vs.SetRField(h, 'Lighting Device', TARGET_FIELD, '')
        return

    h_focus = vs.GetObject(focus_name)
    if h_focus == vs.Handle(0):
        return

    x, y, z = format_coordinates(h_focus)
    final_data = f"{x}, {y}, {z}"

    vs.SetRField(h, 'Lighting Device', TARGET_FIELD, final_data)
    vs.ResetObject(h)

# This function should not need changing
def main():
    criteria = "(R IN ['Lighting Device'])"
    vs.ForEachObject(update_light, criteria)
    vs.AlrtDialog(f"Update Complete! Check {TARGET_FIELD}")


if __name__ == "__main__":
    main()
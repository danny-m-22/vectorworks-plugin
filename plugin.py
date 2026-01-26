import vs

# CONFIGURATION
CARTESIAN_LEFT_IS_L = False
TARGET_FIELD = 'User Field 6'


def unit_conversion(feet, inches):
    # Since we are feeding this positive numbers now,
    # we only need to handle the positive rollover.
    if inches == 12:
        feet += 1
        inches = 0
    return str(feet), str(inches)


def format_coordinates(h_focus):
    focus_point = vs.GetSymLoc3D(h_focus)
    x, y, z = focus_point

    # KEY FIX: Use abs() for Y and Z too.
    # We will handle the signs manually at the end.
    x_abs_string = vs.Num2StrF(abs(x)).strip()
    y_abs_string = vs.Num2StrF(abs(y)).strip()
    z_abs_string = vs.Num2StrF(abs(z)).strip()

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

    # L/R Logic
    suffix = ""
    if x < 0:
        suffix = "L" if CARTESIAN_LEFT_IS_L else "R"
    elif x > 0:
        suffix = "R" if CARTESIAN_LEFT_IS_L else "L"

    # Assemble
    x_string = x_ft + "-" + x_in.replace('"', '') + '"' + suffix
    y_string = y_ft + "-" + y_in.replace('"', '') + '"'
    z_string = z_ft + "-" + z_in.replace('"', '') + '"'

    return x_string, y_string, z_string


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


def main():
    criteria = "(R IN ['Lighting Device'])"
    vs.ForEachObject(update_light, criteria)
    vs.AlrtDialog(f"Update Complete! Check {TARGET_FIELD}")


if __name__ == "__main__":
    main()
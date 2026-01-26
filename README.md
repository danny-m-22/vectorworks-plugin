# Vectorworks Spotlight: Focus Point Coordinate Writer

A simple automation script for Vectorworks Spotlight. This tool automatically finds the **Focus Point** assigned to your lighting devices, calculates the X, Y, and Z coordinates, and writes them into a customizable User Field (e.g., "User Field 6").

This solves the common problem of needing to export actual focus coordinates (Stage Left/Right, Up/Down Stage, Height) for paperwork, which Vectorworks does not include by default.

## What It Does
* **Automatic Updates:** Scans every lighting device in your file.
* **Smart Formatting:** Converts coordinates into a clean standard format:
    * **X:** `10'-6"R` (Includes "L" or "R" suffix)
    * **Y:** `+12'-0"` (Includes + or - prefix)
    * **Z:** `+5'-6"` (Includes + or - prefix)
* **Unit Handling:** Automatically rounds decimal inches (e.g., 11.9" becomes 12", which rolls over to the next foot).

## Installation (No Coding Required)

You do not need to download or install complex files. You simply create the script inside your Vectorworks file.

1.  **Open Vectorworks** and open your project file.
2.  Open the **Resource Manager** (Window > Palettes > Resource Manager).
3.  Right-click in a blank space and select **New Resource... > Script**.
4.  Give the palette a name (e.g., "Automation Tools") and name the script **"Update Focus Coords"**.
5.  **IMPORTANT:** In the script editor window, look at the top dropdown menu. Change it from **VectorScript** to **Python**.
6.  **Copy** the entire code from `plugin.py`.
7.  **Paste** it into the editor window and click **OK**.

## How to Use
1.  Ensure your Lighting Devices have a **Focus Point** assigned in their Object Info Palette.
2.  Find your **Script Palette** (it should be floating on your screen).
3.  Double-click **"Update Focus Coords"**.
4.  A popup will confirm when the update is complete.
5.  Check **User Field 6** (or your custom field) in the Object Info Palette to see the data.

## Configuration settings
If you need to change how the script works, you can edit the text at the very top of the script.

### 1. Changing the Output Field
By default, the script writes to **User Field 6**. To change this:
* Look for the line: `TARGET_FIELD = 'User Field 6'`
* Change the number to your desired field (e.g., `'User Field 5'`).

### 2. Swapping Stage Left/Right
By default, **Positive X is Right** (Stage Right) and **Negative X is Left** (Stage Left). If your setup is reversed:
* Look for the line: `CARTESIAN_LEFT_IS_L = False`
* Change `False` to `True`.

## Troubleshooting & Notes

* **"My Y value is always off by exactly 8 inches"**
    * This is an issue with your **User Origin**. The script reads the internal coordinates. Ensure your Vectorworks User Origin is set to (0,0) at your center line/plaster line intersection.
* **Fractions (e.g., 1/2")**
    * This script is designed for decimal inputs (e.g., 1.5"). If you use fractions in your unit settings, they may not format correctly. It is recommended to use decimal inches or whole inches for the smoothest results.
* **Errors on Export?**
    * If you get an error popup, take a screenshot of the error text and the light causing the issue (if identifiable) to help with debugging.

---
**Disclaimer:** This script is provided as-is. Always check a few lights after running the script to ensure the data is accurate before exporting your final paperwork.

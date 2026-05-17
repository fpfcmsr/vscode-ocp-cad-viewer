"""Test provenance tracking for extrude, loft, revolve, hollow, and offset.

Usage:
    1. Start the OCP CAD Viewer in VS Code
    2. Run: uv run examples/test_provenance_ops.py
    3. The Source button auto-activates (crosshair cursor)
    4. Click any face or edge — VS Code jumps to the line that created it

Expected provenance per face:
    - Box flat faces          → line 20 (Box)
    - Extruded cylinder wall  → line 24 (Circle) + line 25 (extrude)
    - Lofted surface          → line 30/31 (Circles) + line 32 (loft)
    - Revolved surface        → line 37 (Line) + line 38 (revolve)
    - Hollow interior faces   → line 43 (Box) + line 44 (hollow)
    - Offset faces            → line 49 (Rectangle) + line 50 (offset)
"""

from ocp_vscode import show, enable_source_location

enable_source_location()

from build123d import *

# --- 1. Extrude ---
circle = Circle(5)
extruded = extrude(circle, 15)

# --- 2. Loft ---
loft_bottom = Wire.make_circle(10, Plane(origin=(40, 0, 0)))
loft_top = Wire.make_circle(5, Plane(origin=(40, 0, 20)))
lofted = Solid.make_loft([loft_bottom, loft_top])

# --- 3. Revolve ---
with BuildPart() as rev_part:
    with BuildSketch(Plane(origin=(80, 0, 0))):
        with Locations((5, 0)):
            Rectangle(5, 20, align=(Align.MIN, Align.CENTER))
    revolve(axis=Axis((80, 0, 0), (0, 0, 1)))

revolved = rev_part.part

# --- 4. Hollow ---
hollow_box = Box(20, 20, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
hollow_box = hollow_box.locate(Location((120, 0, 0)))
hollowed = hollow_box.hollow(hollow_box.faces().sort_by(Axis.Z)[-1:], -1)

# --- 5. Offset (2D) ---
with BuildSketch(Plane(origin=(160, 0, 0))) as offset_sk:
    Rectangle(10, 10)
    offset(amount=3)

offset_result = offset_sk.sketch

show(circle, extruded, lofted, loft_bottom, loft_top, revolved, hollowed, offset_result)

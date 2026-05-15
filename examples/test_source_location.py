"""Test script for click-face-to-jump-to-source.

Usage:
    1. Start the OCP CAD Viewer in VS Code
    2. Run this script: uv run examples/test_source_location.py
    3. The "Source" button (bottom-right of viewer) auto-activates
       and the cursor becomes a crosshair
    4. Click any face or edge in the 3D view
    5. VS Code should jump to the line that created/modified that geometry

Expected behavior:
    - Click a flat box face       → jumps to line 24 (Box)
    - Click the cylindrical hole  → quick-pick: Box (24), Cylinder (25), cut (26)
    - Click a filleted edge/face  → quick-pick: Box (24), ..., fillet (27)
"""

from ocp_vscode import show, enable_source_location

enable_source_location()

from build123d import *

# --- Test 1: Simple primitive ---
box = Box(20, 20, 10)  # line 27
cyl = Cylinder(5, 20)  # line 28
cut_result = box - cyl  # line 29
filleted = cut_result.fillet(1, [cut_result.edges().sort_by().last])  # line 30

show(filleted)

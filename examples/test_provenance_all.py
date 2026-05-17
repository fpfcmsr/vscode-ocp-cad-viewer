"""Test provenance tracking for all instrumented build123d operations.

Usage:
    1. Start the OCP CAD Viewer in VS Code
    2. Run: uv run examples/test_provenance_all.py
    3. The Source button auto-activates (crosshair cursor)
    4. Click any face or edge — VS Code jumps to the line that created it

Each shape is offset in X so they don't overlap. Sections are labeled
with comments. Expected provenance is noted per shape.
"""

from ocp_vscode import show, enable_source_location

enable_source_location()

from build123d import *

results = []
x = 0
SPACING = 40


# ============================================================
# 1. Algebra-mode primitives (BaseSketchObject / BasePartObject)
# Expected: clicking any face → jumps to the constructor line
# ============================================================

# 1a. Box (algebra mode, no builder context)
box = Box(15, 15, 10)  # → "Box"
box = box.locate(Location((x, 0, 0)))
results.append(box)
x += SPACING

# 1b. Circle / extrude (algebra mode)
circle = Circle(7)  # → "Circle"
extruded_circle = extrude(circle, 12)  # → "Circle" + "extrude"
extruded_circle = extruded_circle.locate(Location((x, 0, 0)))
results.append(extruded_circle)
x += SPACING

# 1c. Rectangle (algebra mode)
rect = Rectangle(12, 8)  # → "Rectangle"
rect = rect.locate(Location((x, 0, 0)))
results.append(rect)
x += SPACING


# ============================================================
# 2. Builder-mode primitives
# Expected: same provenance as algebra mode
# ============================================================

# 2a. Box in BuildPart
with BuildPart() as bp_box:
    with Locations((x, 0, 0)):
        Box(15, 15, 10)  # → "Box"
results.append(bp_box.part)
x += SPACING

# 2b. Circle in BuildSketch + extrude
with BuildPart() as bp_cyl:
    with Locations((x, 0, 0)):
        with BuildSketch():
            Circle(7)  # → "Circle"
        extrude(amount=12)  # → "Circle" + "extrude"
results.append(bp_cyl.part)
x += SPACING


# ============================================================
# 3. Solid factory methods
# Expected: clicking any face → jumps to the make_* line
# ============================================================

# 3a. Solid.make_box
sbox = Solid.make_box(15, 15, 10)  # → "Solid.make_box"
sbox = sbox.locate(Location((x, 0, 0)))
results.append(sbox)
x += SPACING

# 3b. Solid.make_cylinder
scyl = Solid.make_cylinder(7, 12)  # → "Solid.make_cylinder"
scyl = scyl.locate(Location((x, 0, 0)))
results.append(scyl)
x += SPACING

# 3c. Solid.make_sphere
ssph = Solid.make_sphere(8)  # → "Solid.make_sphere"
ssph = ssph.locate(Location((x, 0, 0)))
results.append(ssph)
x += SPACING

# 3d. Solid.make_cone
scone = Solid.make_cone(8, 4, 12)  # → "Solid.make_cone"
scone = scone.locate(Location((x, 0, 0)))
results.append(scone)
x += SPACING

# 3e. Solid.make_torus
stor = Solid.make_torus(10, 3)  # → "Solid.make_torus"
stor = stor.locate(Location((x, 0, 0)))
results.append(stor)
x += SPACING


# ============================================================
# 4. Loft
# Expected: faces → "Wire.make_circle" + "loft"
# ============================================================

loft_bottom = Wire.make_circle(8, Plane(origin=(x, 0, 0)))  # → "Wire.make_circle"
loft_top = Wire.make_circle(4, Plane(origin=(x, 0, 20)))  # → "Wire.make_circle"
lofted = Solid.make_loft([loft_bottom, loft_top])  # → "Wire.make_circle" + "loft"
results.append(lofted)
x += SPACING


# ============================================================
# 5. Revolve
# Expected: faces → "Rectangle" + "revolve"
# ============================================================

with BuildPart() as rev_part:
    with BuildSketch(Plane(origin=(x, 0, 0))):
        with Locations((7, 0)):
            Rectangle(4, 16, align=(Align.MIN, Align.CENTER))  # → "Rectangle"
    revolve(axis=Axis((x, 0, 0), (0, 0, 1)))  # → "Rectangle" + "revolve"
results.append(rev_part.part)
x += SPACING


# ============================================================
# 6. Hollow
# Expected: faces → "Box" + "hollow"
# ============================================================

hollow_box = Box(16, 16, 10)  # → "Box"
hollow_box = hollow_box.locate(Location((x, 0, 0)))
hollowed = hollow_box.hollow(hollow_box.faces().sort_by(Axis.Z)[-1:], -1)  # → "Box" + "hollow"
results.append(hollowed)
x += SPACING


# ============================================================
# 7. Offset (2D)
# Expected: faces → "Rectangle" + "offset"
# ============================================================

with BuildSketch(Plane(origin=(x, 0, 0))) as offset_sk:
    Rectangle(8, 8)  # → "Rectangle"
    offset(amount=3)  # → "Rectangle" + "offset"
results.append(offset_sk.sketch)
x += SPACING


# ============================================================
# 8. Fillet (3D)
# Expected: faces → "Box" + "fillet"
# ============================================================

fillet_box = Box(15, 15, 10)  # → "Box"
fillet_box = fillet_box.locate(Location((x, 0, 0)))
filleted = fillet(fillet_box.edges().sort_by(Axis.Z)[-4:], radius=2)  # → "Box" + "fillet"
results.append(filleted)
x += SPACING


# ============================================================
# 9. Chamfer (3D)
# Expected: faces → "Box" + "chamfer"
# ============================================================

cham_box = Box(15, 15, 10)  # → "Box"
cham_box = cham_box.locate(Location((x, 0, 0)))
chamfered = chamfer(cham_box.edges().sort_by(Axis.Z)[-4:], length=2)  # → "Box" + "chamfer"
results.append(chamfered)
x += SPACING


# ============================================================
# 10. Boolean operations (fuse / cut / intersect)
# Expected: faces → source primitives + "fuse"/"cut"
# ============================================================

# 10a. Fuse
b1 = Box(12, 12, 12)  # → "Box"
b1 = b1.locate(Location((x, 0, 0)))
s1 = Solid.make_sphere(8)  # → "Solid.make_sphere"
s1 = s1.locate(Location((x, 0, 6)))
fused = b1.fuse(s1)  # → "Box"/"Solid.make_sphere" + "fuse"
results.append(fused)
x += SPACING

# 10b. Cut
b2 = Box(15, 15, 10)  # → "Box"
b2 = b2.locate(Location((x, 0, 0)))
c2 = Solid.make_cylinder(5, 20)  # → "Solid.make_cylinder"
c2 = c2.locate(Location((x, 0, -5)))
cutted = b2.cut(c2)  # → "Box"/"Solid.make_cylinder" + "cut"
results.append(cutted)
x += SPACING


# ============================================================
# 11. Mirror
# Expected: faces → original primitive + "transform"
# ============================================================

mirror_box = Box(10, 10, 10)  # → "Box"
mirror_box = mirror_box.locate(Location((x, -10, 0)))
mirrored = mirror_box.mirror(Plane(origin=(x, 0, 0), z_dir=(0, 1, 0)))  # → "Box" + "transform"
results.append(mirror_box)
results.append(mirrored)
x += SPACING


# ============================================================
# 12. Split
# Expected: faces → original primitive + "split"
# ============================================================

split_box = Box(15, 15, 15)  # → "Box"
split_box = split_box.locate(Location((x, 0, 0)))
split_top = split_box.split(Plane(origin=(x, 0, 3)))  # → "Box" + "split"
results.append(split_top)
x += SPACING


# ============================================================
# 13. Scale
# Expected: faces → original primitive + "transform"
# ============================================================

scale_box = Box(10, 10, 10)  # → "Box"
scale_box = scale_box.locate(Location((x, 0, 0)))
scaled = scale_box.scale(1.5)  # → "Box" + "transform"
results.append(scaled)
x += SPACING


# ============================================================
# 14. Sweep
# Expected: faces → "sweep"
# ============================================================

sweep_path = Edge.make_line((x, 0, 0), (x, 0, 20))  # → "Edge.make_line"
sweep_profile = Wire.make_circle(4, Plane(origin=(x, 0, 0)))
swept = Solid.sweep(Face(sweep_profile), sweep_path)  # → "Solid.sweep"
results.append(swept)
x += SPACING


# ============================================================
# 15. Thicken
# Expected: faces → face source + "thicken"
# ============================================================

thick_face = Face.make_rect(12, 12)  # → "Face.make_rect"
thick_face = thick_face.locate(Location((x, 0, 0)))
thickened = Solid.thicken(thick_face, 5)  # → "Face.make_rect" + "thicken"
results.append(thickened)
x += SPACING


# ============================================================
# 16. Draft
# Expected: faces → "Box" + "draft"
# ============================================================

draft_box = Solid.make_box(15, 15, 12)  # → "Solid.make_box"
draft_box = draft_box.locate(Location((x, 0, 0)))
side_faces = draft_box.faces().filter_by(Axis.Z, reverse=True)
neutral = Plane(origin=(x, 0, 0), z_dir=(0, 0, 1))
drafted = draft_box.draft(side_faces, neutral, 5)  # → "Solid.make_box" + "draft"
results.append(drafted)
x += SPACING


# ============================================================
# 17. Edge factory methods
# Expected: clicking any edge → jumps to make_* line
# ============================================================

# 17a. Edge.make_line
line = Edge.make_line((x, -8, 0), (x, 8, 0))  # → "Edge.make_line"
results.append(line)

# 17b. Edge.make_three_point_arc
arc = Edge.make_three_point_arc((x, -8, 5), (x + 5, 0, 5), (x, 8, 5))  # → "Edge.make_three_point_arc"
results.append(arc)

# 17c. Edge.make_spline
spline = Edge.make_spline(  # → "Edge.make_spline"
    [(x, -8, 10), (x + 3, -3, 10), (x - 3, 3, 10), (x, 8, 10)]
)
results.append(spline)

# 17d. Edge.make_bezier
bezier = Edge.make_bezier(  # → "Edge.make_bezier"
    (x, -8, 15), (x + 8, -4, 15), (x + 8, 4, 15), (x, 8, 15)
)
results.append(bezier)
x += SPACING


# ============================================================
# 18. Wire factory methods
# Expected: clicking any edge → jumps to make_* line
# ============================================================

# 18a. Wire.make_polygon
poly = Wire.make_polygon(  # → "Wire.make_polygon"
    [(x, -6, 0), (x + 6, -6, 0), (x + 6, 6, 0), (x, 6, 0)]
)
results.append(poly)

# 18b. Wire.make_circle
wcirc = Wire.make_circle(6, Plane(origin=(x, 0, 10)))  # → "Wire.make_circle"
results.append(wcirc)
x += SPACING


# ============================================================
# 19. Sketch operations (make_face, make_hull, trace)
# Expected: faces → "make_face" / "make_hull" / "trace"
# ============================================================

# 19a. make_face
with BuildSketch(Plane(origin=(x, 0, 0))) as mf_sk:
    with BuildLine():
        Polyline((-5, -5), (5, -5), (5, 5), (-5, 5), (-5, -5))
    make_face()  # → "make_face"
results.append(mf_sk.sketch)
x += SPACING

# 19b. make_hull
with BuildSketch(Plane(origin=(x, 0, 0))) as mh_sk:
    with BuildLine():
        Line((-5, 0), (5, 0))
        ThreePointArc((5, 0), (0, 5), (-5, 0))
    make_hull()  # → "make_hull"
results.append(mh_sk.sketch)
x += SPACING

# 19c. trace
with BuildSketch(Plane(origin=(x, 0, 0))) as tr_sk:
    with BuildLine():
        Line((-5, 0), (5, 0))
    trace(line_width=2)  # → "trace"
results.append(tr_sk.sketch)
x += SPACING


# ============================================================
# 20. Section
# Expected: faces → "section"
# ============================================================

section_box = Box(15, 15, 15)  # → "Box"
section_box = section_box.locate(Location((x, 0, 0)))
sectioned = section(section_box, Plane(origin=(x, 0, 0)))  # → "section"
results.append(sectioned)
x += SPACING


# ============================================================
# 21. Text
# Expected: faces → "Compound.make_text"
# ============================================================

text_shape = Compound.make_text("Hi", font_size=10)  # → "Compound.make_text"
text_shape = text_shape.locate(Location((x, 0, 0)))
results.append(text_shape)
x += SPACING


# ============================================================
# 22. Extrude taper
# Expected: faces → "Circle" + "extrude_taper" (or "extrude"+"loft")
# ============================================================

taper_face = Circle(8)  # → "Circle"
taper_face = taper_face.locate(Location((x, 0, 0)))
tapered = Solid.extrude_taper(taper_face.face(), (0, 0, 15), taper=10)  # → extrude_taper
tapered = tapered.locate(Location((x, 0, 0)))
results.append(tapered)
x += SPACING


# ============================================================
# 23. Offset 3D
# Expected: faces → "Box" + "offset_3d"
# ============================================================

off3d_box = Box(12, 12, 8)  # → "Box"
off3d_box = off3d_box.locate(Location((x, 0, 0)))
offset3d = off3d_box.offset_3d(  # → "Box" + "offset_3d"
    off3d_box.faces().sort_by(Axis.Z)[-1:], 2
)
results.append(offset3d)
x += SPACING


# ============================================================
# 24. Face.make_surface (non-planar)
# Expected: faces → "Face.make_surface"
# ============================================================

surf_edges = [
    Edge.make_line((x - 8, -8, 0), (x + 8, -8, 0)),
    Edge.make_three_point_arc((x + 8, -8, 0), (x + 10, 0, 5), (x + 8, 8, 0)),
    Edge.make_line((x + 8, 8, 0), (x - 8, 8, 0)),
    Edge.make_three_point_arc((x - 8, 8, 0), (x - 10, 0, 5), (x - 8, -8, 0)),
]
surf = Face.make_surface(Wire(surf_edges))  # → "Face.make_surface"
results.append(surf)
x += SPACING


# ============================================================
# 25. 2D fillet
# Expected: faces → "Rectangle" + "fillet"
# ============================================================

with BuildSketch(Plane(origin=(x, 0, 0))) as fil2d_sk:
    r = Rectangle(14, 10)  # → "Rectangle"
    fillet(r.vertices(), radius=2)  # → "Rectangle" + "fillet"
results.append(fil2d_sk.sketch)
x += SPACING


# ============================================================
# 26. 2D chamfer
# Expected: faces → "Rectangle" + "chamfer"
# ============================================================

with BuildSketch(Plane(origin=(x, 0, 0))) as cham2d_sk:
    r2 = Rectangle(14, 10)  # → "Rectangle"
    chamfer(r2.vertices(), length=2)  # → "Rectangle" + "chamfer"
results.append(cham2d_sk.sketch)
x += SPACING


# ============================================================
# Show everything
# ============================================================

show(*results)

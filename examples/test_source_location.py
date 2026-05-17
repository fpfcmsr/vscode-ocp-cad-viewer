"""Test script for click-face-to-jump-to-source."""

from ocp_vscode import show, Camera, enable_source_location

enable_source_location()

from build123d import *


# Dimensions

# shaft 
shaft_radius = 25
shaft_height = 1000

# blade
blade_pitch = 400
blade_radius = 250
blade_thickness = 15



with BuildPart() as archimedes:

    #shaft
    Cylinder(
        radius= shaft_radius,
        height= shaft_height,
        align= (Align.CENTER, Align.CENTER, Align.MIN)
    )

    # helix 
    with BuildLine() as helix:
        Helix(
            pitch= blade_pitch,
            height= shaft_height,
            radius= blade_radius

        )

    # blade profile
    with BuildSketch(Plane.XZ) as blade_profile:
        with Locations((shaft_radius, 0)):
            
            Rectangle(
                blade_radius - shaft_radius,
                blade_thickness,
                align = (Align.MIN, Align.CENTER)
            )

    # sweep
    sweep(path = helix, is_frenet = True )

show(archimedes, helix, blade_profile, reset_camera=Camera.RESET)
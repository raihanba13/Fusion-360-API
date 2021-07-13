#Author-Raihan
#Description-Code from this class\nhttps://www.autodesk.com/autodesk-university/class/Automating-Fusion-360-API-2018#video

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        # ui.messageBox('Hello script')

        # Get reference to the root component
        rootComp = design.rootComponent

        # Get reference to the sketches and plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane

        # Create a new sketch and get Lines reference
        sketch = sketches.add(xyPlane)
        lines = sketch.sketchCurves.sketchLines

        # Prompt user for values (Note: zero error checking)
        lengthInput = ui.inputBox("Enter a length:", "Length", "3")
        depthInput = ui.inputBox("Enter a depth:", "Depth", "1")
        heightInput = ui.inputBox("Enter a distance:", "Height", "2")

        length = float(lengthInput[0])
        depth = float(depthInput[0])
        height = float(heightInput[0])

        # Use autoesk methods to create input geometry
        # point0 = adsk.core.Point3D.create(0, 0, 0)
        # point1 = adsk.core.Point3D.create(0, 1, 0)
        # point2 = adsk.core.Point3D.create(1, 1, 0)
        # point3 = adsk.core.Point3D.create(1, 0, 0)

        point0 = adsk.core.Point3D.create(0, 0, 0)
        point1 = adsk.core.Point3D.create(0, length, 0)
        point2 = adsk.core.Point3D.create(depth, length, 0)
        point3 = adsk.core.Point3D.create(depth, 0, 0)

        # Create Lines
        lines.addByTwoPoints(point0, point1)
        lines.addByTwoPoints(point1, point2)
        lines.addByTwoPoints(point2, point3)
        lines.addByTwoPoints(point3, point0)

        # Get the profile defined by the circle
        profile = sketch.profiles.item(0)

        # Create an extrusion input
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Define that the extent is a distance extent of 1 cm
        distance = adsk.core.ValueInput.createByReal(height)

        # Set the distance extent to be single direction
        extInput.setDistanceExtent(False, distance)

        # Set the extrude to be a solid one
        extInput.isSolid = True

        # Create the extrusion
        extrudes.add(extInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

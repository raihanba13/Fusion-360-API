#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        # upto this point, we create a blank new document
        design = app.activeProduct
        
        # Get the root component of the active design.
        rootComp = design.rootComponent

        lengthInput = ui.inputBox("Enter a length:", "Length", "12")
        widthInput = ui.inputBox("Enter a Width:", "Width", "6")
        heightInput = ui.inputBox("Enter a Height:", "Height", "5")
        thicknessInput = ui.inputBox("Enter a Thickness:", "Thickness", ".5")

        length = float(lengthInput[0])
        width = float(widthInput[0])
        height = float(heightInput[0])
        thickness = float(thicknessInput[0])

        if thickness >= width:
            # not the best way to exit! :(
            raise ValueError('Thickness can not be more than width!')
        
        # Create a new sketch1 on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch1 = sketches.add(xyPlane)

        lines = sketch1.sketchCurves.sketchLines
        recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(length, width,0))
        
        sketch1.geometricConstraints.addHorizontal(recLines.item(0))
        sketch1.geometricConstraints.addHorizontal(recLines.item(2))
        sketch1.geometricConstraints.addVertical(recLines.item(1))
        sketch1.geometricConstraints.addVertical(recLines.item(3))

        prof = sketch1.profiles.item(0)

        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Define that the extent is a distance extent of 5 cm.
        distance = adsk.core.ValueInput.createByReal(height)
        extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Get the body of the extrusion       
        body1 = extrude1.bodies.item(0)
        body1.name = "distance, from profile"

        # Create a collection of entities for shell
        entities1 = adsk.core.ObjectCollection.create()
        entities1.add(extrude1.endFaces.item(0))

        # Create a shell feature
        shellFeats = rootComp.features.shellFeatures
        isTangentChain = False
        shellFeatureInput = shellFeats.createInput(entities1, isTangentChain)
        thickness = adsk.core.ValueInput.createByReal(thickness)
        shellFeatureInput.insideThickness = thickness
        shellFeats.add(shellFeatureInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

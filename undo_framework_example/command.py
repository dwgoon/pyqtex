from qtpy.QtCore import QPointF
from qtpy.QtCore import qrand
from qtpy.QtWidgets import QUndoCommand

from diagramitem import DiagramItem
from diagramitem import DiagramItemType


def createCommandString(item, pos):

    if item.itemType() == DiagramItemType.Box:
        itemType = "Box"
    else:
        itemType = "Triangle"
        
    return "%s at (%f, %f)"%(itemType, pos.x(), pos.y())


class MoveCommand(QUndoCommand):
    Id = 1234
    
    def __init__(self, diagramItem, oldPos, parent=None):
        super().__init__(parent)
        self.myDiagramItem = diagramItem
        self.newPos = diagramItem.pos()
        self.myOldPos = oldPos
        
    def id(self):
        return self.Id
    
    """
    def mergeWith(self, command):
        moveCommand = command
        item = moveCommand.myDiagramItem

        if self.myDiagramItem != item:
            return False

        self.newPos = item.pos();
        self.setText("Move %s"%createCommandString(self.myDiagramItem, self.newPos))

        return True
    """

    def undo(self):
        self.myDiagramItem.setPos(self.myOldPos)
        self.myDiagramItem.scene().update()
        self.setText("Move %s"%createCommandString(self.myDiagramItem, self.newPos))
    
    def redo(self):
        self.myDiagramItem.setPos(self.newPos)
        self.setText("Move %s"%createCommandString(self.myDiagramItem, self.newPos))
    

class DeleteCommand(QUndoCommand):

    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.myGraphicsScene = scene;
        items = self.myGraphicsScene.selectedItems()
        items[0].setSelected(False)
        self.myDiagramItem = items[0]
        fstr = "Delete %s"%createCommandString(self.myDiagramItem,
                                               self.myDiagramItem.pos())
        self.setText(fstr)

    def undo(self):
        self.myGraphicsScene.addItem(self.myDiagramItem)
        self.myGraphicsScene.update()

    def redo(self):
        self.myGraphicsScene.removeItem(self.myDiagramItem)
    

class AddCommand(QUndoCommand):
   
    def __init__(self, addType, scene, parent=None):
        super().__init__(parent)
    
        self.myGraphicsScene = scene
        self.myDiagramItem = DiagramItem(addType)
        self.initialPosition = QPointF((qrand() % 10) + int(scene.width()/2),
                                       (qrand() % 10) + int(scene.height()/2))
        scene.update()
        
        fstr = "Add %s"%(createCommandString(self.myDiagramItem,
                                             self.initialPosition))
        self.setText(fstr)
    
    def __del__(self):
        if not self.myDiagramItem.scene():
            del self.myDiagramItem

    def undo(self):
        self.myGraphicsScene.removeItem(self.myDiagramItem)
        self.myGraphicsScene.update()
    
    def redo(self):
        self.myGraphicsScene.addItem(self.myDiagramItem)
        self.myDiagramItem.setPos(self.initialPosition)
        self.myGraphicsScene.clearSelection()
        self.myGraphicsScene.update()


from qtpy.QtCore import Qt
from qtpy.QtCore import QObject
from qtpy.QtCore import QPointF
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QGraphicsScene

from diagramitem import DiagramItem

class DiagramScene(QGraphicsScene):

    itemMoved = Signal(DiagramItem, QPointF)

    def __init__(self, parent):
        super().__init__(parent)
        self.mainWindow = parent
        self.movingItem = None
        self.oldPos = None


    def mousePressEvent(self, event): # QGraphicsSceneMouseEvent
        mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(),
                           event.buttonDownScenePos(Qt.LeftButton).y())
        
        itemList = self.items(mousePos)
        self.movingItem = None if not itemList else itemList[0]

        if (self.movingItem != None and event.button() == Qt.LeftButton):
            self.oldPos = self.movingItem.pos()

        self.clearSelection()
        super().mousePressEvent(event)

        
    def mouseReleaseEvent(self, event):
        if (self.movingItem != None and event.button() == Qt.LeftButton):
            if (self.oldPos != self.movingItem.pos()):
                self.itemMoved.emit(self.movingItem, self.oldPos)
                               
            self.movingItem = None
        
        super().mouseReleaseEvent(event)

        
        
        
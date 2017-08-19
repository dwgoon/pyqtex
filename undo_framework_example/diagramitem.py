from qtpy.QtCore import QPointF
from qtpy.QtCore import qrand
from qtpy.QtWidgets import QGraphicsItem
from qtpy.QtWidgets import QGraphicsScene
from qtpy.QtWidgets import QGraphicsSceneMouseEvent
from qtpy.QtWidgets import QGraphicsPolygonItem
from qtpy.QtGui import QPolygonF
from qtpy.QtGui import QColor
from qtpy.QtGui import QBrush


class DiagramItemType(object):
    Box = 0
    Triangle = 1

class DiagramItem(QGraphicsPolygonItem):

    Type = QGraphicsItem.UserType + 1
    
    def __init__(self, diagramItemType, item=None):
        super().__init__(item)
        
        self.boxPolygon = QPolygonF()
        self.trianglePolygon = QPolygonF()        
        
        if diagramItemType == DiagramItemType.Box:
            self.boxPolygon << QPointF(0, 0) << QPointF(0, 30) << QPointF(30, 30) \
                            << QPointF(30, 0) << QPointF(0, 0)
            self.setPolygon(self.boxPolygon)
        else:
            self.trianglePolygon << QPointF(15, 0) << QPointF(30, 30) << QPointF(0, 30) \
                                 << QPointF(15, 0)
            self.setPolygon(self.trianglePolygon)        

        color = QColor(qrand()%256, qrand()%256, qrand()%256)
        brush = QBrush(color)
        self.setBrush(brush)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def itemType(self):
        if self.polygon() == self.boxPolygon:
            return DiagramItemType.Box 
        else:
            return DiagramItemType.Triangle
    
    def type(self):
        return self.Type

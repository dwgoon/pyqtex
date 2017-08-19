from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QAction
from qtpy.QtWidgets import QMessageBox
from qtpy.QtWidgets import QUndoStack, QUndoView
from qtpy.QtWidgets import QGraphicsView
from qtpy.QtGui import QKeySequence
from qtpy.QtCore import QRectF
from qtpy.QtCore import QPointF
from qtpy.QtCore import Slot
from qtpy.QtCore import Qt

from diagramitem import DiagramItem
from diagramitem import DiagramItemType
from diagramscene import DiagramScene
from command import AddCommand
from command import DeleteCommand
from command import MoveCommand

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.undoStack = QUndoStack(self)
        self.createActions()
        self.createMenus()
        self.createUndoView()

        self.diagramScene = DiagramScene(self)
        self.diagramScene.setSceneRect(QRectF(0, 0, 500, 500))
        self.diagramScene.itemMoved.connect(self.onItemMoved)

        self.setWindowTitle("Undo Framework")
        view = QGraphicsView(self.diagramScene)
        self.setCentralWidget(view)
        self.resize(700, 500)
        
    def createUndoView(self):
        self.undoView = QUndoView(self.undoStack)
        self.undoView.setWindowTitle("Command List")
        self.undoView.show()
        self.undoView.setAttribute(Qt.WA_QuitOnClose, False)
        
    def createActions(self):
        self.deleteAction = QAction("&Delete Item", self)
        self.deleteAction.setShortcut("Del")
        self.deleteAction.triggered.connect(self.deleteItem)

        self.addBoxAction = QAction("Add &Box", self)
        self.addBoxAction.setShortcut("Ctrl+O")
        self.addBoxAction.triggered.connect(self.addBox)

        self.addTriangleAction = QAction("Add &Triangle", self)
        self.addTriangleAction.setShortcut("Ctrl+T")
        self.addTriangleAction.triggered.connect(self.addTriangle)

        self.undoAction = self.undoStack.createUndoAction(self, "&Undo")
        self.undoAction.setShortcuts(QKeySequence.Undo)

        self.redoAction = self.undoStack.createRedoAction(self, "&Redo")
        self.redoAction.setShortcuts(QKeySequence.Redo)

        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcuts(QKeySequence.Quit)
        self.exitAction.triggered.connect(self.close)

        self.aboutAction = QAction("&About", self)
        self.aboutShortcuts = list()
        self.aboutShortcuts.append("Ctrl+A")
        self.aboutShortcuts.append("Ctrl+B")
        self.aboutAction.setShortcuts(self.aboutShortcuts)
        self.aboutAction.triggered.connect(self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.aboutToShow.connect(self.itemMenuAboutToShow)
        self.editMenu.aboutToHide.connect(self.itemMenuAboutToHide)

        self.itemMenu = self.menuBar().addMenu("&Item")
        self.itemMenu.addAction(self.addBoxAction)
        self.itemMenu.addAction(self.addTriangleAction)

        helpMenu = self.menuBar().addMenu("&About")
        helpMenu.addAction(self.aboutAction)

    def isAnySelected(self):
        return len(self.diagramScene.selectedItems()) != 0
        
    @Slot(DiagramItem, QPointF)    
    def onItemMoved(self, movedItem, oldPosition):
        self.undoStack.push(MoveCommand(movedItem, oldPosition))
    
    @Slot()
    def deleteItem(self):
        if not self.isAnySelected():
            return
        
        deleteCommand = DeleteCommand(self.diagramScene)
        self.undoStack.push(deleteCommand)

    @Slot()
    def itemMenuAboutToHide(self):
        self.deleteAction.setEnabled(True)
    
    @Slot()
    def itemMenuAboutToShow(self):
        self.deleteAction.setEnabled(self.isAnySelected())
    
    @Slot()
    def addBox(self):
        addCommand = AddCommand(DiagramItemType.Box,
                                self.diagramScene)
        self.undoStack.push(addCommand)

    @Slot()
    def addTriangle(self):
        addCommand = AddCommand(DiagramItemType.Triangle,
                                self.diagramScene)
        self.undoStack.push(addCommand)
    
    @Slot()
    def about(self):
        QMessageBox.about(self, "About Undo",
                          "The <b>Undo</b> example demonstrates how to "
                          "use Qt's undo framework in PyQt.")

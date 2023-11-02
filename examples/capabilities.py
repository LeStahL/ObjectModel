from objectmodel.objectmodel import ObjectModel
from objectmodel.objectitemdelegate import ObjectItemDelegate
from typing import (
    Self,
    List,
)
from enum import (
    StrEnum,
    IntFlag,
    IntEnum,
    auto,
)
from sys import (
    argv,
    exit,
)
from PyQt6.QtWidgets import (
    QApplication,
    QTreeView,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QFileInfo

class AnEnum(StrEnum):
    Option1 = 'foo'
    Option2 = 'bar'

class AnIntEnum(IntEnum):
    A = auto()
    B = auto()

class AFlag(IntFlag):
    Nothing = 0
    First = auto()
    Second = auto()
    Third = auto()

class OtherDataClass:
    def __init__(
        self: Self,
        variable: str,
    ) -> None:
        self.AVariable = variable
        self.file = QFileInfo()

class DataClass:
    ClassVariable: int = 0

    def __init__(self: Self) -> None:
        self.InstanceVariable: int = 1
        self.StringVariable: str = "hello, world!"
        self.FloatVariable: float = 1.337
        self.BoolVariable: bool = False
        self.ArrayVariable: List[OtherDataClass] = [
            OtherDataClass("foo"),
            OtherDataClass("bar"),
            OtherDataClass("baz"),
            OtherDataClass("bad"),
        ]
        self.EnumVariable: AnEnum = AnEnum.Option2
        self.IntEnumVariable: AnIntEnum = AnIntEnum.B
        self.FlagVariable: AFlag = AFlag.Second | AFlag.Third

    def anotherFunc(self: Self) -> None:
        pass

if __name__ == '__main__':
    app = QApplication(argv)

    treeView = QTreeView()
    objectModel = ObjectModel()
    treeView.setModel(objectModel)
    objectModel.load(
        name='dataClass',
        object=DataClass(),
    )
    objectItemDelegate = ObjectItemDelegate()
    treeView.setItemDelegate(objectItemDelegate)

    undoAction = QAction("Undo", treeView)
    undoAction.setShortcut("CTRL+z")
    undoAction.triggered.connect(objectModel.undoStack.undo)
    redoAction = QAction("Undo", treeView)
    redoAction.setShortcut("CTRL+SHIFT+z")
    redoAction.triggered.connect(objectModel.undoStack.redo)
    treeView.addActions((undoAction, redoAction))

    treeView.show()
    exit(app.exec())

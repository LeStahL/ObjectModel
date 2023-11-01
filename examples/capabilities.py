from objectmodel.node import Node
from objectmodel.objectmodel import ObjectModel
from typing import (
    Self,
    List,
)
from enum import (
    StrEnum,
    IntFlag,
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

class AnEnum(StrEnum):
    Option1 = 'foo'
    Option2 = 'bar'

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

class DataClass:
    ClassVariable: int = 0

    def __init__(self: Self) -> None:
        self.InstanceVariable: int = 1
        self.StringVariable: str = "hello, world!"
        self.FloatVariable: float = 1.337
        self.ArrayVariable: List[OtherDataClass] = [
            OtherDataClass("foo"),
            OtherDataClass("bar"),
            OtherDataClass("baz"),
            OtherDataClass("bad"),
        ]
        self.EnumVariable: AnEnum = AnEnum.Option2
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

    treeView.show()
    exit(app.exec())
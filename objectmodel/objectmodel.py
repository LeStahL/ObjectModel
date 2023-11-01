from typing import (
    Optional,
    Self,
    Any,
)
from PyQt6.QtCore import (
    QModelIndex,
    QObject,
    QAbstractItemModel,
    Qt,
)
from objectmodel.node import Node

class ObjectModel(QAbstractItemModel):
    def __init__(
        self: Self,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)

        self._rootNode = Node(value='Empty')

    def load(self: Self, name: str, object: Any) -> None:
        self.beginResetModel()
        self._rootNode = Node(value=object, name=name)
        self.endResetModel()

    def index(
        self: Self,
        row: int,
        column: int,
        parent: QModelIndex = QModelIndex(),
    ) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()        
        return self.createIndex(row, column, self.parentNode(parent).children[row])

    def parent(self: Self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()
        
        childNode: Node = index.internalPointer()
        parentNode: Node = childNode.parent

        if parentNode == self._rootNode or parentNode is None:
            return QModelIndex()

        return self.createIndex(parentNode.index, 0, parentNode)

    def rowCount(self: Self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.column() > 0:
            return 0

        return len(self.parentNode(parent).children)

    def parentNode(self: Self, index: QModelIndex) -> Node:
        return index.internalPointer() if index.isValid() else self._rootNode

    def columnCount(self: Self, parent: QModelIndex = QModelIndex()) -> int:
        return 3
    
    def data(
        self: Self,
        index: QModelIndex,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        
        node: Node = index.internalPointer()

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return node.name
            elif index.column() == 1:
                return node.value
            elif index.column() == 2:
                return node.type.__name__

        return None

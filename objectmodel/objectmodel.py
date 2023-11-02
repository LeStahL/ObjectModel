from typing import (
    Optional,
    Self,
    Any,
    List,
)
from PyQt6.QtCore import (
    QModelIndex,
    QObject,
    QAbstractItemModel,
    Qt,
)
from PyQt6.QtGui import (
    QUndoStack,
)
from objectmodel.node import Node
from objectmodel.undovaluechange import UndoValueChange

class ObjectModel(QAbstractItemModel):
    HeaderNames = [
        'Name',
        'Value',
        'Type',
    ]

    def __init__(
        self: Self,
        undoStack: Optional[QUndoStack] = None,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)

        self._rootNode = Node(value='Empty')
        self._undoStack = QUndoStack() if undoStack is None else undoStack

    @property
    def undoStack(self: Self) -> QUndoStack:
        return self._undoStack

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
                if node.isArray:
                    return None
                if node.isObject:
                    return None
                if node.isEnum:
                    return node.value.name

                return str(node.value)

            elif index.column() == 2:
                return node.type.__name__

        return None

    def setData(
        self: Self,
        index: QModelIndex,
        value: Any,
        role: Qt.ItemDataRole = Qt.ItemDataRole.EditRole,
    ) -> bool:
        if not index.isValid():
            return False

        if role == Qt.ItemDataRole.EditRole:
            self._undoStack.push(UndoValueChange(index, value))
            return True

        return False
    
    def indexWithPath(self: Self, path: str) -> QModelIndex:
        return list(filter(
            lambda index: index.internalPointer().path == path,
            self.match(self.createIndex(0, 0, self._rootNode), Qt.ItemDataRole.DisplayRole, path.split('.')[-1], -1, Qt.MatchFlag.MatchRecursive),
        ))[0]

    def flags(self: Self, index: QModelIndex) -> Qt.ItemFlag:
        _flags = super().flags(index)
        if index.column() == 1:
            _flags = _flags | Qt.ItemFlag.ItemIsEditable
        return _flags

    def headerData(
        self: Self,
        section: int,
        orientation: Qt.Orientation,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return ObjectModel.HeaderNames[section]
        
        return None

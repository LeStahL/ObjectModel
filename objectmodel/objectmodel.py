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
    QColor,
)
from objectmodel.node import Node
from objectmodel.undovaluechange import UndoValueChange
from objectmodel.colormap import ColorMap
from copy import deepcopy

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
        self._undoStack.clear()
        self._undoStack.setClean()
        self._rootNode = Node(value=object, name=name)
        self._colorMap = ColorMap(self._rootNode.maxDepth)
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
                if node.isFilePath:
                    return '/'.join(map(lambda component: component[0] if len(component) > 0 else '', node.value.path().split('/'))) + '/' + node.value.fileName()

                return str(node.value)

            elif index.column() == 2:
                return node.type.__name__
            
        elif role == Qt.ItemDataRole.BackgroundRole:
            useDarkPalette: bool = index.row() % 2 == 0
            color: QColor = self._colorMap.colors[node.depth]
            return color if useDarkPalette else color.lighter(115)
        
        elif role == Qt.ItemDataRole.ForegroundRole:
            useDarkPalette: bool = index.row() % 2 == 0
            color: QColor = self._colorMap.colors[node.depth]
            return QColor(Qt.GlobalColor.black if 0.299 * color.redF() + 0.587 * color.greenF() + 0.114 * color.blueF() > 186.0 / 255. else Qt.GlobalColor.white)

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

    def addArrayElementAt(
        self: Self,
        index: QModelIndex,
        value: Optional[Any] = None,
    ) -> None:
        if not index.isValid():
            return

        parentNode: Node = self.parentNode(index)
        if parentNode is None:
            return

        self.beginInsertRows(index.parent(), index.row(), index.row())
        index.parent().internalPointer().insertArrayElement(index.row(), index.internalPointer().type() if value is None else value)
        self.endInsertRows()

        self.rowsInserted.emit(index.parent(), index.row(), index.row())

    def removeArrayElementAt(
        self: Self,
        index: QModelIndex,
    ) -> None:
        if not index.isValid():
            return

        parentNode: Node = self.parentNode(index)
        if parentNode is None:
            return

        self.beginRemoveRows(index.parent(), index.row(), index.row())
        index.parent().internalPointer().removeArrayElement(index.row())
        self.endRemoveRows()

        self.rowsRemoved.emit(self.parent(index), index.row(), index.row())

from PyQt6.QtGui import QUndoCommand
from PyQt6.QtCore import (
    QModelIndex,
    Qt,
)
from typing import (
    Self,
    Any,
)
from copy import (
    deepcopy,
)

class UndoValueChange(QUndoCommand):
    def __init__(
        self: Self,
        index: QModelIndex,
        newValue: Any,
    ) -> None:
        super().__init__()

        self._path = index.internalPointer().path
        self._oldValue = deepcopy(index.internalPointer().value)
        self._newValue = newValue
        self._model = index.model()

        self.setText("ValueChange")

    def redo(self: Self) -> None:
        index: QModelIndex = self._model.indexWithPath(self._path)
        index.internalPointer().value = self._newValue
        self._model.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
        self._model.layoutChanged.emit()

    def undo(self: Self) -> None:
        index: QModelIndex = self._model.indexWithPath(self._path)
        index.internalPointer().value = self._oldValue
        self._model.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
        self._model.layoutChanged.emit()

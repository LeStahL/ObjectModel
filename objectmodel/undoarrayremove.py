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

class UndoArrayRemove(QUndoCommand):
    def __init__(
        self: Self,
        index: QModelIndex,
    ) -> None:
        super().__init__()

        self._path = index.internalPointer().path
        self._oldValue = index.internalPointer().value
        self._model = index.model()

        self.setText("ValueChange")

    def redo(self: Self) -> None:
        index: QModelIndex = self._model.indexWithPath(self._path)
        self._model.removeArrayElementAt(index)

    def undo(self: Self) -> None:
        index: QModelIndex = self._model.indexWithPath(self._path)
        self._model.addArrayElementAt(index, self._oldValue)

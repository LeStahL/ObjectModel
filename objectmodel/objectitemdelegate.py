from PyQt6.QtWidgets import (
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
    QComboBox,
    QFileDialog,
)
from PyQt6.QtCore import (
    QObject,
    QModelIndex,
    QAbstractItemModel,
    Qt,
    QFileInfo,
)
from typing import (
    Optional,
    Self,
)
from objectmodel.node import Node

class ObjectItemDelegate(QStyledItemDelegate):
    def __init__(self,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        
    def createEditor(self: Self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> QWidget:
        node: Node = index.internalPointer()

        if node == None:
            return super().createEditor(parent, option, index)

        if index.column() == 1:
            if node.isEnum:
                comboBox = QComboBox(parent)
                comboBox.addItems([enumKey.name for enumKey in node.type])
                return comboBox
            
            elif node.isBool:
                comboBox = QComboBox(parent)
                comboBox.addItems(['True', 'False'])
                return comboBox
            
            elif node.isFilePath:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
                dialog.setDirectory(node._value.path())
                dialog.setWindowTitle('Change {}'.format(node.name))
                return dialog

        return super().createEditor(parent, option, index)

    def setEditorData(
        self: Self,
        editor: Optional[QWidget],
        index: QModelIndex,
    ) -> None:
        node: Node = index.internalPointer()

        if node == None:
            super().setEditorData(editor, index)
            return
        
        if index.column() == 1:
            if node.isEnum:
                editor.setCurrentText(node.value.name)
            
            elif node.isBool:
                editor.setCurrentText(str(node.value))

        super().setEditorData(editor, index)

    def setModelData(
        self: Self,
        editor: Optional[QWidget],
        model: Optional[QAbstractItemModel],
        index: QModelIndex,
    ) -> None:
        node: Node = index.internalPointer()
        
        if node == None:
            super().setModelData(editor, model, index)
            return
        
        if index.column() == 1:
            if node.isEnum:
                model.setData(index, getattr(node.type, editor.currentText()), Qt.ItemDataRole.EditRole)
                return

            if node.isFloat:
                try:
                    model.setData(index, float(editor.text()), Qt.ItemDataRole.EditRole)
                except:
                    pass
                return

            if node.isInt:
                try:
                    model.setData(index, int(editor.text()), Qt.ItemDataRole.EditRole)
                except:
                    pass
                return
            
            if node.isBool:
                try:
                    model.setData(index, editor.currentText() == 'True', Qt.ItemDataRole.EditRole)
                except:
                    pass
                return
            
            if node.isFilePath:
                try:
                    if editor.result() == QFileDialog.DialogCode.Rejected:
                        return

                    selectedFiles = editor.selectedFiles()
                    model.setData(index, QFileInfo(selectedFiles[0]), Qt.ItemDataRole.EditRole)
                except:
                    pass
                return

        super().setModelData(editor, model, index)

# Launcher widget for FreeCAD
# Copyright (C) 2016  triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


from PySide import QtGui
from PySide import QtCore


def singleInstance():
    from PySide import QtGui

    mw = FreeCADGui.getMainWindow()

    if mw:
        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "Launcher":
                i.deleteLater()
            else:
                pass
    else:
        pass

singleInstance()


def dockWidget():
    from PySide import QtGui
    from PySide import QtCore

    mw = FreeCADGui.getMainWindow()

    class LauncherEdit(QtGui.QLineEdit):
        def __init__(self, parent=None):
            super(LauncherEdit, self).__init__(parent)

        def focusInEvent(self, e):
            if e.reason() == QtCore.Qt.PopupFocusReason:
                pass
            else:
                modelData()

    completer = QtGui.QCompleter()
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

    edit = LauncherEdit()
    edit.setCompleter(completer)

    model = QtGui.QStandardItemModel()
    completer.setModel(model)

    widget = QtGui.QDockWidget()
    widget.setWindowTitle("Launcher")
    widget.setObjectName("Launcher")
    widget.setWidget(edit)

    if mw:
        mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, widget)
    else:
        pass

    def modelData():

        actions = {}
        duplicates = []

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName() is not None:
                if i.objectName() != "":
                    if i.objectName() in actions:
                        if i.objectName() not in duplicates:
                            duplicates.append(i.objectName())
                        else:
                            pass
                    else:
                        actions[i.objectName()] = i
                else:
                    pass
            else:
                pass

        for d in duplicates:
            del actions[d]

        rows = len(actions)

        model.clear()
        model.setRowCount(rows)
        model.setColumnCount(1)

        row = 0

        wbList = FreeCADGui.listWorkbenches()

        for i in actions:

            item = QtGui.QStandardItem()
            item.setText((actions[i].text()).replace("&", ""))
            item.setIcon(actions[i].icon())
            item.setToolTip(actions[i].toolTip())
            item.setEnabled(actions[i].isEnabled())
            item.setData(actions[i].objectName(), QtCore.Qt.UserRole)

            if actions[i].objectName() in wbList:
                item.setData("Workbench", 33)
            else:
                pass

            model.setItem(row, 0, item)
            row = row + 1

    def onReturnPressed():

        edit.clear()
        modelData()

    edit.returnPressed.connect(onReturnPressed)

    def onCompleter(modelIndex):

        actions = {}

        for i in mw.findChildren(QtGui.QAction):
            actions[i.objectName()] = i

        index = completer.completionModel().mapToSource(modelIndex)
        item = model.itemFromIndex(index)
        data = item.data(QtCore.Qt.UserRole)

        if data in actions:
            actions[data].trigger()
        else:
            pass

        if item.data(33) == "Workbench":
            modelData()
        else:
            pass

    completer.activated[QtCore.QModelIndex].connect(onCompleter)

dockWidget()

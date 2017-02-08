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


def singleInstance():
    """
    Only have one instance of Launcher running.
    """
    import FreeCADGui as Gui
    from PySide import QtGui

    mw = Gui.getMainWindow()

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
    """
    Launcher widget for FreeCAD
    """
    import FreeCADGui as Gui
    from PySide import QtGui
    from PySide import QtCore

    mw = Gui.getMainWindow()

    icon = """<svg xmlns="http://www.w3.org/2000/svg" height="64" width="64">
              <rect height="64" width="64" fill="none" />
              </svg>"""

    iconPixmap = QtGui.QPixmap()
    iconPixmap.loadFromData(icon)

    class LauncherEdit(QtGui.QLineEdit):
        """
        Define completer show/hide behavior.
        """
        def __init__(self, parent=None):
            super(LauncherEdit, self).__init__(parent)

        def focusInEvent(self, e):
            """
            Prevent updating model data after closing completer.
            """
            if e.reason() == QtCore.Qt.PopupFocusReason:
                pass
            else:
                modelData()

        def keyPressEvent(self, e):
            """
            Show completer after down key is pressed.
            """
            if e.key() == QtCore.Qt.Key_Down:
                edit.clear()
                completer.setCompletionPrefix("")
                completer.complete()
            else:
                QtGui.QLineEdit.keyPressEvent(self, e)

    completer = QtGui.QCompleter()
    completer.setMaxVisibleItems(16)
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
        """
        Fill the model with model items.
        """
        actions = {}
        duplicates = []

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName():
                if i.objectName() in actions:
                    if i.objectName() not in duplicates:
                        duplicates.append(i.objectName())
                    else:
                        pass
                else:
                    actions[i.objectName()] = i
            else:
                pass

        for d in duplicates:
            del actions[d]

        rows = len(actions)

        model.clear()
        model.setRowCount(rows)
        model.setColumnCount(1)

        row = 0

        for i in actions:

            item = QtGui.QStandardItem()
            item.setText((actions[i].text()).replace("&", ""))
            if actions[i].icon():
                item.setIcon(actions[i].icon())
            else:
                item.setIcon(QtGui.QIcon(QtGui.QIcon(iconPixmap)))
            item.setToolTip(actions[i].toolTip())
            item.setEnabled(actions[i].isEnabled())
            item.setData(actions[i].objectName(), QtCore.Qt.UserRole)

            model.setItem(row, 0, item)
            row += 1

    def onReturnPressed():
        """
        Clear line edit and update model data after enter key is pressed.
        """
        edit.clear()
        modelData()

    edit.returnPressed.connect(onReturnPressed)

    def onCompleter(modelIndex):
        """
        When command is selected and triggered run it and update model data.
        """
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

        modelData()

    completer.activated[QtCore.QModelIndex].connect(onCompleter)

    a = QtGui.QAction(mw)
    mw.addAction(a)
    a.setText("Launcher")
    a.setObjectName("Std_Launcher")
    # a.setShortcut(QtGui.QKeySequence("L"))

    a.triggered.connect(edit.setFocus)

dockWidget()

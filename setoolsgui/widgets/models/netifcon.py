# Copyright 2016, Tresys Technology, LLC
#
# SPDX-License-Identifier: LGPL-2.1-only
#
#
from PyQt5.QtCore import Qt

from .table import SEToolsTableModel


class NetifconTableModel(SEToolsTableModel):

    """Table-based model for netifcons."""

    headers = ["Device", "Device Context", "Packet Context"]

    def data(self, index, role):
        if self.item_list and index.isValid():
            row = index.row()
            col = index.column()
            rule = self.item_list[row]

            if role == Qt.ItemDataRole.DisplayRole:
                if col == 0:
                    return rule.netif
                elif col == 1:
                    return str(rule.context)
                elif col == 2:
                    return str(rule.packet)

            elif role == Qt.ItemDataRole.UserRole:
                return rule

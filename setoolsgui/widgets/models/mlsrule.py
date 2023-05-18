# Copyright 2016, Tresys Technology, LLC
#
# SPDX-License-Identifier: LGPL-2.1-only
#
#
from PyQt5.QtCore import Qt

from .table import SEToolsTableModel


class MLSRuleTableModel(SEToolsTableModel):

    """A table-based model for MLS rules."""

    headers = ["Rule Type", "Source", "Target", "Object Class", "Default Range"]

    def data(self, index, role):
        if self.item_list and index.isValid():
            row = index.row()
            col = index.column()
            rule = self.item_list[row]

            if role == Qt.ItemDataRole.DisplayRole:
                if col == 0:
                    return rule.ruletype.name
                elif col == 1:
                    return rule.source.name
                elif col == 2:
                    return rule.target.name
                elif col == 3:
                    return rule.tclass.name
                elif col == 4:
                    return str(rule.default)

            elif role == Qt.ItemDataRole.UserRole:
                return rule

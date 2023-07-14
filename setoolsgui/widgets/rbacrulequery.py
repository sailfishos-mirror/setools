# SPDX-License-Identifier: LGPL-2.1-only

import logging
from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets
import setools

from . import criteria, tab
from .models.rbacrule import RBACRuleTableModel

if TYPE_CHECKING:
    from typing import Optional


class RBACRuleQueryTab(tab.TableResultTabWidget):

    """An RBAC rule query."""

    section = tab.AnalysisSection.Rules
    tab_title = "Role-based Access Control (RBAC) Rules"
    mlsonly = False

    def __init__(self, policy: "setools.SELinuxPolicy", _,
                 parent: "Optional[QtWidgets.QWidget]" = None) -> None:

        super().__init__(setools.RBACRuleQuery(policy), enable_criteria=True, parent=parent)

        self.setWhatsThis("<b>Search RBAC rules in a SELinux policy.</b>")

        #
        # Set up criteria widgets
        #
        rt = criteria.RBACRuleTypeCriteriaWidget("Rule Type",
                                                 self.query,
                                                 parent=self.criteria_frame)
        rt.setToolTip("The rule types for rule matching.")
        rt.setWhatsThis(
            """
            <p><b>Select rule types for rule matching.</b></p>

            <p>If a rule's has a one of the selected types, it will be returned.</p>
            """)

        src = criteria.RoleNameWidget("Source Role",
                                      self.query,
                                      "source",
                                      enable_regex=True,
                                      parent=self.criteria_frame)
        src.setToolTip("The source role for rule matching.")
        src.setWhatsThis(
            """
            <p><b>Enter the source role for rule matching.</b></p>

            <p>If regex is enabled, a regular expression is used for matching
            the role name instead of direct string comparison.</p>
            """)

        dst = criteria.TypeOrAttrNameWidget("Target Role/Type",
                                            self.query,
                                            "target",
                                            mode=criteria.TypeOrAttrNameMode.type_or_attribute,
                                            enable_regex=True,
                                            enable_indirect=True,
                                            parent=self.criteria_frame)
        # add roles to completion
        model = dst.criteria.completer().model()
        assert isinstance(model, QtCore.QStringListModel)
        completion = model.stringList()
        completion.extend(r.name for r in policy.roles())
        model.setStringList(completion)

        dst.setToolTip("The target role/type for rule matching.")
        dst.setWhatsThis(
            """
            <p><b>Enter the target role/type for rule matching.</b></p>

            <p>If regex is enabled, a regular expression is used for matching
            the role/type name instead of direct string comparison.</p>
            """)

        tclass = criteria.ObjClassCriteriaWidget("Object Class",
                                                 self.query,
                                                 "tclass",
                                                 parent=self.criteria_frame)
        tclass.setToolTip("The object class(es) for rule matching.")
        tclass.setWhatsThis(
            """
            <p><b>Select object classes for rule matching.</b></p>

            <p>A rule will be returned if its object class is one of the selected
            classes</p>
            """)

        dflt = criteria.RoleNameWidget("Default Role",
                                       self.query,
                                       "default",
                                       enable_regex=True,
                                       parent=self.criteria_frame)
        dflt.setToolTip("The default role for rule matching.")
        dflt.setWhatsThis(
            """
            <p><b>Enter the default role for rule matching.</b></p>

            <p>If a rule has this role as the default, it will be returned.
            Allow rules will not be returned.</p>
            """)

        # Add widgets to layout
        self.criteria_frame_layout.addWidget(rt, 0, 0, 1, 2)
        self.criteria_frame_layout.addWidget(src, 1, 0, 1, 1)
        self.criteria_frame_layout.addWidget(dst, 1, 1, 1, 1)
        self.criteria_frame_layout.addWidget(tclass, 2, 0, 1, 1)
        self.criteria_frame_layout.addWidget(dflt, 2, 1, 1, 1)
        self.criteria_frame_layout.addWidget(self.buttonBox, 3, 0, 1, 2)

        # Save widget references
        self.criteria = (rt, src, dst, tclass, dflt)

        # Set result table's model
        self.table_results_model = RBACRuleTableModel(self.table_results)


if __name__ == '__main__':
    import sys
    import warnings
    import pprint

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    warnings.simplefilter("default")

    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    widget = RBACRuleQueryTab(setools.SELinuxPolicy(), mw)
    mw.setCentralWidget(widget)
    mw.resize(widget.size())
    whatsthis = QtWidgets.QWhatsThis.createAction(mw)
    mw.menuBar().addAction(whatsthis)
    mw.setStatusBar(QtWidgets.QStatusBar(mw))
    mw.show()
    rc = app.exec_()
    pprint.pprint(widget.save())
    sys.exit(rc)

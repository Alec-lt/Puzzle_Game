"""
       ┌─┐       ┌─┐
    ┌──┘ ┴───────┘ ┴──┐
    │                 │
    │       ───       │
    │  ─┬┘       └┬─  │
    │                 │
    │       ─┴─       │
    │                 │
    └───┐         ┌───┘
        │         │
        │         │
        │         │
        │         └──────────────┐
        │                        │
        │                        ├─┐
        │                        ┌─┘
        │                        │
        └─┐  ┐  ┌───────┬──┐  ┌──┘
          │ ─┤ ─┤       │ ─┤ ─┤
          └──┴──┘       └──┴──┘
                 神兽保佑
                代码无BUG!
"""


from PyQt5.QtCore import pyqtSignal, QObject
import time


class AiThread(QObject):
    trigger = pyqtSignal()

    def __init__(self):
        super(AiThread, self).__init__()
        self.flag = 0

    def run(self):
        while self.flag > 0:
            self.flag -= 1
            self.trigger.emit()
            time.sleep(0.01)
        return


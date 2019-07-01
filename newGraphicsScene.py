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
from PyQt5.QtWidgets import QGraphicsScene


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.x = -1
        self.y = -1
        # 是否打乱过
        self.if_make_upset = False
        self.now_selected = -1

    def mousePressEvent(self, event):
        if self.if_make_upset is False:
            return
        pos = event.scenePos()
        self.x = pos.x()
        self.y = pos.y()


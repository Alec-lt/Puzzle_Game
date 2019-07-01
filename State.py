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
import gc


class Node(object):
    def __init__(self, map_list=[], man_distance=-1, g_value=0):
        """
        结点类  (i, j)为白块的位置
        :param map_list: 存取状态
        :param man_distance: 曼哈顿距离
        """
        self.map = map_list[:]
        self.man_distance = man_distance
        self.g_value = g_value


class Step(object):
    def __init__(self, pre=-1, ch=-1):
        """
        步类
        :param pre: 上一个步类结点
        :param ch: 方向
        """
        self.pre = pre
        self.ch = ch


class MinBinHeapq(object):
    """
    最小堆
    """
    def __init__(self):
        self.size = 0
        self.data = []

        node = Node()
        self.data.append(node)

    def pre_up(self, i):
        """
        上升结点
        :param i: 上升的结点编号
        :return:  void
        """
        while i // 2 > 0:
            if self.data[i].man_distance + self.data[i].g_value < self.data[i // 2].man_distance + self.data[i // 2].g_value:
                self.data[i // 2], self.data[i] = self.data[i], self.data[i // 2]
            i = i // 2

    def push(self, k):
        """
        插入结点操作
        :param k: 插入结点类
        :return: void
        """
        self.data.append(k)
        self.size += 1
        self.pre_up(self.size)

    def pre_down(self, i):
        """
        元素下潜
        :param i: 当前元素编号
        :return: void
        """
        while (i*2) <= self.size:
            mc = self.min_child(i)
            if self.data[i].man_distance + self.data[i].g_value > self.data[mc].man_distance + self.data[mc].g_value:
                self.data[i], self.data[mc] = self.data[mc], self.data[i]
            i = mc

    def min_child(self, i):
        """
        寻找最小的子孩子
        :param i: 当前结点的编号
        :return: 最小孩子的编号
        """
        if i * 2 + 1 > self.size:
            return i * 2
        else:
            if self.data[i*2].man_distance + self.data[i*2].g_value < self.data[i*2 + 1].man_distance + self.data[i*2 + 1].g_value:
                return i * 2
            else:
                return i * 2 + 1

    def pop(self):
        """
        弹出元素，先把头一个存一下，用最后一个的值赋值
        删除最后一个元素，最后再进行元素下潜
        :return: 结点类
        """
        value = self.data[1]
        self.data[1] = self.data[self.size]
        self.size = self.size - 1
        self.data.pop()
        # gc.collect()
        return value

    def empty(self):
        """
        判空
        :return: 空 True 非空 False
        """
        if self.size == 0:
            return True
        return False



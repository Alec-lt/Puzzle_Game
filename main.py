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
import sys
from vision import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread
from PIL import Image, ImageQt
import random
from newGraphicsScene import GraphicsScene
from State import Node, MinBinHeapq, Step
import time
from copy import deepcopy
from aiThread import AiThread


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        # 图像，保存原始图片
        self.image = None
        # 存储图像文件路径
        self.image_name = None
        # 存一下场景
        self.scene = GraphicsScene(self)
        # 列表元素总数，分块总数
        self.number = 0
        # 分块的图片列表
        self.c_image = []
        # 图的数组保存形式
        self.map = []
        # 合并的图片（主要操作展示对象）
        self.combine_image = None

        # 是否进行过的操作
        self.if_opened = False
        self.if_upset = False
        self.if_ai = False

        # 白块的位置
        self.white = -1
        # 方向
        # 0  1  2  3
        # 上 下 左 右
        self.direction = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.step_direction = [0, 1, 2, 3]

        # 分割维度
        self.dim = 3
        # 单个边长 （width, height）
        self.x = 0
        self.y = 0

        # A_star算法相关变量
        self.fac = []
        self.step_dict = {}
        self.hash_visited = {}
        self.steps = []
        self.order = 0
        self.backthread = None
        self.thread = None

        # 难度选择上下限
        self.selectHard.setMaximum(10)
        self.selectHard.setMinimum(3)

        # 计数君
        self.hhhh = 0

        # 槽函数
        self.upset.clicked.connect(self.make_upset)
        self.pictureChoose.clicked.connect(self.openfile)
        self.reset.clicked.connect(self.make_reset)
        self.AI.clicked.connect(self.ai_work)
        self.saveProgress.clicked.connect(self.save_progress)
        self.readProgress.clicked.connect(self.read_progress)

    def save_progress(self):
        self.close_ai()
        if self.if_upset:
            self.combine()
            self.combine_image.save("./source/combine_image.bmp")
            self.image.save("./source/image.bmp")
            file = open('./source/list.txt', 'w')
            for i in range(len(self.map)):
                file.write(str(self.map[i]))
                file.write('\t')
            file = open('./source/dim.txt', 'w')
            file.write(str(self.dim))
            file.close()
        return

    def read_progress(self):
        self.close_ai()

        if self.if_opened is True:
            self.scene.clear()

        self.if_opened = True
        self.scene.if_make_upset = True
        self.if_upset = True
        self.scene.now_selected = -1

        image_name = "./source/combine_image.bmp"

        self.combine_image = Image.open(image_name)

        self.image = Image.open("./source/image.bmp")

        self.image_name = image_name

        # 选择维度
        # self.dim = self.selectHard.value()
        file = open('./source/dim.txt', 'r')
        f = file.read()
        self.dim = int(f)
        file.close()

        dim = self.dim

        self.x = self.combine_image.size[0] / self.dim
        self.y = self.combine_image.size[1] / self.dim
        x = self.x
        y = self.y

        # 分块信息清空
        self.c_image.clear()
        self.map.clear()

        count = 0
        for j in range(dim):
            for i in range(dim):

                area = (i * x, j * y, i * x + x, j * y + y)
                image = Image.open(self.image_name)
                im = image.crop(area)
                self.c_image.append(im)

                count = count + 1

        # 数组形态的图赋初值
        file = open('./source/list.txt', 'r')
        f = file.readlines()
        mapp = []
        for i in f:
            k = i.strip()
            j = k.split('\t')
            mapp.append(j)
        file.close()
        for i in range(len(mapp[0])):
            self.map.append(int(mapp[0][i]))
        # for i in range(len(self.map)):
        #     print(self.map[i])

        # 分块总数，记录一下，用起来方便一些，说白了就是dim*dim
        self.number = count

        # self.white = self.map.index(0)

        self.combine()
        self.show_image()

        self.image_name = "./source/image.bmp"
        self.ai_fac()

    def openfile(self):
        """
        打开图片文件
        :return: None
        """
        self.close_ai()

        if self.if_opened is True:
            self.scene.clear()

        self.if_opened = True
        self.scene.if_make_upset = False

        image_name, image_type = QFileDialog.getOpenFileName(self, "choose a picture", "./source",
                                                             "*.jpeg;;*.jpg;;*.png;;*.bmp;;All Files (*)")

        self.image = Image.open(image_name)
        self.combine_image = self.image

        self.image_name = image_name

        pixmap = QtGui.QPixmap(image_name)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.showView.setScene(self.scene)

        self.ai_fac()

    def combine(self):
        """
        合并图片
        :return: None
        """
        h_image = Image.new('RGBA', (self.image.size[0], self.image.size[1]))

        count = 0
        for j in range(self.dim):
            for i in range(self.dim):

                location = (int(i*self.x), int(j*self.y))

                h_image.paste(self.c_image[count], location)

                count = count + 1
        self.combine_image = h_image.copy()

    def show_image(self):
        """
        展示图片
        :return: None
        """
        self.scene.clear()
        in_pixmap = ImageQt.ImageQt(self.combine_image)
        pixmap = QtGui.QPixmap.fromImage(in_pixmap)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.showView.setScene(self.scene)

    def make_upset(self):
        """
        打乱
        :return: None
        """
        self.close_ai()

        # 如果原图是空的，那么不行
        if self.image is None:
            return

        flag = False

        self.if_upset = True

        self.scene.if_make_upset = True
        self.scene.x = -1
        self.scene.y = -1
        self.scene.now_selected = -1

        self.dim = self.selectHard.value()
        dim = self.dim
        self.x = self.image.size[0] / dim
        self.y = self.image.size[1] / dim
        x = self.x
        y = self.y

        self.c_image.clear()

        count = 0
        for j in range(dim):
            for i in range(dim):

                if count == dim * dim - 1:
                    e_image = Image.new('RGB', (self.image.size[0], self.image.size[1]), color='#FFFFFF')
                    area = (0, 0, x, y)
                    im = e_image.crop(area)
                    self.c_image.append(im)
                    count = count + 1
                    break

                area = (i * x, j * y, i * x + x, j * y + y)
                image = self.image
                im = image.crop(area)
                self.c_image.append(im)

                count = count + 1

        # 数组形态的图赋初值
        self.map.clear()
        for k in range(count - 1):
            self.map.append(k + 1)
        self.map.append(0)

        # 分块总数，记录一下，用起来方便一些，说白了就是dim*dim
        self.number = count

        while flag is False:

            # 板块三轮换
            for i in range(int((count / 3) * (count / 3)) + 1):
                n = random.randint(0, count - 1)
                m = n
                while n == m:
                    m = random.randint(0, count - 1)
                o = m
                while o == m or o == n:
                    o = random.randint(0, count - 1)
                if n > m:
                    n, m = m, n
                if m > o:
                    m, o = o, m

                self.c_image[n], self.c_image[m] = self.c_image[m], self.c_image[n]
                self.c_image[m], self.c_image[o] = self.c_image[o], self.c_image[m]

                self.map[n], self.map[m] = self.map[m], self.map[n]
                self.map[m], self.map[o] = self.map[o], self.map[m]

            flag = self.whether_reduction()

        self.combine()
        self.show_image()

        self.white = self.map.index(0)

    def make_reset(self):
        """
        重置
        :return: None
        """
        self.close_ai()
        if self.image is None:
            return
        self.scene.if_make_upset = False
        self.scene.clear()
        pixmap = QtGui.QPixmap(self.image_name)
        self.scene.addPixmap(pixmap)
        self.showView.setScene(self.scene)

    def ai_manhattan(self, map_list=[]):
        """
        曼哈顿距离计算
        :return: distance
        """
        distance = 0
        for i in range(self.dim*self.dim):
            if map_list[i] == 0:
                continue
            cx = int(i / self.dim)
            cy = int(i % self.dim)
            gx = int((map_list[i]-1) / self.dim)
            gy = int((map_list[i]-1) % self.dim)
            distance += (abs(cx-gx) + abs(cy-gy))

        return 10 * distance

    def ai_fac(self):
        """
        计算阶乘数列
        :return: None
        """
        self.fac.append(1)
        for i in range(1, 26):
            self.fac.append(i*self.fac[i-1])

    def ai_to_hash(self, state=[]):
        """
        哈希化
        :param state: 状态数组
        :return: 哈希值
        """
        result = 0
        length = len(state)

        for i in range(length):
            k = 0
            for j in range(i+1, length):
                if state[i] > state[j]:
                    k += 1
            result = result + k*self.fac[length-i-1]

        return result

    def ai_step_print(self, hash_node):
        k = self.step_dict.get(hash_node)
        if k.pre == -1:
            return
        self.ai_step_print(k.pre)
        self.steps.append(k.ch)

    def ai_a_star(self):
        """
        执行A_star算法
        :return: None
        """

        q = MinBinHeapq()
        sta = Node(self.map)
        old_hash = self.ai_to_hash(sta.map)
        new_step = Step(-1, -1)
        self.step_dict.setdefault(old_hash, deepcopy(new_step))
        self.hash_visited.setdefault(old_hash, 1)

        q.push(deepcopy(sta))

        while not q.empty():
            self.hhhh += 1
            sta = deepcopy(q.pop())

            if sta.man_distance == -1:
                sta.man_distance = self.ai_manhattan(sta.map)

            if sta.man_distance == 0:
                self.ai_step_print(self.ai_to_hash(sta.map))
                break

            s = sta.map.index(0)
            sx = int(s / self.dim)
            sy = int(s % self.dim)
            old_man_distance = sta.man_distance
            old_g_value = sta.g_value
            old_hash = self.ai_to_hash(sta.map)

            for i in range(4):

                mi = sx + self.direction[i][0]
                mj = sy + self.direction[i][1]

                if mi < 0 or mi >= self.dim or mj < 0 or mj >= self.dim:
                    continue

                m = mi * self.dim + mj

                sta.map[s], sta.map[m] = sta.map[m], sta.map[s]

                # 通过字典 查看哈希值(状态)是否被访问过
                new_hash = self.ai_to_hash(sta.map)

                if self.hash_visited.get(new_hash) is None:
                    self.hash_visited.setdefault(new_hash, 1)

                    sta.man_distance = self.ai_manhattan(sta.map)
                    sta.g_value = old_g_value + 1

                    new_step.pre, new_step.ch = old_hash, i
                    self.step_dict.setdefault(new_hash, deepcopy(new_step))

                    q.push(deepcopy(sta))

                    sta.man_distance = old_man_distance
                    sta.g_value = old_g_value

                sta.map[s], sta.map[m] = sta.map[m], sta.map[s]

            del sta

        self.hash_visited.clear()
        del q

    def ai_work(self):
        """
        自动还原展示
        步数依据：self.steps = [...]
        :return: None
        """
        self.close_ai()
        if not self.if_upset:
            return

        # 步数的相关数据清空
        self.step_dict.clear()
        self.steps.clear()
        self.order = 0
        self.backthread = None
        self.thread = None

        self.if_upset = False
        self.if_ai = True
        self.scene.if_make_upset = False

        self.white = self.map.index(0)

        start = time.time()
        self.ai_a_star()
        end = time.time()
        print('搜索完成，共用时：', (end - start), '秒')
        print(self.steps)
        print('所需步数为：', len(self.steps))
        print('共搜索状态数：', self.hhhh)
        self.hhhh = 0

        self.backthread = AiThread()
        self.backthread.trigger.connect(self.ai_show)
        self.backthread.flag = len(self.steps)

        self.thread = QThread()
        self.backthread.moveToThread(self.thread)
        self.thread.started.connect(self.backthread.run)
        self.thread.start()

    def close_ai(self):
        if self.if_ai:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
        self.if_ai = False
        return

    def ai_show(self):

        di = self.steps[self.order]
        self.order += 1

        tx = int(self.white / self.dim) + self.direction[di][0]
        ty = int(self.white % self.dim) + self.direction[di][1]

        s = self.dim * tx + ty

        self.map[self.white], self.map[s] = self.map[s], self.map[self.white]
        self.c_image[self.white], self.c_image[s] = self.c_image[s], self.c_image[self.white]

        self.white = s

        self.combine()
        self.show_image()

    def whether_reduction(self):
        """
        能否还原检测
        :return: 能 True 不能 False
        """
        res = 0
        count = self.number
        for i in range(count):
            for j in range(i+1, count):
                if self.map[j] == 0:
                    continue
                if self.map[j] < self.map[i]:
                    res += 1

        if res % 2 == 0 and self.dim == 3 or (res + abs(int(self.map.index(0) / self.dim) - (self.dim - 1))) % 2 == 0:
            return True
        return False

    def mousePressEvent(self, event):
        """
        鼠标控制还原拼图
        :param event: 事件采集，关键是桌面点击像素坐标采集
        :return: None
        """
        self.close_ai()
        if self.scene.x == -1 or self.scene.y == -1:
            return
        if self.scene.if_make_upset is False:
            return
        x_rem = self.scene.x % self.x
        y_rem = self.scene.y % self.y
        x = int(self.scene.x / self.x)
        y = int(self.scene.y / self.y)

        if x_rem > 0:
            x += 1
        if y_rem > 0:
            y += 1
        s = (y-1)*self.dim + (x-1)

        if s == self.scene.now_selected:
            return
        if self.map[s] == 0:
            return

        self.scene.now_selected = s
        self.white = self.map.index(0)

        """
        横为 x 上 方向右
        竖为 y 左 方向下
        """
        tx = int(self.white / self.dim)
        ty = int(self.white % self.dim)

        find = False
        for i in range(4):
            sx = tx + self.direction[i][0]
            sy = ty + self.direction[i][1]

            if sx > self.dim-1 or sx < 0 or sy > self.dim-1 or sy < 0:
                continue
            if self.map[sx*self.dim + sy] == self.map[s]:
                find = True
                break

        if find:
            self.map[self.white], self.map[s] = self.map[s], self.map[self.white]
            self.c_image[self.white], self.c_image[s] = self.c_image[s], self.c_image[self.white]

            self.white = s

            self.combine()
            self.show_image()
        else:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())

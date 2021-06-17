import tkinter as tk
import time

textlist = []
origin = []
result = []
target = {}
num = 1
length=0
for i in range(4):
    for j in range(4):
        target[num] = (i, j)
        num += 1

    target[0] = (3, 3)


# 评估从现状态到目标状态需要的最少步数
def h(node):  # node即当前状态
    cost = 0
    for i in range(4):
        for j in range(4):
            num = node[i][j]
            x, y = target[num]
            cost += abs(x - i) + abs(y - j)  # 假设从当前到终态直接移动

    return cost


# 移动，拓展当前结点
def expand(node):
    x, y = 0, 0
    for i in range(4):
        for j in range(4):
            if (node[i][j] == 0):
                x, y = i, j  # 0所在的位置
    canmove = []
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 代表向上下左右移动
    for i, j in moves:
        a, b = x + i, y + j
        if (a < 4 and a > -1 and b < 4 and b > -1):
            temp = [[num for num in col] for col in node]  # 生成当前的临时状态
            temp[x][y] = temp[a][b]
            temp[a][b] = 0  # 移动0位置
            canmove.append(temp)

    return sorted(canmove, key=lambda x: h(x))  # 对存在的每个移动后的状态进行评估 h(x),并升序排列


# 判断是否为目标状态
def is_goal(node):
    index = 1
    for row in node:
        for col in row:
            if (index != col):
                break
            index += 1
    return index == 16


def search(path, g, bound):
    global length
    node = path[-1]  # 取path中最新的状态
    f = g + h(node)
    if (f > bound):
        return f  # 剪枝，跳过f超出阈值的状态
    if (is_goal(node)):  # 到达终态返回-1
        return -1

    Min = 9999
    for moved in expand(node):
        if moved not in path:  # 不重复执行
            length = length + 1

            path.append(moved)
            question.refresh_data(path)
            t = search(path, g + 1, bound)  # 移动一步，g+1
            if (t == -1):
                return -1
            if (t < Min):
                Min = t

            path.pop()
            question.refresh_data(path)

    return Min


def ida_star(root):
    bound = h(root)
    path = [root]

    while (True):
        t = search(path, 0, bound)
        if (t == -1):
            print("search length is %d" % (length))
            return (path, bound)  # 到达终态

        if (t > 70):
            print("search length is %d" % (length))
            return ([], bound)  # 未找到返回空列表


        bound = t



def load():
    # root = [2,  7,  5,  3], [11, 10,  9, 14], [4,  0,  1,  6], [4,  0,  1,  6]
    # root = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]
    # root = [[5, 1, 3, 4], [2, 7, 8, 12], [9, 6, 11, 15], [0, 13, 10, 14]]  # 15
    # root = [[6, 10, 3, 15], [14, 8, 7, 11], [5, 1, 0, 2], [13, 12, 9, 4]]
    root = [[11, 9, 4, 15],[1, 3, 0, 12],[7, 5, 8, 6],[13, 2, 10, 14]]       #41
    # root = [[2, 3, 4, 0], [1, 5, 7, 8], [9, 6, 10, 12], [13, 14, 11, 15]]
    return root


class UI(tk.Tk):
    def __init__(self, *args, **kw):
        super().__init__()
        self.wm_title('15-digits GUI')
        self.configure(background='white')
        self.geometry('700x210')

        for i in range(16):
            textlist.append(tk.Text(self, height=1, width=2))
            origin.append(tk.Text(self, height=1, width=2))
            result.append(tk.Text(self, height=1, width=2))

        for i in range(16):
            textlist[i].configure(font=("微软雅黑", 13))
            origin[i].configure(font=("微软雅黑", 13))
            result[i].configure(font=("微软雅黑", 13))

        label = tk.Label(self, text='15-digits', font=("微软雅黑", 15))
        label.grid(row=0, column=0)
        label2 = tk.Label(self, text='search', font=("微软雅黑", 15))
        label2.grid(row=0, column=6)
        label3 = tk.Label(self, text='result: ', font=("微软雅黑", 15))
        label3.grid(row=0, column=11)

        for i in range(16):
            if i == 0:
                origin[i].grid(row=1, column=2, padx=3, pady=3)
                textlist[i].grid(row=1, column=7, padx=3, pady=3)
                result[i].grid(row=1, column=12, padx=3, pady=3)
            elif 0 < i < 4:
                origin[i].grid(row=1, column=i + 2, padx=3)
                textlist[i].grid(row=1, column=i + 7, padx=3)
                result[i].grid(row=1, column=i + 12, padx=3)
            elif i == 4:
                origin[i].grid(row=2, column=2, padx=3, pady=3)
                textlist[i].grid(row=2, column=7, padx=3, pady=3)
                result[i].grid(row=2, column=12, padx=3, pady=3)
            elif 4 < i < 8:
                origin[i].grid(row=2, column=i - 2, padx=3)
                textlist[i].grid(row=2, column=i + 3, padx=3)
                result[i].grid(row=2, column=i + 8, padx=3, pady=3)
            elif i == 8:
                origin[i].grid(row=3, column=2, padx=3, pady=3)
                textlist[i].grid(row=3, column=7, padx=3, pady=3)
                result[i].grid(row=3, column=12, padx=3, pady=3)
            elif 8 < i < 12:
                origin[i].grid(row=3, column=i - 6, padx=3)
                textlist[i].grid(row=3, column=i - 1, padx=3)
                result[i].grid(row=3, column=i + 4, padx=3, pady=3)
            elif i == 12:
                origin[i].grid(row=4, column=2, padx=3, pady=3)
                textlist[i].grid(row=4, column=7, padx=3, pady=3)
                result[i].grid(row=4, column=12, padx=3, pady=3)
            elif 12 < i < 16:
                origin[i].grid(row=4, column=i - 10, padx=3)
                textlist[i].grid(row=4, column=i - 5, padx=3)
                result[i].grid(row=4, column=i, padx=3, pady=3)
        for i in range(4):
            for j in range(4):
                origin[i * 4 + j].delete('1.0', 'end')
                origin[i * 4 + j].insert('end', root[i][j])

        # self.refresh_data(0, textlist)

    def refresh_data(self, path):
        # 需要刷新数据的操作
        # 代码...

        pa = path[-1]
        for i in range(4):
            for j in range(4):
                textlist[i * 4 + j].delete('1.0', 'end')
                textlist[i * 4 + j].insert('end', pa[i][j])
                textlist[i].update()

        # time.sleep(1)
        # if is_goal(pa):
        #     self.mainloop()

    def show_result(self, path):
        pa = path[-1]
        for i in range(4):
            for j in range(4):
                result[i * 4 + j].delete('1.0', 'end')
                result[i * 4 + j].insert('end', pa[i][j])
                result[i].update()
        self.mainloop()




if __name__ == "__main__":
    length = 0
    time1 = time.time()
    root = load()  # 设置原始状态
    question = UI()
    (path, bound) = ida_star(root)  # path为搜寻过程中的状态转变
    time2 = time.time()
    step = 0

    if len(path) == 0:
        print("Not Found, time costs %f s" % (time2 - time1))
        print("Not")
    else:
        for p in path:
            print('step', step)
            step += 1
            for row in p:
                print(row)
        print("Found, time costs %f s" % (time2 - time1))
        print("search length is %d" % (length))
        print('bound', bound)
        question.show_result(path)


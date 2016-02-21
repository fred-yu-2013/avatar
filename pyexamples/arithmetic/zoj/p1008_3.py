TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Item():
    def __init__(self, rect):
        self.rect = rect
        self.count = 0

    def __str__(self):
        return str(self.rect) + str(self.count)

    def __eq__(self, other):
        return self.rect == other.rect


class Context():
    def __init__(self):
        self.index = 0  # Index of text cases.
        self.remain_count = None  # For one test case.
        self.n = 0
        self.n2 = 0
        self.items = []

        self.states = {LEFT: {}, RIGHT: {}, TOP: {}, BOTTOM: {}}
        # self.not_matched = {LEFT: [], TOP: [], RIGHT: [], BOTTOM: []}
        self.classes = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        self.classes_count = []

    def handle_line(self, line):
        # -> True if need end.
        if self.remain_count is None or self.remain_count == 0:
            self.n = int(line)
            if self.n == 0:
                return True
            if self.remain_count == 0:  # Except the first time.
                print ''
            self.index += 1
            self.n2 = self.n * self.n
            self.remain_count = self.n2
            self.items = []

            self.states = {LEFT: {}, RIGHT: {}, TOP: {}, BOTTOM: {}}
            # self.not_matched = {LEFT: [], TOP: [], RIGHT: [], BOTTOM: []}
            self.classes = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            self.classes_count = [1, self.n - 2, 1,
                                  self.n - 2, (self.n - 2) * (self.n - 2), self.n - 2,
                                  1, self.n - 2, 1]
        else:
            parts = line.split()
            new_item = Item(tuple(map(int, parts)))
            is_exist = False
            for item in self.items:
                if item == new_item:
                    item.count += 1
                    is_exist = True
                    break
            if not is_exist:
                new_item.count += 1
            self.items.append(new_item)
            self.__state_item(new_item)
            self.remain_count -= 1
            if self.remain_count == 0:
                res = True
                if self.n > 1:
                    if self.n > 2 and self.__is_impossible():
                        res = False
                    else:
                        res = self.gt(0, [None] * self.n2)
                print 'Game %d: %s' % (self.index, 'Possible' if res else 'Impossible')
        return False

    def __state_item(self, item):
        for d in [TOP, RIGHT, BOTTOM, LEFT]:
            if item.rect[d] not in self.states[d]:
                self.states[d][item.rect[d]] = [item]
            else:
                self.states[d][item.rect[d]].append(item)

    def __is_impossible(self):
        res = [False, False, False, False]
        for item in self.items:
            directions = [TOP, RIGHT, BOTTOM, LEFT]
            directions_r = [BOTTOM, LEFT, TOP, RIGHT]
            count = 0
            for i in range(4):
                if item.rect[directions[i]] not in self.states[directions_r[i]] \
                        or (len(self.states[directions_r[i]][item.rect[directions[i]]]) == 1 \
                        and self.states[directions_r[i]][item.rect[directions[i]]][0] == item):
                    # self.not_matched[directions[i]].append(item)
                    res[directions[i]] = True
                    count += 1
                else:
                    res[directions[i]] = False

            if count > 2 or (count == 2 and (res[0] and res[2]) or (res[1] and res[3])):
                return True

            t, r, b, l = map(lambda x: not x, res)
            if b:
                if r: self.classes[1].append(item)
                if l and r: self.classes[2].append(item)
                if l: self.classes[3].append(item)
            if b and t:
                if r: self.classes[4].append(item)
                if l and r: self.classes[5].append(item)
                if l: self.classes[6].append(item)
            if t:
                if r: self.classes[7].append(item)
                if l and r: self.classes[8].append(item)
                if l: self.classes[9].append(item)

        # for d in [TOP, RIGHT, BOTTOM, LEFT]:
        #     if len(self.not_matched[d]) > self.n:
        #         return True

        for i in range(9):
            if len(self.classes[i + 1]) < self.classes_count[i]:
                return True

        return False

    def gt(self, index, dst_ll):
        if index == self.n2:
            return True

        r, c = index / self.n, index % self.n
        # r_left, c_left = self.n - r - 1, self.n - c - 1
        top, left = index - self.n, index - 1

        for item in self.items:
            if item.count == 0:
                continue

            if r > 0 and item.rect[TOP] != dst_ll[top].rect[BOTTOM]:
                continue

            if c > 0 and item.rect[LEFT] != dst_ll[left].rect[RIGHT]:
                continue

            # if r == 0 and item not in self.not_matched[TOP] \
            #         and len(self.not_matched[TOP]) > c_left:
            #     continue
            #
            # if r + 1 == self.n and item not in self.not_matched[BOTTOM] \
            #         and len(self.not_matched[BOTTOM]) > c_left:
            #     continue
            #
            # if c == 0 and item not in self.not_matched[LEFT] \
            #         and len(self.not_matched[LEFT]) > r_left:
            #     continue
            #
            # if c + 1 == self.n and item not in self.not_matched[RIGHT] \
            #         and len(self.not_matched[RIGHT]) > r_left:
            #     continue

            # # old_not_matched = dict(self.not_matched)
            #
            # for d in [TOP, RIGHT, BOTTOM, LEFT]:
            #     if item in self.not_matched[d]:
            #         self.not_matched[d].remove(item)

            dst_ll[index] = item
            item.count -= 1

            if self.gt(index + 1, dst_ll):
                return True

            item.count += 1

            # self.not_matched = old_not_matched

        return False


def main():
    context = Context()
    import sys
    for line in sys.stdin:
        if context.handle_line(line.strip()):
            break

main()

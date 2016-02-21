TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

INDEXES = {1: [1],
           2: [0, 1, 2, 3],
           3: [0, 1, 3, 2, 4, 6, 5, 7, 8],
           4: [0, 1, 4, 2, 5, 8, 3, 6, 9, 12, 7, 10, 13, 11, 14, 15],
           5: [0, 1, 5, 2, 6, 10, 3, 7, 11, 15, 4, 8, 12, 16, 20, 9, 13, 17, 21, 14, 18, 22, 19, 23, 24]}


class Item():
    def __init__(self, rect):
        self.rect = rect
        self.is_used = False

    def __str__(self):
        return str(self.rect) + '-' + str(self.is_used)


class Context():
    def __init__(self):
        self.index = 0
        self.n = 0
        self.n2 = 0
        self.states = {}
        self.remain_count = None
        self.items = []
        self.indexes = None

        self.is_possible = False

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
            self.states = {LEFT: {}, RIGHT: {}, TOP: {}, BOTTOM: {}}
            self.remain_count = self.n2
            self.items = []
            self.indexes = INDEXES[self.n]
        else:
            parts = line.split()
            item = Item(map(int, parts))
            self.__add_item(item)
            self.remain_count -= 1
            if self.remain_count == 0:
                res = True
                if self.n > 1:
                    if self.n == 2 or not self.__is_impossible():
                        res = self.gt([None] * self.n2, 0)
                    else:
                        res = False
                print 'Game %d: %s' % (self.index, 'Possible' if res else 'Impossible')

    def __add_item(self, item):
        self.items.append(item)
        for d in [TOP, RIGHT, BOTTOM, LEFT]:
            if item.rect[d] not in self.states[d]:
                self.states[d][item.rect[d]] = [item]
            else:
                self.states[d][item.rect[d]].append(item)

    def __direction_exist(self, item, src_d, dst_d):
        if item.rect[src_d] in self.states[dst_d]:
            l = len(self.states[dst_d][item.rect[src_d]])
            return l > 1 or self.states[dst_d][item.rect[src_d]][0] != item
        return False

    def __is_impossible(self):
        for item in self.items:
            has_left = self.__direction_exist(item, LEFT, RIGHT)
            has_right = self.__direction_exist(item, RIGHT, LEFT)
            has_top = self.__direction_exist(item, TOP, BOTTOM)
            has_bottom = self.__direction_exist(item, BOTTOM, TOP)

            if (has_left and has_top) \
                    or (has_left and has_top and has_right) \
                    or (has_top and has_left and has_bottom) \
                    or (has_left and has_top and has_right and has_bottom) \
                    or (has_right and has_bottom) \
                    or (has_left and has_bottom and has_right) \
                    or (has_top and has_right and has_bottom):
                continue
            else:
                return True
        return False

    def __find_current_ones_by_prefix(self, dst_ll, index):
        if index == 0:
            return self.items[:]
        match_items = []
        # Top is exist.
        top = index - self.n
        if top >= 0:
            item = dst_ll[top]
            state = self.states[TOP]
            if not item.rect[BOTTOM] in state:
                return []
            match_items = filter(lambda x: not x.is_used, state[item.rect[BOTTOM]])
        # Left is exist.
        if (index % self.n) != 0:
            item = dst_ll[index - 1]
            state = self.states[LEFT]
            if not item.rect[RIGHT] in state:
                return []
            tmp_items = filter(lambda x: not x.is_used, state[item.rect[RIGHT]])
            if not match_items:
                return tmp_items
            match_items = filter(lambda x: not x.is_used and x in match_items, tmp_items)
        return match_items

    def __is_match_suffix(self, item, index):
        if self.n2 == index + 1:
            return True
        # Right is exist.
        right_items = None
        if (index + 1) % self.n != 0:
            state = self.states[LEFT]
            if not item.rect[RIGHT] in state \
                    or not filter(lambda x: not x.is_used, state[item.rect[RIGHT]]):
                return False

        # Bottom is exist.
        if index + self.n < self.n2:
            state = self.states[TOP]
            if not item.rect[BOTTOM] in state \
                    or not filter(lambda x: not x.is_used and (not right_items or x in right_items),
                                  state[item.rect[BOTTOM]]):
                return False
        return True

    def gt(self, dst_ll, p_index):
        # print map(str, dst_ll), p_index

        if p_index >= self.n2:
            return True

        index = self.indexes[p_index]

        items = self.__find_current_ones_by_prefix(dst_ll, index)
        for item in items:
            if not self.__is_match_suffix(item, index):
                continue

            item.is_used = True
            dst_ll[index] = item

            res = self.gt(dst_ll, p_index + 1)
            if res:
                return True

            item.is_used = False
            dst_ll[index] = None

        return False


def main():
    context = Context()
    import sys
    # for line in sys.stdin:
    for line in iter(open('p1008.in').readline, ''):
        if context.handle_line(line.strip()):
            break

if __name__ == '__main__':
    import utils
    tr = utils.TimeRecorder()

    main()

    # 0.3172s
    tr.record()

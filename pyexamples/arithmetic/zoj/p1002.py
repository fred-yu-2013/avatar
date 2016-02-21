# Fire Net
import sys


class Computer:
    def __init__(self, n, blocks):
        self.n = n
        self.blocks = blocks
        last_pos = len(blocks) - 1
        for _ in range(len(blocks)):
            if blocks[last_pos] == '.':
                break
            else:
                last_pos -= 1
        self.last_pos = last_pos

    def do(self):
        if self.last_pos < 0:
            print '0'
        else:
            max = 0
            for count in self._make_counts(self.n, self.blocks, 0):
                max = count if count > max else max
            print max

    def _make_counts(self, n, blocks, start):
        if start >= len(blocks):
            yield 0
        else:
            if blocks[start] == 'X':
                for result in self._make_counts(n, blocks, start + 1):
                    yield result
            else:
                for result in self._make_counts(n, blocks, start + 1):
                    yield result
                if self._can_set_gun(n, blocks, start):
                    blocks[start] = 'G'
                    for result in self._make_counts(n, blocks, start + 1):
                        yield result + 1
                    blocks[start] = '.'

    def _can_set_gun(self, n, blocks, position):
        row = position / n
        col = position % n
        for r in reversed(range(row)):
            index = r * n + col
            if blocks[index] == 'X':
                break
            elif blocks[index] == 'G':
                return False
        for c in reversed(range(col)):
            index = row * n + c
            if blocks[index] == 'X':
                break
            elif blocks[index] == 'G':
                return False
        return True

# main
n = 0
blocks = ''
count = n
for line in sys.stdin:
    if count == 0:
        n = int(line)
        if n == 0:
            break
        blocks = ''
        count = n
    else:
        blocks += line.strip()
        count -= 1
        if not count:
            computer = Computer(n, list(blocks))
            computer.do()
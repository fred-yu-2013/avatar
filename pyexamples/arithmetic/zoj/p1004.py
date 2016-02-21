import sys


class Computer:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def do(self):
        if len(self.src) != len(self.dst):
            print '['
            print ']'
        else:
            print '['
            result = []
            for operation in self._make_operations(self.src, self.dst, []):
                if operation:
                    result.append(' '.join(operation))
            result = sorted(result)
            for item in result:
                print item + ' '
            print ']'

    def _make_operations(self, src, dst, stack):
        if not dst:
            if src or stack:
                yield None
            else:
                yield []
        else:
            ch = dst[0]
            if src:
                index = src.find(ch)
                if index == -1:
                    yield None
                while True:
                    old_stack = list(stack)
                    result = []
                    for i in range(index + 1):
                        if i != index:
                            stack.append(src[i])
                        result.append('i')
                    result.append('o')
                    for operation in self._make_operations(src[index + 1:], dst[1:], stack):
                        if operation is None:
                            yield None
                        else:
                            yield result + operation
                    stack = old_stack
                    index = src.find(ch, index + 1)
                    if index == -1:
                        break
            if stack:
                old_stack = list(stack)
                stack_ch = stack.pop()
                if ch == stack_ch:
                    result = ['o']
                    for operation in self._make_operations(src, dst[1:], stack):
                        if operation is None:
                            yield None
                        else:
                            yield result + operation
                else:
                    yield None
                stack = old_stack

# main
src = None
dst = None
count = 0
for line in sys.stdin:
    if count == 0:
        src = line.strip()
        count += 1
    elif count == 1:
        dst = line.strip()
        # print src, dst
        computer = Computer(src, dst)
        computer.do()
        count = 0

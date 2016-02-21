__author__ = 'Fred'
"""
{4,2,5,9,17,19}, 127 => 42 + 59 + 17 + 19 = 127
"""
import copy


class Context:
    def __init__(self, numbers, target):
        self.numbers = numbers
        self.target = target

    def generate(self):
        if not self.numbers or len(self.numbers) < 1:
            raise 'Cannot generate'
        for result in self._generate2(self.numbers):
            if result and len(result) > 0 and sum(result) == self.target:
                print '%s = %s' % (' + '.join(str(x) for x in result), str(self.target))

    def _generate2(self, numbers):
        if len(numbers) <= 1:
            yield numbers
        else:
            for i in range(1, len(numbers)):
                left = numbers[:i]
                right = numbers[i:]
                for item in self._generate2(right):
                    yield [self._merge(left)] + item

    def _merge(self, numbers):
        if not numbers or len(numbers) == 0:
            raise 'Failed merge numbers.'
        if len(numbers) == 1:
            return numbers[0]
        result = numbers[-1]
        for i in reversed(range(0, len(numbers) - 1)):
            result = int(str(numbers[i]) + str(result))
        return result


def main():
    numbers = [4, 2, 5, 9, 17, 19]
    target = 137
    # numbers = [2, 4]
    # target = 24
    context = Context(numbers, target)
    context.generate()

main()

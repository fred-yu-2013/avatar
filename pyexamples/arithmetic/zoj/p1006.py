def ch2int(ch):
    if ch == '_':
        return 0
    elif ch == '.':
        return 27
    return ord(ch) - ord('a') + 1


def int2ch(value):
    if value == 0:
        return '_'
    elif value == 27:
        return '.'
    return chr(value + ord('a') - 1)


def c2p(cl, pl, k):
    n = len(cl)
    for i in range(n):
        pl[k * i % n] = (cl[i] + i) % 28


def untwist(src, k):
    cl = map(ch2int, src)
    pl = [-1] * len(cl)
    c2p(cl, pl, k)
    return ''.join(map(int2ch, pl))


def main():
    import sys
    for line in sys.stdin:
        if line.strip() == '0':
            return
        parts = line.strip().split()
        print untwist(parts[1], int(parts[0]))

main()

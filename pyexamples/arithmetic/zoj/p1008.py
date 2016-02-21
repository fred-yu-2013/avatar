# -*- coding: utf-8 -*-

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


def is_match_around(dst_ll, dst_context, item, p):
    n = dst_context['n']
    index = p[0] * n + p[1]
    top, bottom, left, right = index - n, index + n, index - 1, index + 1
    if 0 <= top < n and dst_ll[top] and not dst_ll[top][BOTTOM] != item[TOP]:
        return False
    if 0 <= bottom < n and dst_ll[bottom] and not dst_ll[bottom][TOP] != item[BOTTOM]:
        return False
    if 0 <= left < n and dst_ll[left] and not dst_ll[left][RIGHT] != item[LEFT]:
        return False
    if 0 <= right < n and dst_ll[right] and not dst_ll[right][LEFT] != item[RIGHT]:
        return False
    return True


def get_possible_positions(dst_ll, dst_context, item):
    res = []
    for pos in dst_context['poses']:
        # if dst_context['rect'][BOTTOM] - dst_context['rect'][TOP] + 1 == dst_context['src_n']
        index = pos[0] * dst_context['n'] + pos[1]
        # Try top.
        p = (pos[0], pos[1] - 1)
        if (not p in res) and (not p in dst_context['poses']) \
                and (item[BOTTOM] == dst_ll[index][TOP]) \
                and (dst_context['rect'][BOTTOM] - p[1] + 1 <= dst_context['src_n']) \
                and is_match_around(dst_ll, dst_context, item, p):
            direct = TOP if dst_context['rect'][TOP] == pos[1] else None
            res.append((p, direct))

        # Try bottom.
        p = (pos[0], pos[1] + 1)
        if (not p in res) and (not p in dst_context['poses']) \
                and (item[TOP] == dst_ll[index][BOTTOM]) \
                and (p[1] - dst_context['rect'][TOP] + 1 <= dst_context['src_n']) \
                and is_match_around(dst_ll, dst_context, item, p):
            direct = BOTTOM if dst_context['rect'][BOTTOM] == pos[1] else None
            res.append((p, direct))

        # Try left.
        p = (pos[0] - 1, pos[1])
        if (not p in res) and (not p in dst_context['poses']) \
                and (item[RIGHT] == dst_ll[index][LEFT]) \
                and (dst_context['rect'][RIGHT] - p[0] + 1 <= dst_context['src_n']) \
                and is_match_around(dst_ll, dst_context, item, p):
            direct = LEFT if dst_context['rect'][LEFT] == pos[0] else None
            res.append((p, direct))

        # Try right.
        p = (pos[0] + 1, pos[1])
        if (not p in res) and (not p in dst_context['poses']) \
                and (item[LEFT] == dst_ll[index][RIGHT]) \
                and (p[0] - dst_context['rect'][LEFT] + 1 <= dst_context['src_n']) \
                and is_match_around(dst_ll, dst_context, item, p):
            direct = RIGHT if dst_context['rect'][RIGHT] == pos[0] else None
            res.append((p, direct))
    return res


def put_item_in_position(dst_ll, dst_context, item, pos, direct):
    # just put the item.
    # print dst_ll, dst_context, item, pos, direct
    dst_context['poses'].append(pos)
    # print pos, item
    dst_ll[pos[0] * dst_context['n'] + pos[1]] = item
    if direct == TOP:
        dst_context['rect'][TOP] -= 1
        # dst_context['is_fix_height'] =
    elif direct == BOTTOM:
        dst_context['rect'][BOTTOM] += 1
    elif direct == LEFT:
        dst_context['rect'][LEFT] -= 1
    elif direct == RIGHT:
        dst_context['rect'][RIGHT] += 1


# def is_fix_square(dst_ll, dst_context):
#     r = dst_context['rect']
#     src_n = dst_context['res_n']
#     return r[RIGHT] - r[LEFT] + 1 == src_n and r[BOTTOM] - r[TOP] + 1 == src_n


def gt(dst_ll, dst_context, remains):
    """
    :param dst_context: dst square context.
        'poses': all item positions.
        'rect': exactly contains the items.
        'src_n':
        'src_n2':
        'n':
    """
    # print dst_ll, dst_context, remains
    if dst_context['src_n'] == 1:
        return True
    if not remains:
        return True
    if not 'poses' in dst_context:
        item = remains[0]
        dst_context['poses'] = []
        i = dst_context['src_n'] - 1
        dst_context['rect'] = [i, i, i, i]
        put_item_in_position(dst_ll, dst_context, item, (i, i), None)
        remains.remove(item)
    for item in remains:
        positions = get_possible_positions(dst_ll, dst_context, item)
        # print positions
        for pos, direct in positions:
            # import copy
            # tmp_dst_ll = copy.deepcopy(dst_ll)
            # tmp_dst_context = copy.deepcopy(dst_context)
            # tmp_remains = remains[:]
            # tmp_remains.remove(item)
            # put_item_in_position(tmp_dst_ll, tmp_dst_context, item, pos, direct)
            # if gt(tmp_dst_ll, tmp_dst_context, tmp_remains):
            #     return True

            # 0.026
            old_dst_ll = dst_ll[:]
            old_rect = dst_context['rect'][:]
            old_poses = dst_context['poses'][:]
            old_remains = remains[:]
            remains.remove(item)
            put_item_in_position(dst_ll, dst_context, item, pos, direct)
            if gt(dst_ll, dst_context, remains):
                return True
            dst_context['rect'] = old_rect
            dst_context['poses'] = old_poses
            dst_ll = old_dst_ll
            remains = old_remains
    return False

# dst_ll = [[j for i in range(3)] for j in range(3)]
# print gt(dst_ll, {'src_n': 2, 'src_n2': 4, 'n': 3}, [[5, 9, 1, 4], [4, 4, 5, 6], [6, 8, 5, 4], [0, 4, 4, 3]])


def handle_line(context, line):
    """
    :param context:
        n:
        items:
    -> is_quit.
    """
    if not 'index' in context:
        context['index'] = 1
    if not 'remain_count' in context or context['remain_count'] == 0:
        context['n'] = int(line)
        if context['n'] == 0:
            return True
        if 'remain_count' in context and context['remain_count'] == 0:
            print ''
        context['remain_count'] = context['n'] * context['n']
        context['items'] = []
    else:
        parts = line.split()
        context['items'].append(map(int, parts))
        context['remain_count'] -= 1
        if context['remain_count'] == 0:
            dst_n = context['n'] * 2 - 1
            # dst_ll = [[j for i in range(dst_n)] for j in range(dst_n)]
            dst_ll = [None] * dst_n * dst_n
            dst_context = {'src_n': context['n'], 'src_n2': context['n'] * context['n'], 'n': dst_n}
            res = gt(dst_ll, dst_context, context['items'])
            print 'Game %d: %s' % (context['index'], 'Possible' if res else 'Impossible')
            context['index'] += 1


def main():
    context = {}
    import sys
    # for line in sys.stdin:
    for line in iter(open('p1008.in').readline, ''):
        if handle_line(context, line.strip()):
            break

if __name__ == '__main__':
    import utils
    tr = utils.TimeRecorder()
    for i in range(1):
        main()
    # 3.82s
    tr.record()

    # main()

# -*- coding: utf-8 -*-


# def get_blocks(values):
#     mi, ma = 0, 0
#     result = []
#     gen_exe = []
#     for v in sorted(values):
#         if not gen_exe:
#             mi = ma = v
#             gen_exe.append(v)
#         else:
#             if abs(v - mi) < 7 and abs(v - ma) < 7:
#                 gen_exe.append(v)
#                 if v < mi:
#                     mi = v
#                 elif v > ma:
#                     ma = v
#             else:
#                 if len(gen_exe) > 1:
#                     result.append(gen_exe)
#                 mi = ma = v
#                 gen_exe = [v]
#     return result
#
# a = [87, 84, 86, 89, 90, 2014, 1000, 1002, 997, 999]
# print get_blocks(a)
#
#
# def get_first_item(value):
#     if isinstance(value, list):
#         return get_first_item(value[0])
#     return value
#
# l1 = [[[[['A'], ['B']], ['C']], 'D'], 'E']
# print get_first_item(l1)
# l2 = ['F', [[[['A'], ['B']], ['C']], 'D'], 'E']
# print get_first_item(l2)


def tOut(_tInput, _order=[]):
    _tOutput = [0, 1, 2, 3, 4, 5]
    _tReturn = []
    for x in _order:
        _tReturn.append(_tOutput[x])
    return (_tReturn)

tOrderReq = [1, 4, 5, 2]

tReturnData = tOut(None, (tOrderReq))
print tReturnData

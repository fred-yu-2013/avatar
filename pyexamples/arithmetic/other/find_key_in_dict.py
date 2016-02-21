# -*- coding: utf-8 -*-


def find_key_in_dict(d, t):
    """ d is dict for searching, t is target list.
    -> return matching key list.
    """
    b_str = reduce(lambda x, y: str(x) + str(y), t)
    return map(lambda x: x[0], filter(lambda i: b_str in reduce(lambda x, y: str(x) + str(y), i[1]), d.items()))

a = {'DOC3187': [1, 2, 3, 6, 7],
     'DOC4552': [5, 2, 3, 6],
     'DOC4974': [1, 2, 3, 6],
     'DOC8365': [1, 2, 3, 5, 6, 7],
     'DOC3738': [1, 4, 2, 3, 6],
     'DOC5311': [1, 5, 2, 3, 6, 7],
     }

t = [5,2,3]

print find_key_in_dict(a, t)

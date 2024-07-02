# test_pdb.py
def transform_list(x):
    x.append(1)
    x.extend([2, 3])
    return x


def test_list():
    a = []
    a = transform_list(a)
    a = a + [4]
    assert a == [1, 2, 3, 4]
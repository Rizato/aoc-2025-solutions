from eleven.solution import NetworkParser


def test_part_one_example():
    parser = NetworkParser()
    example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    network = parser.parse(example)

    assert network.find_paths() == 5


# def test_part_two_example():
#     parser = NetworkParser()
#     example = """aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out"""
#     network = parser.parse(example)
#
#     assert network.find_num_paths() == 5

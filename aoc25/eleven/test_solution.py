from aoc25.eleven.solution import NetworkParser


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

    assert network.find_paths("you", "out") == 5


def test_part_two_example():
    parser = NetworkParser()
    example = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
    network = parser.parse(example)

    assert network.find_dac_fft_paths("svr", "out", ["fft", "dac"]) == 2

if __name__ == "__main__":
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from theory.scales import HeptatonicScale

    scale = HeptatonicScale("C")
    print(scale)

    scale = HeptatonicScale("G")
    print(scale)

    scale = HeptatonicScale("C", "minor")
    print(scale)

    scale = HeptatonicScale("Cb")
    print(scale)

    scale = HeptatonicScale("Db", "dorian")
    print(scale)

    scale = HeptatonicScale("C#", "lydian")
    print(scale)

    for mode in HeptatonicScale.INTERVALS.keys():
        scale = HeptatonicScale("G", mode)
        print(scale)

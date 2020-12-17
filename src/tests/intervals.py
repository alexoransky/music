if __name__ == "__main__":
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from theory.intervals import DiatonicInterval

    for name in DiatonicInterval.SEMITONE_CNT.keys():
        i = DiatonicInterval(name)
        print(f"{i.full_name()}: semitones: {i.semitone_cnt} pitch ratio: {i.pitch_ratio}")

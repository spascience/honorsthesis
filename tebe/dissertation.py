"""
dissertation.py

An attempt at implementing the generative model described
in pages 337-365 of Prof. Mukherji's dissertation (2014).

"""

class Stufe:
    # Circle of Fifths in sharps, octave equivalence
    FIFTHS_NAMES = ['C','G','D','A','E','B',
                    'F#','C#','G#','D#','A#','E#']

    def __init__(self, cf=0, ct=0):
        # default ctor
        # circle of fifths value
        self.cf = cf
        # circle of thirds value
        self.ct = ct

        self.name = self.get_name()

    def get_name(self):
        # should work for negative cf too
        return self.FIFTHS_NAMES[self.cf % 12]

    def __str__(self):
        return f"{self.name}: c5 = {self.cf}, c3 = {self.ct}"


class Model:
    def __init__(self, western=True):
        # options for Western Tonality and Rock merge parameters
        self.merge_positive = western

        self.stufen = { Stufe(i, i) for i in range(-12,13) }

        # fixme: test
        print(self.stufen)

    def agree(self, s1, s2):
        """
        "checks" syntactic (cf, ct) features of s1 and s2. Returns
        True if merge in this direction is legal.

        :param s1: Stufe
        :param s2: Stufe
        :return: boolean
        """

        if self.merge_positive:
            # TODO: implment
            return False

        raise NotImplementedError
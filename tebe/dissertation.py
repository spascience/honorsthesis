"""
dissertation.py

An attempt at implementing the generative model described
in pages 337-365 of Prof. Mukherji's dissertation (2014).

"""

import numpy as np # for random action

class Stufe:
    # Circle of Fifths in sharps, octave equivalence
    FIFTHS_NAMES = ['C','G','D','A','E','B',
                    'F#','C#','G#','D#','A#','F']
    # TODO: Circle of Thirds relationships

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

class SyntacticObject:
    def __init__(self, m1, m2):
        """
        represents the output of Merge.

        :param m1: a Stufe or SyntacticObject
        :param m2: a Stufe or SyntacticObject
        """

        self.items = (m1, m2)

        # latter object projects syntactic features
        self.cf = m2.cf
        self.ct = m2.ct

    def __str__(self):
        # recursively access contained stufen
        return f"[{str(self.items[0])}, {str(self.items[1])}]"


class Model:
    def __init__(self, western=True):
        # options for Western Tonality and Rock merge parameters
        self.merge_negative = western

        self.stufen = { Stufe(i, i) for i in range(-12,13) }

        # fixme: test
        print("Stufen\n======")
        print(self.stufen)

    def agree(self, s1, s2):
        """
        "checks" syntactic (cf, ct) features of s1 and s2. Returns
        True if merge in this direction is legal.

        :param s1: Stufe
        :param s2: Stufe
        :return: boolean
        """

        if self.merge_negative:
            # western tonal
            return (s2.cf + 1) == s1.cf
            # TODO: thirds relationship
        else:
            # rock
            return (s1.cf + 1) == s2.cf
            # TODO: thirds relationship

    def merge(self, s1, s2):
        """
        R: agree(s1, s2)

        :param s1: Stufe or SyntacticObject
        :param s2: Stufe or SyntacticObject
        :return: SyntacticObject
        """
        return SyntacticObject(s1, s2)

    def filter(self, workspace):
        """
        later: cycle-based derivation?
        Checks if current derivation contains the Ursatz
        as its deepest structure.
        (yes, this is a scaringly encompassing filter)


        :param workspace: SyntacticObject
        :return: boolean
        """

        # should work for any key
        tonic_cf = workspace.cf
        tonic_ct = workspace.ct

        if self.merge_negative:
            if (workspace.items[0].cf == tonic_cf and  # tonic prolongation
                workspace.items[1].items[0] == tonic_cf + 1):
                # Tonic Prolongation, Dominant Prolongation, Tonic Completion
                return True
        else:
            # TODO: Rock music
            return False

    def generate(self, n=1, select=None):
        """
        Stochastically generates an ordering of stufen using Merge.
        (Regarding C & S 2011: Assumes Select is applied once
        at the beginning of the derivation)

        :param n: number of syntactic objects to generate
        :select: ordered collection of Stufe; all that you want available
                 for the generation. If "None" then uses all available
        :return: SyntacticObject
        """

        # begin
        if not select:
            select = self.stufen

        derivation = None
        while not self.filter(derivation)
        #TODO: BRUH. think first, then implement

        # pick two random stufen and see if they agree
        s1_i, s2_i = np.random.randint(0, len(select), size=2)
        s1, s2 = select[s1], select[s2]

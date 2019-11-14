"""
dissertation.py

An attempt at implementing the generative model described
in pages 337-365 of Prof. Mukherji's dissertation (2014).
Takes mathematical inspiration from Collins & Stabler (2011).

"""

import random

class Stufe:
    # Circle of Fifths in sharps, octave equivalence
    FIFTHS_NAMES = ['C','G','D','A','E','B',
                    'F#','C#','G#','D#','A#','F']
    # TODO: (Diatonic) Circle of Thirds relationships

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

    def __repr__(self):
        return f"[{str(self.items[0])}, {str(self.items[1])}]"


class Model:
    def __init__(self, western=True):
        # options for Western Tonality and Rock merge parameters
        self.merge_negative = western

        self.stufen = { Stufe(i, i) for i in range(-12,13) }

        # fixme: test
        print("Stufen\n======")
        for s in self.stufen:
            print(s)

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

    def filter(self, root):
        """
        later: cycle-based derivation?
        Checks if current derivation contains the Ursatz
        as its deepest structure.
        (yes, this is a scaringly encompassing filter)


        :param root: SyntacticObject
        :return: boolean
        """

        # should work for any key
        tonic_cf = root.cf
        tonic_ct = root.ct

        if self.merge_negative:
            if (root.items[0].cf == tonic_cf and  # tonic prolongation
                root.items[1].items[0] == tonic_cf + 1):
                # Tonic Prolongation, Dominant Prolongation, Tonic Completion
                return True
        else:
            # TODO: Rock music
            return False

    def get_agreeable_features(self, stufe):
        """
        Determines stufen that would be legally Merge-able
        with stufe and returns their syntactic features.

        :param stufe: Stufe or SyntacticObject
        :return: ordered iterable of ints
        """

        if self.merge_negative:
            return [stufe.cf - 1]
        else:
            return [stufe.cf + 1]

        # TODO: thirds relationship

    def get_possible_merges(self, stufe, lexicon_by_feature):
        """
        Returns an ordered iterable of all possible Merges
        with stufe within the provided workspace
        :param stufe: SyntacticObject
        :param lexicon_by_feature: map ints to Stufen
        :return: tuple of tuples of SyntacticObjects
        """

        # TODO: thirds relationship

        # merge-TO-ables
        mergees = list()
        mergee_features = self.get_agreeable_features(stufe)
        for feature in mergee_features:
            if feature in lexicon_by_feature:
                mergees.append(lexicon_by_feature[feature])

        # merge-FROM-ables
        mergers = list()
        # TODO: make more general
        merger_features = [stufe.cf + 1]

        # BLOCK repeated merges
        if type(stufe) == SyntacticObject and type(stufe.items[0]) == Stufe:
            # only one stufe between merger and mergee, remove repeated stufe
            for i in range(len(merger_features)):
                if merger_features[i] == stufe.items[0].cf:
                    merger_features.pop(i)

        for feature in merger_features:
            if feature in lexicon_by_feature:
                mergers.append(lexicon_by_feature[feature])

        # TODO: more elegant way to do this?
        if len(mergee_features) + len(merger_features) == 0:
            return ()

        # package possible merges
        merges_TO = tuple( (stufe, mergee) for mergee in mergees )
        merges_FROM = tuple( (merger, stufe) for merger in mergers )

        return merges_TO + merges_FROM

    def generate_v3(self, n=10, lexicon=None):
        """
        Stochastically generates an ordering of stufen using Merge.
        Uses a stochastic, Agree-driven Select style. That is,
        Agree is applied first to an SO in the Workspace and
        a stufe with correct syntactic features is Selected.
        Filter/Transfer is applied after every occurence of Merge.

        :param n: number of syntactic objects to generate
        :lexicon: ordered collection of Stufe; all that you want available
                  for the generation. If "None" then uses all available
        :return: SyntacticObject
        """

        # begin
        if not lexicon:
            lexicon = self.stufen

        lexicon_by_cf = { s.cf: s for s in lexicon }
        # TODO: add thirds relationship

        # randomly add two stufen to the workspace (initial Select)
        workspace = random.sample(lexicon, 2)

        num_generated = 0
        completed = list()
        while num_generated < n:
            current_i = random.choice(range(len(workspace)))
            current = workspace[current_i]

            merges = self.get_possible_merges(current, lexicon_by_cf)

            # crash clause
            if len(merges) == 0:
                print("Derivation Crashed")
                print("current stage: ")
                print(workspace)
                return completed

            choice = random.choice(merges)

            m = self.merge(choice[0], choice[1])
            workspace[current_i] = m

            # check for completed derivations
            if self.filter(m):
                # "Transfer"
                completed.append(m)
                num_generated += 1

        return completed

    def spell_out(self, generated):
        """
        Prints the generated compositions in a pretty way.

        :param generated: list of SyntacticObjects
        :return: nothing
        """

        print("Compositions\n============\n")

        for comp in generated:
            print(comp)
            print('\n')
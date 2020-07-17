"""
model.py

Model of harmonic composition in Western Tonal Music, based
on formalization of Minimalist grammar by Chris Collins and Ed Stabler:

Collins, C., & Stabler, E. (2016). A formalization of minimalist syntax.
    Syntax, 19(1), 43-78.

This model generates chord sequences via the assumption that the computational
system for Human Language and the computational system for Human Music are
actually the same. For more information, see:

Katz, J., & Pesetsky, D. (2011). The identity thesis for language and music.
    Manuscript, January.

Mukherji, S. (2014). Generative Musical Grammar-A Minimalist Approach.
    PhD Diss. Princeton University.



Sean P. Anderson, seanpaul@umich.edu
Generative Linguistics And Music grant
Professors S. Mukherji, S. Epstein, and J. Zhang, University of Michigan
October 6, 2019

Done in work for undergraduate Honors Thesis
"""

import random


class Stufe:
    """Musical equivalent of "Lexical Item"
    Chromatic edition"""
    # Circle of Fifths in sharps, octave equivalence
    FIFTHS_NAMES = ['C', 'G', 'D', 'A', 'E', 'B',
                    'F#', 'C#', 'G#', 'D#', 'A#', 'F']
    FIFTHS_NAMES_MINOR = ['a', 'e', 'b', 'f#', 'c#', 'g#',
                          'd#', 'a#', 'f', 'c', 'g', 'd']

    def __init__(self, c5=0, c3=0, major=True):
        # default ctor
        self.is_major = major
        # circle of fifths value
        self.c5 = c5
        # circle of thirds value
        self.c3 = c3

        self.name = self.get_name()

    def get_name(self):
        # should work for negative cf too
        if self.is_major:
            return self.FIFTHS_NAMES[self.c5 % 12]
        else:
            return self.FIFTHS_NAMES_MINOR[self.c5 % 12]

    def __str__(self):
        return f"{self.name}: c5 = {self.c5}"


class SyntacticObject:
    def __init__(self, m1, m2):
        """
        Represents the output of Merge.

        :param m1: a Stufe or SyntacticObject
        :param m2: a Stufe or SyntacticObject
        """

        self.items = (m1, m2)

        # Latter object projects syntactic features
        self.c5 = m2.c5
        self.c3 = m2.c3

    def __str__(self):
        # recursively access contained stufen
        return f"[{str(self.items[0])}, {str(self.items[1])}]"

"""
class LexicalArray:
    # make Lexical Array explicit
    def __init__(self, items):
        
        default ctor
        :param items: collection of Stufe
        
        self.items = set(items)


class Workspace:
    # make Workspace explicit
    def __init__(self, items):
        
        default ctor
        :param items: collection of syntactic objects
        
        self.items = set(items)
"""


class Composer:
    """
    Model A:
    Stochastic Free-Merge composer dispensing with Agree, indexing,
    and internal Merge (transformations). SpellOuts SyntacticObjects
    that pass Ursatz Filter. For simplicity, derivations are completed
    in C Major/A minor (WLOG to other keys).
    """
    class Stage:
        # For Select to operate on, to be consistent with C&S 2011
        def __init__(self, la=set(), workspace=set()):
            """
            default ctor
            :param la: set of Stufe objs
            :param w: set of SyntacticObject and Stufe objs
            """
            # Lexical Array
            self.la = la
            # Workspace
            self.workspace = workspace

        def __str__(self):
            return f"<{str(self.la)}, {str(self.workspace)}>"

    def __init__(self):
        self.stage_i = 0

    def filter(self, so) -> bool:
        """
        Returns true if so is "fully interpretable." In this case,
        whether it exhibits the Ursatz at the root.

        :param so: SyntacticObject
        :return: bool
        """

        is_tonic = (so.c5 == 0)
        has_dominant = False
        starts_with_tonic = False

        if isinstance(so.items[1], SyntacticObject):
            has_dominant = (so.items[1].items[0].c5 == 1)

        if is_tonic and has_dominant:
            starts_with_tonic = self._filter_helper(so.items[0])

        return is_tonic and has_dominant and starts_with_tonic

    def _filter_helper(self, so) -> bool:
        """
        recursively check for tonic Stufe in left branches

        :param so: SyntacticObject or Stufe
        :return: bool
        """
        if isinstance(so, Stufe):
            return so.c5 == 0
        else:
            return self._filter_helper(so.items[0])

    def select(self, item: Stufe, stage: Stage) -> Stage:
        """
        Select as defined in C&S. Moves an item from LA into
        Workspace.
        R: item in Stage.la

        :param item: Stufe
        :param stage: Stage
        :return: Stage
        """
        stage.la = stage.la - {item}
        # fixme: won't handle multiple copies of same stufe
        # shouldn't be a problem for tebe though
        stage.workspace.add(item)
        return stage

    def select_random(self, stage: Stage) -> Stage:
        """
        Moves a random Stufe from the LexicalArray to
        the Workspace.
        R: not Stage.la.empty()

        :param stage: Composer.Stage
        :return: Composer.Stage
        """
        # oof TODO: consider not using hash tables
        item = random.choice(tuple(stage.la))
        return self.select(item, stage)

    def merge(self, so1, so2, stage: Stage) -> SyntacticObject:
        """
        Performs external Merge on two SO's in stage.workspace
        as defined in C&S.
        REQUIRES: s01, s02 in stage.workspace
        MODIFIES: stage

        :param s01: Stufe or SyntacticObject
        :param s02: Stufe or SyntacticObject
        :param stage: Composer.Stage
        :return: SyntacticObject
        """
        stage.workspace = ((stage.workspace - {so1}) - {so2})
        new_so = SyntacticObject(so1, so2)
        stage.workspace.add(new_so)
        return new_so

    def merge_random(self, stage: Stage) -> Stage:
        """
        Performs Merge on two random SO's in stage.workspace.

        :param stage: Stage
        :return: stage
        """
        # oof TODO: consider not using hash tables
        so1, so2 = random.sample(tuple(stage.workspace), 2)
        return self.merge(so1, so2, stage)

    def derive(self, la):
        """
        Executes a derivation starting with LexicalArray la.
        Every SO generated that passes Filter will be spelled out.

        :param la: collection of Stufe objs
        :return: collection of derivations
        """

        if len(la) < 2:
            print("Error: You need more than 2 Stufen to compose")
            return list()

        # set up (select 2)
        derivations = list()
        current = Composer.Stage(la=set(la))
        current = self.select_random(current)
        current = self.select_random(current)
        self.stage_i = 2

        # derivation
        while len(current.la) > 0 or len(current.workspace) != 1:
            flip = random.choice([0,1])
            if flip and len(current.la) > 0:
                # Select
                current = self.select_random(current)
            elif not flip and len(current.workspace) != 1:
                # Merge
                new_so = self.merge_random(current)
                # Filter and spell out
                if self.filter(new_so):
                    # found a valid derivation!
                    derivations.append(new_so)

            self.stage_i += 1
            # FIXME: test
            print(f"Stage #{self.stage_i}:")
            print(current)
            print()

        # end of derivation
        if self.filter(list(current.workspace)[0]):  # awk
            print("Derivation finished")
        else:
            # derivation crashed
            print("Derivation crashed")

        return derivations


def main():
    # tebe testing
    # all stufen hypothesized to be in Bortniansky's Tebe Poem
    lexicon = [(0, True), (0, True), (-1, True),
               (2, True), (1, True), (4, True), (0, False),
               (6, True), (1, True), (0, True)]
    lexical_array = list()

    for c5, is_major in lexicon:
        lexical_array.append(Stufe(c5=c5, major=is_major))

    model = Composer()
    derivations = model.derive(lexical_array)

    print("All Derivations\n===============")
    print(derivations)

    return 0


if __name__ == "__main__":
    main()

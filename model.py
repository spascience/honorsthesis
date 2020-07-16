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


class Stufe:
    """Musical equivalent of "Lexical Item"
    Chromatic edition"""
    # Circle of Fifths in sharps, octave equivalence
    FIFTHS_NAMES = ['C', 'G', 'D', 'A', 'E', 'B',
                    'F#', 'C#', 'G#', 'D#', 'A#', 'F']

    def __init__(self, c5=0, c3=0):
        # default ctor
        # circle of fifths value
        self.c5 = c5
        # circle of thirds value
        self.c3 = c3

        self.name = self.get_name()

    def get_name(self):
        # should work for negative cf too
        return self.FIFTHS_NAMES[self.c5 % 12]

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
        """
        #default ctor
        #:param items: collection of Stufe
        """
        self.items = set(items)


class Workspace:
    # make Workspace explicit
    def __init__(self, items):
        """
        #default ctor
        #:param items: collection of syntactic objects
        """
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
        def __init__(self, la=set(), w=set()):
            """
            default ctor
            :param la: set of Stufe objs
            :param w: set of SyntacticObject and Stufe objs
            """
            # Lexical Array
            self.la = la
            # Workspace
            self.w = w

        def __str__(self):
            return f"<{str(self.la)}, {str(self.w)}>"

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
        if isinstance(so.items[1], SyntacticObject):
            has_dominant = (so.items[1].items[0].c5 == 1)

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

    def derive(self, la):
        """
        Executes a derivation starting with LexicalArray la.
        Every SO generated that passes Filter will be spelled out.

        :param la: collection of Stufe objs
        :return: collection of derivations
        """
        pass



"""
modelB.py

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

modelB derives with feature-driven Merge (Agree), closer to the
Mukherji (2014) model.

Sean P. Anderson, seanpaul@umich.edu
Generative Linguistics And Music grant
Professors S. Mukherji, S. Epstein, and J. Zhang, University of Michigan
July 26, 2020

Done in work for undergraduate Honors Thesis
"""

import random
import itertools

from model import Composer, Stufe, SyntacticObject


class ComposerB(Composer):
    # Mukherji (2014) model
    def agree(self, so1, so2) -> bool:
        """
        Stufen-based Agree. Returns whether so1 and
        so2 are Merge-able in the order specified.

        :param so1: Stufe or SyntacticObject
        :param so2: Stufe or SyntacticObject
        :return: bool
        """

        # Western Tonal music parameterization
        do_agree = (0 <= so1.c5 - so2.c5 <= 1) or (0 <= so1.c3 - so2.c5 <= 1)
        return do_agree

    def get_mergables(self, stage: Composer.Stage) -> (bool, list):
        """
        Checks if a merge is possible with items in stage.workspace.
        Returns false if no possible merges exist. Returns a list of
        SO pairs if true.

        :param stage: Composer.Stage
        :return: bool, list of tuples
        """

        success = False
        merges_possible = list()
        # order matters
        for so1, so2 in itertools.permutations(stage.workspace, r=2):
            if self.agree(so1, so2):
                # TODO: stop at first pair found?
                success = True
                merges_possible.append( (so1, so2) )

        return success, merges_possible

    def derive(self, la, verbose=True):
        """
        Executes a derivation starting with Lexical Array la.
        Flips a coin to decide whether to Select or to Merge.
        If Merging, merges agreeing SO's if possible, otherwise
        makes no operation. Every SO generated that passes Filter
        will be spelled out.

        :param la: collection of Stufe objs
        :param verbose: bool
        :return: collection of derivations, bool
        """

        if len(la) < 2:
            print("Error: You need more than 2 Stufen to compose")
            return list()

        # set up (select 2)
        derivations = list()
        current = Composer.Stage(la=set(la), workspace=set())
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
                merge_possible, mergeables = self.get_mergables(current)
                if merge_possible:
                    so1, so2 = random.choice(mergeables)
                    new_so = self.merge(so1, so2, current)
                    # Filter and spell out
                    if self.filter(new_so):
                        # found a valid derivation!
                        derivations.append(new_so)

            self.stage_i += 1
            if verbose:
                print(f"Stage #{self.stage_i}:")
                current.print()
                print()

        # end of derivation
        if self.filter(list(current.workspace)[0]):  # awk
            print("Derivation finished")
            return derivations, True
        else:
            # derivation crashed
            print("Derivation crashed")
            return derivations, False


def main():
    # tebe testing
    # all stufen hypothesized to be in Bortniansky's Tebe Poem
    lexicon = [(0, True, False), (0, True, False), (-1, True, False),
               (2, True, False), (1, True, False), (4, True, False), (0, False, False),
               (6, False, True), (1, True, False), (0, True, False)]
    lexical_array = list()

    for c5, is_major, is_dim in lexicon:
        lexical_array.append(Stufe(c5=c5, major=is_major, dim=is_dim))

    model = ComposerB()
    derivations, success = model.derive(lexical_array)

    print("All Derivations\n===============")
    print(derivations)
    if len(derivations) > 0:
        print(derivations[-1].spell_out())

    """
    print("\nSearch for tebe\n===============")
    model = Composer()
    completed, count, so_list = tebe_search(model)
    print("Search for tebe finished")
    print(f"Found surface: {completed}\nafter {count} attempts\n")
    print([str(so) for so in so_list])
    """

    return 0


if __name__ == "__main__":
    main()

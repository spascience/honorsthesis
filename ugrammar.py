"""
ugrammar.py

An implementation of Chris Collins and Ed Stabler's formalization of
Minimalist Syntax.

Collins, C., & Stabler, E. (2016). A formalization of minimalist syntax. Syntax, 19(1), 43-78.

©2019 Sean Anderson
seanpaul@umich.edu

Generative Linguistics And Music grant
Professors S. Mukherji, S. Epstein, and J. Zhang
University of Michigan
"""

class UGrammar:
    """
    Universal Grammar
    """
    def __init__(self, SemF, SynF, PhonF):
        """
        :param SemF: container of Semantic features #Fixme: represented as?
        :param SynF: container of Syntactic features
        :param PhonF: container of Phonetic features
        :return: UGrammar
        """

        self.SemF = SemF
        self.SynF = SynF
        self.PhonF = PhonF

# Note: Decided against using Inner Classes because of Python's inner Classes
#       don't have access to the outer class object, which would have been
#       ideal here.

# no custom class needed for Lexicon (as of now)

def SemFeature:
    # placeholder for Semantic feature.
    pass

def SynFeature
    # placeholder for Syntactic feature.
    pass

def PhonFeature
    # placeholder for Phonetic feature.
    pass

class LexicalItem:
    def __init__(self, sem, syn, phon):
        """
        R: sem, syn, and phon in UGrammar.SemF, UGramamr.SynF,
           and UGrammar.PhonF respectively

        To make working with <SEM, SYN, PHON> triples easier.
        For use in GLAM project, stufen (~chord~) names will be stored in
        the "sem" feature.
        """

        # todo: perform feature check?

        self.sem = sem
        self.syn = syn
        self.phon = phon
    
    def featurecheck(self, grammar):
        """
        :param grammar: UGrammar instance
        :return: True if features are legal within UGrammar

        E: Checks if features are valid within this UGrammar class.
        """

        return self.sem in grammar.SemF and self.syn in grammar.SynF and \
               self.phon in grammar.PhonF

class LexicalItemToken:
    def __init__(self, item, token):
        """
        :param item: LexicalItem
        :param token: int
        
        Requires: this item-token pair isn't already taken?
        """

        self.item = item
        self.token = token





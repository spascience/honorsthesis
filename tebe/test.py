"""
test.py

A simple test of the Tebe generative model.

11/13/2019 Sean Anderson
"""

from tebe import dissertation

def main():

    composer = dissertation.Model()

    compositions = composer.generate_v3(n=1)

    composer.spell_out(compositions)

    return 0


if __name__ == '__main__':
    main()

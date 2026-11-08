import numpy as np

from heuristiques_squelette import heuristique1, heuristique2X
from util_tp2 import (
    pbsac1, pbsac2, pbsac3, pbsac4, pbsac5,
    pbsac6, pbsac7, pbsac8, pbsac9,
)


def main():
    problems = [pbsac1, pbsac2, pbsac3, pbsac4, pbsac5,
                pbsac6, pbsac7, pbsac8, pbsac9]

    print(f"{'Problem':<10} {'H1':>8} {'H2,1':>8} {'H2,inf':>8} {'H2,2':>8}")
    for problem in problems:
        c, A, b = problem()
        _, f1 = heuristique1(c, A, b)
        _, f21 = heuristique2X(c, A, b, X=1)
        _, f2inf = heuristique2X(c, A, b, X=np.inf)
        _, f22 = heuristique2X(c, A, b, X=2)
        print(f"{problem.__name__:<10} {f1:>8} {f21:>8} {f2inf:>8} {f22:>8}")


if __name__ == "__main__":
    main()

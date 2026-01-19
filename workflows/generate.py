import sys

from wsp import WSP, ReadMe


def main(n: int):
    for wsp in WSP.list_random(n):
        wsp.build()
    WSP.aggregate()
    ReadMe().build()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python workflows/generate.py <n>")
        sys.exit(1)
    main(int(sys.argv[1]))

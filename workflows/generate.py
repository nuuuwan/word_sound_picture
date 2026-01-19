from wsp import WSP, ReadMe


def main():
    for wsp in WSP.list_random(5):
        wsp.build()
    WSP.aggregate()
    ReadMe().build()


if __name__ == "__main__":
    main()

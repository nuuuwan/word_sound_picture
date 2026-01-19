from wsp import WSP


def main():
    for wsp in WSP.list_random(5):
        wsp.build()


if __name__ == "__main__":
    main()

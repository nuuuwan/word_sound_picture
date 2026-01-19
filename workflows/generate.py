from wsp import WSP


def main():
    for wsp in WSP.list_random(5):
        wsp.build()
    WSP.aggregate()


if __name__ == "__main__":
    main()

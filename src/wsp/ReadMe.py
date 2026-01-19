from utils import File, Log

from wsp.WSP import WSP

log = Log("ReadMe")


class ReadMe:
    README_PATH = "README.md"

    def get_lines_for_header(self) -> list[str]:
        return [
            "# சொல்-ஒலி-படம்",
            "",
            "தமிழ் கற்க எளிதான வழி.",
            "",
        ]

    def get_lines_for_metadata(
        self, i_metadata: int, metadata: dict
    ) -> list[str]:
        lines = []
        ta_word = metadata["ta_word"]
        picture_path = metadata["picture_path"]

        lines += [
            f"## {i_metadata:02d}. {ta_word}",
            "",
            f"![{ta_word}]({picture_path})",
            "",
        ]
        return lines

    def get_lines_for_wsp(self) -> list[str]:
        metadata_list = WSP.load_metadata_list()
        lines = []
        for i_metadata, metadata in enumerate(metadata_list, start=1):
            lines += self.get_lines_for_metadata(i_metadata, metadata)
        return lines

    def get_lines(self) -> list[str]:

        return self.get_lines_for_header() + self.get_lines_for_wsp()

    def build(self):
        lines = self.get_lines()
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")

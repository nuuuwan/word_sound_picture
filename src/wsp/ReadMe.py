import os

from utils import File, JSONFile, Log

log = Log("ReadMe")


class ReadMe:
    README_PATH = "README.md"

    def load_metadata_list(self) -> list[dict]:
        metadata_list = []
        for cur_root, _, file_names in os.walk(os.path.join("data", "wsp")):
            for file_name in file_names:
                if file_name == "metadata.json":
                    file_path = os.path.join(cur_root, file_name)
                    metadata = JSONFile(file_path).read()
                    metadata_list.append(metadata)

        log.debug(f"Loaded metadata for {len(metadata_list)} WSPs.")
        return metadata_list

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
        metadata_list = self.load_metadata_list()
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

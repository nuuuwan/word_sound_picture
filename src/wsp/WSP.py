import asyncio
import base64
import os
import random
import tempfile
from functools import cached_property

from googletrans import Translator
from gtts import gTTS
from openai import OpenAI
from PIL import Image
from utils import File, JSONFile, Log

log = Log("WSP")


# Pricing: https://platform.openai.com/docs/pricing?utm_source=chatgpt.com
# Image API: https://platform.openai.com/docs/api-reference/images/create


class WSP:
    def __init__(self, en_word: str):
        self.en_word = en_word

    @classmethod
    def __list_all_en_words__(cls):
        en_words = File(
            os.path.join("data", "static", "first-100.txt")
        ).read_lines()
        stripped_words = [w.strip() for w in en_words]
        minus_short_words = [w for w in stripped_words if len(w) >= 3]
        return minus_short_words

    @classmethod
    def list_all(cls):
        en_words = cls.__list_all_en_words__()
        return [cls(en_word) for en_word in en_words]

    @classmethod
    def list_random(cls, n: int):
        en_words = cls.__list_all_en_words__()
        sampled_words = random.sample(en_words, n)
        return [cls(en_word) for en_word in sampled_words]

    @cached_property
    def dir_path(self):
        return os.path.join(
            "data", "wsp", self.en_word[0], self.en_word[:2], self.en_word
        )

    @cached_property
    def ta_word(self):
        # translate self.en_word into Tamil using googletrans
        translator = Translator()
        translation = asyncio.run(
            translator.translate(self.en_word, dest="ta")
        )
        return translation.text

    def build_sound(self) -> str:
        tts = gTTS(self.ta_word, lang="ta")
        sound_path = os.path.join(self.dir_path, "sound.mp3")
        tts.save(sound_path)
        log.debug(f"Wrote {File(sound_path)}")
        return sound_path

    def __generate_picture_prompt__(self) -> str:
        return f"""

            A warm, child-friendly illustration
            in the style of a Sri Lankan
            children's picture book.

            The image is a single page collage
            with multiple small sub-scenes
            arranged like frames or panels.

            Each sub-image clearly represents
            the meaning of the word
            "{self.en_word}"
            using different situations.

            Meaning must be conveyed only
            through characters, actions,
            and the environment.

            Use subtle Sri Lankan cues
            such as clothing, homes,
            nature, or daily life.

            All sub-scenes are simple,
            colourful, and emotionally clear,
            with soft lines and gentle faces.

            Scenes should vary slightly
            to show the word in use
            across contexts.

            No written text, letters,
            numbers, or symbols
            anywhere in the image.

            The overall composition
            should feel unified,
            warm, and playful.

        """

    def __generate_image_from_api__(self, prompt: str) -> bytes:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        result = client.images.generate(
            prompt=prompt,
            model="gpt-image-1.5",
            n=1,
            output_format="png",
            size="1024x1024",
        )
        image_base64 = result.data[0].b64_json
        return base64.b64decode(image_base64)

    def __save_and_resize_image__(self, image_bytes: bytes) -> str:
        temp_picture_path = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
        ).name
        with open(temp_picture_path, "wb") as f:
            f.write(image_bytes)

        picture_path = os.path.join(self.dir_path, "picture.png")
        with Image.open(temp_picture_path) as img:
            img = img.resize((320, 320))
            img.save(picture_path)
        log.debug(f"Wrote {File(picture_path)}")
        return picture_path

    def build_picture(self) -> str:
        prompt = self.__generate_picture_prompt__()
        image_bytes = self.__generate_image_from_api__(prompt)
        picture_path = self.__save_and_resize_image__(image_bytes)
        return picture_path

    def __build_hot__(self):
        dir_path = self.dir_path
        os.makedirs(dir_path, exist_ok=True)
        sound_path = self.build_sound()
        picture_path = self.build_picture()
        metadata = dict(
            en_word=self.en_word,
            ta_word=self.ta_word,
            sound_path=sound_path,
            picture_path=picture_path,
        )
        metadata_file = JSONFile(os.path.join(dir_path, "metadata.json"))
        metadata_file.write(metadata)
        log.info(f"Wrote {metadata_file}")

    def build(self):
        dir_path = self.dir_path
        metadata_file = JSONFile(os.path.join(dir_path, "metadata.json"))
        if metadata_file.exists:
            log.debug(
                f"WSP for '{self.en_word}' already exists. Skipping build."
            )
            return False

        self.__build_hot__()
        return True

    @classmethod
    def load_metadata_list(cls) -> list[dict]:
        metadata_list = []
        for cur_root, _, file_names in os.walk(os.path.join("data", "wsp")):
            for file_name in file_names:
                if file_name == "metadata.json":
                    file_path = os.path.join(cur_root, file_name)
                    metadata = JSONFile(file_path).read()
                    metadata_list.append(metadata)

        log.debug(f"Loaded metadata for {len(metadata_list)} WSPs.")
        return metadata_list

    @classmethod
    def aggregate(cls):
        metadata_list = cls.load_metadata_list()
        aggregate_file = JSONFile(
            os.path.join("data", "wsp", "aggregate.json")
        )
        aggregate_file.write(metadata_list)
        log.info(f"Wrote {aggregate_file}")

# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import urllib.request

from pathlib import Path
from ..paths import dir_project_root


dir_tmp = dir_project_root / "tmp"


def safe_write(path: Path, b: bytes):
    try:
        path.write_bytes(b)
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b)


@dataclasses.dataclass
class AudioFile:
    name: str

    @property
    def url(self) -> str:
        return f"https://github.com/MacHu-GWU/audinota-project/releases/download/artifacts/{self.name}"

    @property
    def path(self) -> Path:
        return dir_tmp / self.name

    def download(self):
        print(f"Downloading {self.url} to {self.path}")
        with urllib.request.urlopen(self.url) as f:
            data = f.read()
            safe_write(self.path, data)

    def read(self) -> bytes:
        try:
            return self.path.read_bytes()
        except FileNotFoundError:
            self.download()
            return self.path.read_bytes()


class AudioFileEnum:
    a01_ai_karen_hao_agi_openai_ai_10min = AudioFile(
        name="01-AI-Karen-Hao-AGI-OpenAI-AI-10min.mp3"
    )
    a02_stablecoin_15min = AudioFile(name="02-Stablecoin-15min.mp3")
    a03_luo_ji_si_wei_kai_hui_60min = AudioFile(
        name="03-Luo-Ji-Si-Wei-Kai-Hui-60min.mp3"
    )

    @classmethod
    def iter(cls) -> T.Iterator[AudioFile]:
        for k, v in cls.__dict__.items():
            if isinstance(v, AudioFile):
                yield v

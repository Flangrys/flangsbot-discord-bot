import pathlib
from dataclasses import dataclass


@dataclass
class Extension:
    name: str
    description: str

    module: str

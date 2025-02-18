from typing import Literal, Tuple

type ReleaseType = Literal["release", "candidate", "beta", "indev"]

type ClientVersion = Tuple[int, int, int, ReleaseType]

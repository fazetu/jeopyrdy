import os
from typing import Any, List, Optional

import numpy as np
import pyfiglet


def show(text: str, big: bool = True, wait: bool = True) -> Optional[str]:
    if big:
        text = pyfiglet.figlet_format(text)

    if wait:
        return input(text)
    else:
        print(text)


def clear():
    os.system("cls")


def pick1(x: List[Any]) -> Any:
    return np.random.choice(x, size=1).tolist()[0]


def is_int(x: str) -> bool:
    try:
        int(x)
        return True
    except Exception:
        return False


def file_ext(file: str) -> str:
    parts = file.split(".")
    return parts[len(parts) - 1]

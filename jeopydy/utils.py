from typing import Any, List
import os

import numpy as np
import pyfiglet


def show(text: str, **kwargs):
    print(pyfiglet.figlet_format(text, **kwargs))
    

def wait_show(text: str, **kwargs) -> str:
    return input(pyfiglet.figlet_format(text, **kwargs))


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
import json
import os
from typing import Optional

from src.env import ROOT_PATH


def instance_to_dict(obj: object):
    return obj.__dict__


def read_json(filepath) -> Optional[dict]:
    try:
        with open(os.path.normpath(os.path.join(ROOT_PATH, filepath))) as f:
            return json.load(f)
    except OSError:
        return None


def write_json(filepath, obj: dict) -> Optional[int]:
    try:
        with open(os.path.normpath(os.path.join(ROOT_PATH, filepath)), 'w') as f:
            json.dump(obj, f)
            return 1
    except OSError:
        return None

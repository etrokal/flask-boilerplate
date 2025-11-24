from ctypes import ArgumentError
import glob
from pathlib import Path
from typing import Any, Dict
from flask import current_app, g, json
from decouple import config


from .language_manager import Language

import os
from dotenv import dotenv_values

CONFIG = dotenv_values()
CONFIG['PROJECT_DIR'] = os.path.dirname(os.path.realpath(__file__))

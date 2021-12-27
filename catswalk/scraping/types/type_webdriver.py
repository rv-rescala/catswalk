from enum import Enum
from dataclasses import dataclass
from typing import List, Mapping

class EXECUTION_ENV(Enum):
    LOCAL = "local"
    LOCAL_HEADLESS = "local_headless"
    AWS_LAMBDA = "aws_lambda"


@dataclass
class DeviceType:
    """[summary]
    """
    mode: str
    agent: str

class DEVICE_MODE(Enum):
    DESKTOP = "Desktop"
    MOBILE = "Mobile"

class DEVICE(Enum):
    DESKTOP_GENERAL = DeviceType(mode=DEVICE_MODE.DESKTOP, agent="general")
    MOBILE_GALAXY_S5 = DeviceType(mode=DEVICE_MODE.MOBILE, agent="Galaxy S5")
    
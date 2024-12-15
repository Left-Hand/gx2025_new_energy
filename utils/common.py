import ezdxf
import os
from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace
from ezdxf.math import Vec2
import numpy as np
from typing import *
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

Points: TypeAlias = np.ndarray


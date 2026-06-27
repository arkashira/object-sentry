from dataclasses import dataclass
from enum import Enum
from typing import List, Any

class Technique(Enum):
    GRAYSCALE = 1
    BLUR = 2
    SHARPEN = 3

@dataclass
class Image:
    data: bytes

class ImageProcessor:
    def __init__(self):
        self.techniques = [Technique.GRAYSCALE, Technique.BLUR, Technique.SHARPEN]

    def get_techniques(self) -> List[Technique]:
        return self.techniques

    def _to_technique(self, technique: Any) -> Technique:
        """
        Convert input to a Technique enum if possible.
        Raises ValueError if the conversion fails.
        """
        if isinstance(technique, Technique):
            return technique
        try:
            return Technique(technique)
        except ValueError:
            raise ValueError("Invalid technique")

    def apply_technique(self, image: Image, technique: Any) -> Image:
        technique = self._to_technique(technique)

        # Simulate image processing
        if technique == Technique.GRAYSCALE:
            return Image(data=b'grayscale_image')
        elif technique == Technique.BLUR:
            return Image(data=b'blurred_image')
        elif technique == Technique.SHARPEN:
            return Image(data=b'sharpened_image')
        else:
            # Should never reach here because _to_technique validates
            raise ValueError("Invalid technique")

    def validate_technique(self, technique: Any) -> bool:
        try:
            tech = self._to_technique(technique)
            return tech in self.techniques
        except ValueError:
            return False

from image_processing import Image, ImageProcessor, Technique
import pytest

def test_get_techniques():
    processor = ImageProcessor()
    techniques = processor.get_techniques()
    assert len(techniques) == 3
    assert techniques[0] == Technique.GRAYSCALE
    assert techniques[1] == Technique.BLUR
    assert techniques[2] == Technique.SHARPEN

def test_apply_technique():
    processor = ImageProcessor()
    image = Image(data=b'original_image')
    new_image = processor.apply_technique(image, Technique.GRAYSCALE)
    assert new_image.data == b'grayscale_image'

def test_apply_invalid_technique():
    processor = ImageProcessor()
    image = Image(data=b'original_image')
    with pytest.raises(ValueError):
        processor.apply_technique(image, 4)

def test_validate_technique():
    processor = ImageProcessor()
    assert processor.validate_technique(Technique.GRAYSCALE) == True
    assert processor.validate_technique(4) == False

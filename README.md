# Object Sentry

Object Sentry is a platform for object detection in images and videos.

## Usage

1. Run `python -m src.object_sentry --filename test.jpg --content-type image/jpeg`
2. The platform will validate the file upload and provide an error message if the file format is invalid.
3. If the file format is valid, the platform will upload the file and detect objects in it.

## Testing

1. Run `python -m pytest tests/test_object_sentry.py`
2. The tests will exercise the acceptance criteria and ensure the platform is working correctly.

import argparse
import dataclasses
import json
from typing import List

@dataclasses.dataclass
class FileUpload:
    filename: str
    content_type: str
    data: bytes

class ObjectSentry:
    def __init__(self):
        self.supported_formats = ['image/jpeg', 'image/png', 'video/mp4']

    def validate_file_upload(self, file_upload: FileUpload) -> bool:
        if file_upload.content_type not in self.supported_formats:
            return False
        return True

    def upload_file(self, file_upload: FileUpload) -> str:
        if not self.validate_file_upload(file_upload):
            raise ValueError("Invalid file format")
        return f"File {file_upload.filename} uploaded successfully"

    def detect_objects(self, file_upload: FileUpload) -> List[str]:
        # Simulate object detection
        return ["object1", "object2"]

def main():
    parser = argparse.ArgumentParser(description="Object Sentry")
    parser.add_argument("--filename", help="Filename to upload")
    parser.add_argument("--content-type", help="Content type of the file")
    args = parser.parse_args()

    object_sentry = ObjectSentry()
    file_upload = FileUpload(args.filename, args.content_type, b"file_data")
    try:
        result = object_sentry.upload_file(file_upload)
        print(result)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

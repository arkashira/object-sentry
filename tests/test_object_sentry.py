from object_sentry import ObjectSentry, FileUpload

def test_validate_file_upload_valid_format():
    object_sentry = ObjectSentry()
    file_upload = FileUpload("test.jpg", "image/jpeg", b"file_data")
    assert object_sentry.validate_file_upload(file_upload) == True

def test_validate_file_upload_invalid_format():
    object_sentry = ObjectSentry()
    file_upload = FileUpload("test.txt", "text/plain", b"file_data")
    assert object_sentry.validate_file_upload(file_upload) == False

def test_upload_file_valid_format():
    object_sentry = ObjectSentry()
    file_upload = FileUpload("test.jpg", "image/jpeg", b"file_data")
    assert object_sentry.upload_file(file_upload) == "File test.jpg uploaded successfully"

def test_upload_file_invalid_format():
    object_sentry = ObjectSentry()
    file_upload = FileUpload("test.txt", "text/plain", b"file_data")
    try:
        object_sentry.upload_file(file_upload)
        assert False
    except ValueError as e:
        assert str(e) == "Invalid file format"

def test_detect_objects():
    object_sentry = ObjectSentry()
    file_upload = FileUpload("test.jpg", "image/jpeg", b"file_data")
    assert object_sentry.detect_objects(file_upload) == ["object1", "object2"]

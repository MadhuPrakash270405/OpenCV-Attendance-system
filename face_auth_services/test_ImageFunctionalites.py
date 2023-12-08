import pytest
from face_auth_services.ImageFunctionalites import check_face_in_image

# Create test data for images
valid_face_image_data = "../resources/images/2837016.png"
invalid_face_image_data = "../resources/images/invalid_image.jpeg"

def test_check_face_in_image_valid():
    result = check_face_in_image(valid_face_image_data)
    assert result is True

def test_check_face_in_image_invalid():
    result = check_face_in_image(invalid_face_image_data)
    assert result is False

if __name__ == '__main__':
    pytest.main()

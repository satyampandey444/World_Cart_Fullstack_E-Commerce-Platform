from app.models import ImageData
from app import os



def read_image_as_binary(file_path: str) -> ImageData:
    """
    Reads an image from the specified path, converts it to binary data,
    and returns an ImageData object for database entry.

    Args:
        file_path (str): The path to the image file.

    Returns:
        ImageData: The ImageData object containing the image's name and binary data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    # Extract the file name from the path
    file_name = os.path.basename(file_path)

    # Read the image as binary data
    with open(file_path, "rb") as file:
        binary_data = file.read()

    # Create an ImageData object with the file name and binary data
    image_record = ImageData(name=file_name, binary_data=binary_data)
    return image_record
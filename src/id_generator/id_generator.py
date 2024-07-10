import random
import string
import uuid


def generate_guid() -> str:
    """A generator that creates a GUID."""

    return str(uuid.uuid4())


def generate_id(length: int = 8) -> str:
    """A generator that creates an ID with a specific length.

    Args:
        length: The length of the ID.

    Returns:
        The generated ID.

    Raises:
        ValueError: If the length parameter is not an integer.
        ValueError: If the length is less than 1 or greater than 36.
    """

    if not isinstance(length, int):
        raise ValueError("Length must be an integer.")

    if length < 1:
        raise ValueError("Length must be greater than 0.")

    if length > 36:
        raise ValueError("Length must be less than or equal to 36.")

    generated_id = str(uuid.uuid4())[:length]

    if generated_id.endswith("-"):
        character = random.choice(string.ascii_letters)

        generated_id = generated_id[:-1]
        generated_id += character

    return generated_id


def generate_client_id(client_id: str, length: int) -> str:
    """Generate a client ID.

    Args:
        client_id: The client ID.
        length: The length of the ID.

    Returns:
        The generated client ID.

    Raises:
        ValueError: If the client ID is empty.
        ValueError: If the client ID is not a string.
        ValueError: If the length is not an integer.
        ValueError: If the length is less than 1.
        ValueError: If the length is greater than 36.
    """

    if not client_id:
        raise ValueError("Client ID cannot be empty.")

    if not isinstance(client_id, str):
        raise ValueError("Client ID must be a string.")

    if not isinstance(length, int):
        raise ValueError("Length must be an integer.")

    if length < 1:
        raise ValueError("Length must be greater than 0.")

    if length > 36:
        raise ValueError("Length must be less than or equal to 36.")

    replace_text = {"_": "-", " ": "-"}

    for key, value in replace_text.items():
        if key in client_id:
            client_id = client_id.replace(key, value)

    return client_id + "-" + generate_id(length)

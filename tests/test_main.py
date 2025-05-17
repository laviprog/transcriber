from src.main import welcome_message


def test_welcome_message_returns_correct_string():
    expected = "Hello from python-best-template!"
    result = welcome_message()
    assert result == expected, f"Expected '{expected}', but got '{result}'"


def test_welcome_message_type():
    result = welcome_message()
    assert isinstance(result, str), "Return value should be of type 'str'"

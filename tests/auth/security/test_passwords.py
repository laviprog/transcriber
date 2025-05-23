from src.auth.security.passwords import hash_password, verify_password


def test_hash_password_returns_string():
    """Test that hash_password returns a non-empty string."""
    password = "test_password"
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_hash_password_generates_different_hashes():
    """Test that same password generates different hashes (salt verification)."""
    password = "test_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_verify_password_correct():
    """Test that verify_password returns True for correct password."""
    password = "test_password"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test that verify_password returns False for incorrect password."""
    password = "test_password"
    hashed = hash_password(password)

    assert verify_password("wrong_password", hashed) is False


def test_hash_format_is_argon2():
    """Test that hash uses Argon2 format."""
    hashed = hash_password("test_password")
    assert hashed.startswith("$argon2")

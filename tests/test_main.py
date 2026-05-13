from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_read_root_returns_ok_status() -> None:
    """Valida retorno de status ok no endpoint raiz."""

    # Arrange
    expected_payload = {"status": "ok"}

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_payload

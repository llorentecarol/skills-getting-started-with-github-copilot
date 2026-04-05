def test_get_activities(client):
    """Arrange-Act-Assert: GET /activities returns all activities."""
    # Arrange
    # (default state is prepared by the reset fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_successful(client):
    """Arrange-Act-Assert: Sign up for a valid activity."""
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup(client):
    """Arrange-Act-Assert: Duplicate signup returns a 400 error."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_unknown_activity(client):
    """Arrange-Act-Assert: Signup to an unknown activity returns 404."""
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


def test_unregister_successful(client):
    """Arrange-Act-Assert: Unregister removes a participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_non_registered(client):
    """Arrange-Act-Assert: Unregister fails for a non-registered student."""
    # Arrange
    activity_name = "Art Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_unknown_activity(client):
    """Arrange-Act-Assert: Unregister from unknown activity returns 404."""
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()

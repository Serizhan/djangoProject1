from datetime import date

import pytest


@pytest.mark.django_db
def test_create_vacancy(client, hr_token):
    expected_response = {
        "id": 1,
        "created": date.today().strftime("%Y-%m-%d"),
        "skills": [],
        "slug": "123",
        "text": "123",
        "status": "draft",
        "min_experience": None,
        "likes": 0,
        "updated_at": None,
        "user": None

    }

    data = {
        "slug": "123",
        "text": "123",
        "status": "draft"
    }

    response = client.post(
        "/vacancy/create/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION="Token " + hr_token
    )

    assert response.status_code == 200
    assert response.data == expected_response

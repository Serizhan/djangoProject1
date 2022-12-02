# from datetime import date
#
# import pytest
#
# from vacancies.models import Vacancy


# @pytest.mark.django_db
# def test_vacancy_list(client):
#     vacancy = Vacancy.objects.create(
#         slug="123",
#         text="123"
#     )
#
#     expected_response = {
#         "count": 1,
#         "next": None,
#         "previous": None,
#         "results": [{
#             "id": vacancy.pk,
#             "text": "123",
#             "slug": "123",
#             "status": "draft",
#             "created": date.today().strftime("%Y-%m-%d"),
#             "username": None,
#             "skills": []
#         }]
#     }
#
#     response = client.get("/vacancy/")
#
#     assert response.status_code == 200
#     assert response.data == expected_response


from django.urls import path

from vacancies import views


urlpatterns = [
    path('', views.VacancyListView.as_view()),
    path('<int:pk>/', views.VacancyDetailView.as_view()),
    path('create/', views.VacancyCreateView.as_view()),
    path('<int:pk>/update/', views.VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', views.VacancyDestroyView.as_view()),
    path('by_user/', views.user_vacancies),
    path('like/', views.VacancyLikeView.as_view()),
]

from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from djangoProject1 import settings
from vacancies.models import Vacancy, Skill
from vacancies.permissions import VacancyCreatePermission
from vacancies.serializers import VacancyDetailSerializer, VacancyListSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello(request):
    return HttpResponse('Hello World')


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )
        skills = request.GET.getlist('skill', None)
        skills_q = None
        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
            else:
                skills_q |= Q(skills__name__icontains=skill)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDestroyView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vacancies(request):
    user_qs = User.objects.annotate(vacancies=Count('vacancy'))

    paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    users = []
    for user in page_object:
        users.append({
            "id": user.id,
            "name": user.username,
            "vacancies": user.vacancies
        })

    response = {
        "items": users,
        "total": paginator.count,
        "num_page": paginator.num_pages,
        "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
    }

    return JsonResponse(response)


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
                            safe=False)

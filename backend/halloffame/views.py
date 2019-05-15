from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from halloffame.filters import HeroFilterSet
from halloffame.models import Hero
from halloffame.permissions import IsOwnerOrReadOnly
from halloffame.serializers import HeroSerializer


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet
    ordering_fields = ('user__username', 'battles_won', 'battles_lost', 'level')

    def get_queryset(self):
        return Hero.objects.get_annotations()

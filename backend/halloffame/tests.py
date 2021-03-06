from rest_framework import test, status
from rest_framework.reverse import reverse

from battles.factories import BattleFactory
from halloffame.factories import HeroFactory, UserFactory, RaceFactory, GuildFactory
from halloffame.models import Hero


class HallOfFamePermissionsTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.race1 = RaceFactory()
        cls.race2 = RaceFactory()
        cls.guild1 = GuildFactory()
        cls.guild2 = GuildFactory()
        cls.hero_list_url = reverse('hero-list')

    def setUp(self):
        self.user1 = UserFactory()
        self.user1_url = reverse("hero-detail", args=(self.user1.id,))
        self.user2 = UserFactory()
        self.user2_url = reverse("hero-detail", args=(self.user2.id,))
        self.client.force_login(self.user1)

    def test_create_new_hero(self):
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_not_create_second_hero(self):
        HeroFactory(user=self.user1)
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Hero.objects.count(), 1)

    def test_create_new_hero_assigned_to_someone_else(self):
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user2.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Hero.objects.count(), 0)

    def test_delete_someone_elses_hero(self):
        HeroFactory(user=self.user2)
        response = self.client.delete(self.user2_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_change_guild(self):
        HeroFactory(user=self.user1)
        response = self.client.patch(self.user1_url, {'user': self.user1.id, 'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_change_someone_elses_guild(self):
        HeroFactory(user=self.user2)
        response = self.client.patch(self.user2_url, {'user': self.user2.id, 'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HallOfFameFilteringTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hero_list_url = reverse('hero-list')
        cls.hero1 = HeroFactory()
        cls.hero2 = HeroFactory()
        cls.hero3 = HeroFactory()

        cls.battle1 = BattleFactory(attendees=(cls.hero1, cls.hero2), looser=cls.hero1, is_looser_dead=False)
        cls.battle2 = BattleFactory(attendees=(cls.hero1, cls.hero3), looser=cls.hero1, is_looser_dead=False)
        cls.battle3 = BattleFactory(attendees=(cls.hero2, cls.hero3), looser=cls.hero3, is_looser_dead=True)

    def test_alive_heroes_filtering(self):
        response = self.client.get(self.hero_list_url, {'is_alive': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_dead_heroes_filtering(self):
        response = self.client.get(self.hero_list_url, {'is_alive': 'False'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_available_opponents_for_specified_hero_filtering(self):
        self.hero1.race.can_fight_with.set([self.hero1.race, self.hero2.race, self.hero3.race])
        self.hero1.race.save()
        hero4 = HeroFactory(race=self.hero1.race)
        BattleFactory(attendees=(hero4, self.hero3), looser= self.hero3)

        response = self.client.get(self.hero_list_url, {'find_opponents_for': hero4.user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

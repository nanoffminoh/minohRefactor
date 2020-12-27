import unittest
from model.reward import Reward, RewardList, Stats
from tests import MOCK_REWARD_WIFI, MOCK_REWARD_SATELLITE, MAXED_STATS,\
    REWARD_TABLET1, REWARD_TABLET2, REWARD_WINE, REWARD_WIFI


class RewardTest(unittest.TestCase):

    def test_create_reward(self):
        new_reward = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                            MOCK_REWARD_WIFI['rewards'])
        self.assertEqual(new_reward.reward_type, MOCK_REWARD_WIFI['type'])
        self.assertEqual(new_reward.name, MOCK_REWARD_WIFI['name'])
        self.assertEqual(new_reward.stat_requirement.get_value('Contract'), MOCK_REWARD_WIFI['stats']['Contract'])

    def test_create_reward_with_empty_fields(self):
        new_reward = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'])
        self.assertEqual(new_reward.reward_type, MOCK_REWARD_WIFI['type'])
        self.assertEqual(new_reward.name, MOCK_REWARD_WIFI['name'])
        self.assertEqual(new_reward.stat_requirement.get_value('Contract'), 0)
        self.assertEqual(new_reward.material_requirement, 0)
        self.assertEqual(new_reward.reward_requirement, [])

    def test_reward_total_requirements(self):
        reward = Reward('myName', 'Contract', stats={'Tech': 3, 'Artifact': 4}, materials=5, rewards=[])
        self.assertEqual(reward.stat_requirement.sum_stat(), 3+4)
        self.assertEqual(reward.total_requirements(), 3+4+5)


class RewardListTest(unittest.TestCase):

    def test_create_and_fill_reward_list(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'])
        reward_list = RewardList()
        self.assertEqual(len(reward_list.pending_rewards), 0)
        self.assertEqual(len(reward_list.obtained_rewards), 0)
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.pending_rewards), 1)
        self.assertEqual(len(reward_list.obtained_rewards), 0)
        # getting reward
        self.assertEqual(reward_list.get_pending_reward(MOCK_REWARD_WIFI['name']).name, MOCK_REWARD_WIFI['name'])

    def test_obtain_reward(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'])
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.pending_rewards), 1)
        self.assertEqual(len(reward_list.obtained_rewards), 0)
        self.assertEqual(reward_list.is_obtained(MOCK_REWARD_WIFI['name']), False)
        reward_list.obtain_reward(MOCK_REWARD_WIFI['name'])
        self.assertEqual(len(reward_list.pending_rewards), 0)
        self.assertEqual(len(reward_list.obtained_rewards), 1)
        self.assertEqual(reward_list.is_obtained(MOCK_REWARD_WIFI['name']), True)

    def test_stats_requirement(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                      MOCK_REWARD_WIFI['rewards'])
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.possible_rewards()), 0)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)

    def test_reward_requirement(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                      MOCK_REWARD_WIFI['rewards'])
        satellite = Reward(MOCK_REWARD_SATELLITE['name'], MOCK_REWARD_SATELLITE['type'], MOCK_REWARD_SATELLITE['stats'],
                           MOCK_REWARD_SATELLITE['materials'], MOCK_REWARD_SATELLITE['rewards'])
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        reward_list.add_pending_reward(satellite)
        self.assertEqual(len(reward_list.pending_rewards), 2)
        self.assertEqual(len(reward_list.obtained_rewards), 0)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)
        reward_list.obtain_reward(MOCK_REWARD_WIFI['name'])
        self.assertEqual(len(reward_list.pending_rewards), 1)
        self.assertEqual(len(reward_list.obtained_rewards), 1)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)

    def test_reward_type(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                      MOCK_REWARD_WIFI['rewards'])
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS), team='RD')), 1)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS), team='Exploration')), 0)

    def test_unobtainable_reward(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                      MOCK_REWARD_WIFI['rewards'], obtainable=False)
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 0)
        wifi2 = Reward('test', MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                       MOCK_REWARD_WIFI['rewards'])
        reward_list.add_pending_reward(wifi2)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)

    def test_material_requirements(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], 1,
                      MOCK_REWARD_WIFI['rewards'])
        reward_list = RewardList()
        reward_list.add_pending_reward(wifi)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 0)
        wifi2 = Reward('test', MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], MOCK_REWARD_WIFI['materials'],
                       MOCK_REWARD_WIFI['rewards'])
        reward_list.add_pending_reward(wifi2)
        self.assertEqual(len(reward_list.possible_rewards(stats=Stats(MAXED_STATS))), 1)

    def test_reward_name_listing(self):
        wifi = Reward(MOCK_REWARD_WIFI['name'], MOCK_REWARD_WIFI['type'], MOCK_REWARD_WIFI['stats'], 1,
                      MOCK_REWARD_WIFI['rewards'])
        reward_list = RewardList()
        self.assertEqual(reward_list.list_reward_names(), [])
        reward_list.add_pending_reward(wifi)
        self.assertEqual(reward_list.list_reward_names(), [MOCK_REWARD_WIFI['name']])
        self.assertEqual(reward_list.list_obtained_reward_names(), [])
        self.assertEqual(reward_list.list_pending_reward_names(), [MOCK_REWARD_WIFI['name']])
        reward_list.obtain_reward(MOCK_REWARD_WIFI['name'])
        self.assertEqual(reward_list.list_obtained_reward_names(), [MOCK_REWARD_WIFI['name']])
        self.assertEqual(reward_list.list_pending_reward_names(), [])
        self.assertEqual(reward_list.list_reward_names(), [MOCK_REWARD_WIFI['name']])

    def test_sorting_essential_rewards(self):
        reward_list = RewardList()
        self.assertEqual(reward_list.list_reward_names(), [])
        reward_list.add_pending_reward(REWARD_TABLET2)
        reward_list.add_pending_reward(REWARD_WINE)
        reward_list.add_pending_reward(REWARD_TABLET1)
        self.assertEqual(REWARD_WINE.essential, True)
        self.assertEqual(REWARD_TABLET2.essential, False)
        self.assertEqual(reward_list.list_reward_names(), ['Tablet2', 'Wine', 'Tablet1'])
        reward_list.sort_put_essentials_on_top()
        self.assertEqual(reward_list.list_reward_names(), ['Wine', 'Tablet2', 'Tablet1'])

    def test_sorting_rewards_by_requirement(self):
        reward1 = Reward('Name1', 'Contract', stats={'Contract': 2}, materials=3, rewards=[])
        reward2 = Reward('Name2', 'Contract', stats={'Tech': 3, 'Artifact': 4}, materials=5, rewards=[])
        reward3 = Reward('Name3', 'Contract', stats={'Memento': 3, 'Artifact': 4}, materials=0, rewards=[])
        reward_list = RewardList()
        reward_list.add_pending_reward(reward1)
        reward_list.add_pending_reward(reward2)
        reward_list.add_pending_reward(reward3)
        self.assertEqual(reward_list.list_reward_names(), ['Name1', 'Name2', 'Name3'])
        reward_list.sort_rewards_by_requirements_sum()
        self.assertEqual(reward_list.list_reward_names(), ['Name2', 'Name3', 'Name1'])

    def test_sorting_rewards_by_stat_priority(self):
        team_stats = Stats({'Artifact': 2, 'Memento': 4})
        reward_list = RewardList()
        reward_list.add_pending_reward(REWARD_WIFI)
        reward_list.add_pending_reward(REWARD_TABLET1)
        reward_list.add_pending_reward(REWARD_WINE)
        reward_list.add_pending_reward(REWARD_TABLET2)
        self.assertEqual(reward_list.list_reward_names(), ['WiFi', 'Tablet1', 'Wine', 'Tablet2'])
        reward_list.sort_rewards_by_type(team_stats.list_stats())
        self.assertEqual(reward_list.list_reward_names(), ['Tablet1', 'Tablet2', 'Wine', 'WiFi'])

    def test_get_reward_choices(self):
        team_stats = Stats({'Tech': 6, 'Contract': 6})
        reward_list = RewardList()
        reward_list.add_pending_reward(REWARD_WIFI)
        choices = reward_list.get_reward_choices(team_stats, material=0)
        self.assertEqual(choices, [('Connect the hotel to the internet.', 'WiFi'), ('Ignore and keep researching.', 'none')])

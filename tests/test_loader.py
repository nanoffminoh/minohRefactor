import unittest
from presets import preset_rewards, preset_guest_stats, preset_couple_stats
from access.loader import load_reward_list, load_guest, load_relationships
from model.reward import RewardList
from model.couple import RelationshipList
from model.guest import GuestList
from model.stats import Stats


class RewardTest(unittest.TestCase):

    def test_load_rewards_correctly(self):
        reward_list = RewardList()
        self.assertEqual(reward_list.list_reward_names(), [])
        load_reward_list(preset_rewards, reward_list=reward_list)
        self.assertEqual(len(reward_list.list_reward_names()), len(list(preset_rewards.keys())))

    def test_update_rewards_list(self):
        reward_list = RewardList()
        first_reward_name = list(preset_rewards.keys())[0]
        first_reward = preset_rewards[first_reward_name]
        # only load first element
        load_reward_list({first_reward_name: first_reward}, reward_list)
        self.assertEqual(reward_list.list_reward_names(), [first_reward_name])
        # load full list
        load_reward_list(preset_rewards, reward_list=reward_list)
        self.assertEqual(len(reward_list.list_reward_names()), len(list(preset_rewards.keys())))

    def test_essential_and_unobtainable_rewards(self):
        reward_list = RewardList()
        load_reward_list(preset_rewards, reward_list=reward_list)
        # testing obtainable, non-essential reward
        tablet1 = reward_list.get_pending_reward('Tablet1')
        self.assertEqual(tablet1.obtainable, True)
        self.assertEqual(tablet1.essential, False)
        # testing obtainable, essential reward
        tablet1 = reward_list.get_pending_reward('Wine')
        self.assertEqual(tablet1.obtainable, True)
        self.assertEqual(tablet1.essential, True)
        # testing unobtainable, non-essential reward
        tablet1 = reward_list.get_pending_reward('Build3')
        self.assertEqual(tablet1.obtainable, False)
        self.assertEqual(tablet1.essential, False)

    def test_add_guest(self):
        guest_list = GuestList()
        self.assertEqual(len(guest_list.get_free_guests()), 0)
        first_guest_name = list(preset_guest_stats.keys())[0]
        guest_list.add_guest(load_guest(first_guest_name, preset_guest_stats))
        self.assertEqual(len(guest_list.get_free_guests()), 1)
        self.assertEqual(guest_list.get_guest_stats(first_guest_name).get_value('Tech'),
                         preset_guest_stats[first_guest_name]['Tech'])

    def test_load_relationships(self):
        rel_list = RelationshipList()
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota,P,Storm')), 0)
        load_relationships(preset_couple_stats, rel_list)
        self.assertEqual(len(rel_list.get_relationships_that_can_start('Luke,Black,Onsen,Kota,P,Storm')),
                         len(list(preset_couple_stats.keys())))

    def test_couple_stats_load_correctly(self):
        rel_list = RelationshipList()
        load_relationships(preset_couple_stats, rel_list)
        self.assertEqual(preset_couple_stats['Luke,Black']['stats']['Tech'], 1)
        self.assertEqual(rel_list.get_relationship_status('Black,Luke'), 'unset')
        self.assertEqual(rel_list.get_bonus_stats_for_relationship('Black,Luke').get_value('Tech'),
                         Stats(preset_couple_stats['Luke,Black']['stats']).get_value('Tech'))

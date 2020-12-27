import unittest
from model.stats import Stats
from presets import preset_guest_stats

KOTA_STATS = preset_guest_stats['Kota']
LUKE_STATS = preset_guest_stats['Luke']


class StatsTest(unittest.TestCase):

    def test_stats_initialize_empty(self):
        new_stats = Stats()
        self.assertEqual(new_stats.get_value('Danger'), 0)

    def test_stats_initialize_not_empty(self):
        new_stats = Stats(KOTA_STATS)
        self.assertEqual(new_stats.get_value('Contract'), KOTA_STATS['Contract'])

    def test_stat_addition(self):
        kota_stats = Stats(KOTA_STATS)
        luke_stats = Stats(LUKE_STATS)
        self.assertEqual(kota_stats.get_value('Contract'), KOTA_STATS['Contract'])
        self.assertEqual(luke_stats.get_value('Contract'), LUKE_STATS['Contract'])
        stat_sum = kota_stats + luke_stats

        self.assertEqual(stat_sum.get_value('Contract'), KOTA_STATS['Contract'] + LUKE_STATS['Contract'])
        self.assertEqual(luke_stats.get_value('Contract'), LUKE_STATS['Contract'])
        self.assertEqual(kota_stats.get_value('Contract'), KOTA_STATS['Contract'])

    def test_max_stats(self):
        luke_stats = Stats(LUKE_STATS)
        self.assertEqual('Contract' not in luke_stats.top_stats(), True)
        self.assertEqual('Fragment' in luke_stats.top_stats(), True)
        self.assertEqual('Surveying' in luke_stats.top_stats(), True)

    def test_met_requirements(self):
        luke_stats = Stats(LUKE_STATS)
        kota_stats = Stats(KOTA_STATS)
        contract_2 = Stats({'Contract': 2})
        self.assertEqual(luke_stats.meets(contract_2), False)
        self.assertEqual(kota_stats.meets(contract_2), True)

    def test_stat_sum(self):
        empty = Stats()
        self.assertEqual(empty.sum_stat(), 0)
        full = Stats({'Tech': 2, 'Contract': 4})
        self.assertEqual(full.sum_stat(), 6)

    def test_stat_sub(self):
        stat1 = Stats({'Tech': 3, 'Contract': 4})
        stat2 = Stats({'Tech': 1, 'Artifact': 6})
        stat_sub = stat1 - stat2
        self.assertEqual(stat_sub.get_value('Tech'), 2)
        self.assertEqual(stat_sub.get_value('Contract'), 4)
        self.assertEqual(stat_sub.get_value('Artifact'), -6)

    def test_stat_equals(self):
        stat1 = Stats()
        stat2 = Stats()
        self.assertEqual(stat1 == stat2, True)
        stat3 = Stats({'Tech': 3})
        stat4 = Stats({'Contract': 4})
        self.assertEqual(stat1 == stat3, False)
        self.assertEqual(stat4 == stat3, False)
        stat5 = Stats({'Tech': 3, 'Contract': 4})
        self.assertEqual(stat4 + stat3 == stat5, True)

    def test_objects_dont_affect_each_other(self):
        blank1 = Stats()
        blank2 = Stats()
        self.assertEqual(blank1.sum_stat(), 0)
        self.assertEqual(blank2.sum_stat(), 0)

        blank2.increase_stat('Tech', 2)
        self.assertEqual(blank1.sum_stat(), 0)
        self.assertEqual(blank2.sum_stat(), 2)

    def test_stat_doesnt_modify_dictionary(self):
        my_dict = {'Tech': 3, 'Contract': 2}
        copy = my_dict.copy()
        not_blank = Stats(my_dict)
        self.assertEqual(not_blank.sum_stat(), 5)
        self.assertEqual(copy['Tech'], my_dict['Tech'])

        not_blank.increase_stat('Tech', 2)
        self.assertEqual(not_blank.sum_stat(), 7)
        self.assertEqual(copy['Tech'], my_dict['Tech'])

    def test_does_not_accept_incorrect_stat_names(self):
        stat = Stats({'Tech': 2, 'whatever': 5})
        self.assertEqual(len(stat.stat_dict.keys()), 7)
        self.assertEqual('whatever' in stat.stat_dict.keys(), False)
        self.assertEqual(stat.sum_stat(), 2)

    def test_default_stat_list(self):
        my_dict = {'Tech': 1, 'Contract': 4, 'Artifact': 3}
        stat = Stats(my_dict)
        self.assertEqual(stat.list_stats()[0]['stat'], 'Contract')
        self.assertEqual(len(stat.list_stats()), 3)

    def test_filtered_stat_list(self):
        my_dict = {'Tech': 1, 'Contract': 4, 'Artifact': 3}
        stat = Stats(my_dict)
        self.assertEqual(stat.list_stats(['Tech', 'Artifact'])[0]['stat'], 'Artifact')

    def filter_rd_and_exploration(self):
        my_dict = {'Tech': 1, 'Contract': 4, 'Artifact': 3, 'Fragment': 2, 'Memento': 3}
        stat = Stats(my_dict)
        self.assertEqual(stat.get_value('Tech'), 1)
        self.assertEqual(stat.get_value('Memento'), 3)
        self.assertEqual(stat.filter_rd().get_value('Tech'), 1)
        self.assertEqual(stat.filter_rd().get_value('Memento'), 0)
        self.assertEqual(stat.filter_exploration().get_value('Tech'), 0)
        self.assertEqual(stat.filter_exploration().get_value('Memento'), 3)

    def test_gets_top_stat_correctly(self):
        stat = Stats({'Tech': 1, 'Artifact': 3, 'Danger': 2})
        self.assertEqual(stat.top_stat(), 'Artifact')
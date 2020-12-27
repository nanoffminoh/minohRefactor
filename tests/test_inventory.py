import unittest
from model.inventory import Inventory, FileList
from model.stats import Stats


class InventoryTest(unittest.TestCase):

    def test_initialize_inventory(self):
        inventory = Inventory()
        self.assertEqual(inventory.accumulated_stats['RD'].sum_stat(), 0)
        self.assertEqual(inventory.accumulated_stats['Exploration'].sum_stat(), 0)
        self.assertEqual(inventory.get_passive_bonus().sum_stat(), 0)
        self.assertEqual(inventory.items, [])
        self.assertEqual(inventory.rawMaterials, 0)

    def test_items(self):
        inventory = Inventory()
        self.assertEqual(inventory.items, [])
        inventory.add_item('bag')
        self.assertEqual(inventory.items, ['bag'])
        inventory.add_item('bag')
        self.assertEqual(inventory.items, ['bag'])
        inventory.remove_item('ball')
        self.assertEqual(inventory.items, ['bag'])
        inventory.remove_item('bag')
        self.assertEqual(inventory.items, [])

    def test_modify_passive_bonus(self):
        inventory = Inventory()
        self.assertEqual(inventory.get_passive_bonus().sum_stat(), 0)
        inventory.increase_passive_bonus('Tech', 3)
        self.assertEqual(inventory.get_passive_bonus().sum_stat(), 3)
        inventory.increase_passive_bonus('Danger', -1)
        self.assertEqual(inventory.get_passive_bonus().sum_stat(), 2)

    def test_spend_stats(self):
        inventory = Inventory()
        self.assertEqual(inventory.accumulated_stats['RD'].sum_stat(), 0)
        self.assertEqual(inventory.accumulated_stats['Exploration'].sum_stat(), 0)
        inventory.accumulate_stats(Stats({'Tech': 3, 'Contract': 2}), 'RD')
        self.assertEqual(inventory.accumulated_stats['RD'].sum_stat(), 5)
        self.assertEqual(inventory.accumulated_stats['Exploration'].sum_stat(), 0)
        inventory.spend_stats(Stats({'Tech': 1}), 'RD')
        self.assertEqual(inventory.accumulated_stats['RD'].sum_stat(), 4)
        self.assertEqual(inventory.accumulated_stats['Exploration'].sum_stat(), 0)


class FileListTest(unittest.TestCase):

    def test_empty_file_list(self):
        file_list = FileList()
        self.assertEqual(file_list.files['Memento'], [])

    def test_add_file_to_list(self):
        file_list = FileList()
        file_list.add_file('memento', {'id': 'file1', 'name': 'My File'})
        self.assertEqual(len(file_list.files['Memento']), 1)
        self.assertEqual(file_list.get_files('Memento')[0]['name'], 'My File')

    def test_add_invalid_file(self):
        file_list = FileList()
        file_list.add_file('memento', {'name': 'My File'})
        self.assertEqual(len(file_list.files['Memento']), 0)

    def test_add_repeated_file(self):
        file_list = FileList()
        file_list.add_file('memento', {'id': 'file1', 'name': 'My File'})
        file_list.add_file('memento', {'id': 'file1', 'name': 'My File'})
        self.assertEqual(len(file_list.files['Memento']), 1)

    def test_list_file_types(self):
        file_list = FileList()
        file_list.add_file('memento', {'id': 'file1', 'name': 'My File'})
        self.assertEqual(file_list.list_file_types(), ['Memento'])
        file_list.add_file('artifact', {'id': 'file2', 'name': 'My Arfitact'})
        self.assertEqual(file_list.list_file_types(), ['Memento', 'Artifact'])

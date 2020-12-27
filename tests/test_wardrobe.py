import unittest
from model.wardrobe import Wardrobe


class WardrobeTest(unittest.TestCase):

    def test_keys_in_initialized_wardrobe(self):
        wardrobe = Wardrobe()
        self.assertTrue('fur' in wardrobe.clothing.keys())

    def test_initializes_with_default_clothes(self):
        wardrobe = Wardrobe()
        self.assertTrue(wardrobe.has_clothing("clothes", "40s"))
        self.assertFalse(wardrobe.has_clothing("clothes", "whatever"))

    def test_add_non_boolean_clothing(self):
        wardrobe = Wardrobe()
        self.assertFalse(wardrobe.has_clothing("clothes", "pijamas"))
        wardrobe.add('clothes', 'pijamas')
        self.assertTrue(wardrobe.has_clothing("clothes", "pijamas"))

    def test_add_boolean_clothing(self):
        wardrobe = Wardrobe()
        self.assertFalse(wardrobe.has_clothing("nose_ring", "True"))
        wardrobe.add("nose_ring", "True")
        self.assertTrue(wardrobe.has_clothing("nose_ring", "True"))

    def test_writes_boolean_filename_correctly(self):
        wardrobe = Wardrobe()
        self.assertEqual(wardrobe.clothing['nose_ring']['False']['idle'], 'gui/wardrobe/none_idle')
        wardrobe.add("nose_ring", "True")
        self.assertEqual(wardrobe.clothing['nose_ring']['True']['idle'], 'gui/wardrobe/nose_ring_idle')

    def test_writes_non_boolean_filename_correctly(self):
        wardrobe = Wardrobe()
        wardrobe.add("fur", "blue")
        self.assertEqual(wardrobe.clothing['fur']['blue']['hover'], 'gui/wardrobe/blue_hover')

    def test_cant_add_article_already_in(self):
        wardrobe = Wardrobe()
        self.assertTrue(wardrobe.has_clothing('clothes', '40s'))
        self.assertEqual(len(wardrobe.clothing['clothes'].keys()), 3)
        wardrobe.add('clothes', '40s')
        self.assertEqual(len(wardrobe.clothing['clothes'].keys()), 3)

    def test_fill_up_wardrobe(self):
        wardrobe = Wardrobe()
        self.assertFalse(wardrobe.has_clothing('fur', 'blue'))
        wardrobe.fill_up()
        self.assertTrue(wardrobe.has_clothing('fur', 'blue'))

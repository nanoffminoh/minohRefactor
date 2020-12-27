import unittest
from access.others import list_into_text, encrpyt_rank, decrypt_rank


class OthersTest(unittest.TestCase):

    def test_list_into_text(self):
        self.assertEqual(list_into_text(['Kota']), 'Kota')
        self.assertEqual(list_into_text(['Kota', 'Luke']), 'Kota and Luke')
        self.assertEqual(list_into_text(['Kota', 'Luke', 'Black']), 'Kota, Luke and Black')

    def test_encrypt_rank(self):
        self.assertEqual(encrpyt_rank(0), 'Fearsome Bronze Calf')
        self.assertEqual(encrpyt_rank(2.5), 'Grand Gold Calf')
        self.assertEqual(encrpyt_rank(-10), 'Fearsome Gold Peacock')
        self.assertEqual(encrpyt_rank(500), 'Great Bronze Auroch')

    def test_decrypt_rank(self):
        self.assertEqual(decrypt_rank('Fearsome Bronze Calf'), 0)
        self.assertEqual(decrypt_rank('Grand Gold Calf'), 2.5)
        self.assertEqual(decrypt_rank('Fearsome Gold Peacock'), -10)
        self.assertEqual(decrypt_rank('Great Bronze Auroch'), 32)

import unittest
from Decoder import *

class TestDecoderMethod(unittest.TestCase):
    def test_correct_test1(self):
        self.assertEqual(Decoder(Alphabet('test1\\alphabet.txt'),
                                 Probabilities('test1\\probs.csv')).ctcBeamSearch(),
                         'a')

    def test_correct_test2(self):
        self.assertEqual(Decoder(Alphabet('test2\\alphabet.txt'),
                                 Probabilities('test2\\probs1.csv')).ctcBeamSearch(),
                         'wo bekomme ich meine ausgabenliste')
        self.assertEqual(Decoder(Alphabet('test2\\alphabet.txt'),
                                 Probabilities('test2\\probs2.csv')).ctcBeamSearch(),
                         'wo ist das ärztezentrum')
        self.assertEqual(Decoder(Alphabet('test2\\alphabet.txt'),
                                 Probabilities('test2\\probs3.csv')).ctcBeamSearch(),
                         'wie vel uhr ist es')

    def test_correct_input(self):
        with self.assertRaises(NonCorrectDecoderInput):
            s = Decoder(Alphabet('test1\\alphabet1.txt'),
                    Probabilities('test1\\probs.csv')).ctcBeamSearch(None)


if __name__ == '__main__':
    unittest.main()
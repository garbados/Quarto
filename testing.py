import random
import unittest
from board import Board
import copy


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    def test_board(self):
        board = Board()
        ALL_PIECES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        ATTRIBUTES = [
            [0, 1, 2, 3, 4, 5, 6, 7],   [8, 9, 10, 11, 12, 13, 14, 15],
            [0, 1, 2, 3, 8, 9, 10, 11], [4, 5, 6, 7, 12, 13, 14, 15],
            [0, 1, 4, 5, 8, 9, 12, 13], [2, 3, 6, 7, 10, 11, 14, 15],
            [0, 2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13, 15]]

        for at in range(len(ATTRIBUTES)):
            att = ATTRIBUTES[at]
            for i in range(10000):
                all_possible_pieces = copy.deepcopy(att)
                four_pieces = list()
                for piece in range(4):
                    index = random.randrange(len(all_possible_pieces))
                    four_pieces.append(all_possible_pieces.pop(index))
                self.assertTrue(board.four_match(four_pieces[
                                0], four_pieces[1], four_pieces[2], four_pieces[3]))

        self.assertFalse(board.four_match(0, 1, 2, -1))

        for att in ATTRIBUTES:
            for i in range(10000):
                all_possible_pieces = copy.deepcopy(att)
                four_pieces = list()
                for piece in range(3):
                    index = random.randrange(len(all_possible_pieces))
                    four_pieces.append(all_possible_pieces.pop(index))
                all_possible_pieces = copy.deepcopy(ALL_PIECES)
                all_ats = list()
                for at in ATTRIBUTES:
                    there = True
                    for piece in four_pieces:
                        if piece not in at:
                            there = False
                            break
                    if(there):
                        all_ats.append(at)
                for a in all_ats:
                    for b in a:
                        if b in all_possible_pieces:
                            all_possible_pieces.remove(b)
                print all_possible_pieces
                print four_pieces
                index = random.randrange(len(all_possible_pieces))
                four_pieces.append(all_possible_pieces.pop(index))
                four_pieces = list(set(four_pieces))
                print four_pieces
                self.assertFalse(board.four_match(four_pieces[
                                 0], four_pieces[1], four_pieces[2], four_pieces[3]))


if __name__ == '__main__':
    unittest.main()

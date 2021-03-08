import unittest
import pygame
from gui_items import Arrow, Text, MessageBox, Timer, Hand

class TestArrow(unittest.TestCase):
    def setUp(self):
        self.arrow = Arrow((0, 0), False, None)

    def test_color_before(self):
        self.assertEqual(self.arrow.color, Arrow.DEF_COLOR)

    def test_mouse(self):
        self.assertTrue(self.arrow.check_mouse((25, 25)))
        self.assertEqual(self.arrow.color, Arrow.HOVER_COLOR)


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer((0, 0))

    def test_count(self):
        for _ in range(Timer.LENGTH + 20):
            self.timer.update()
        self.assertEqual(self.timer.count, Timer.LENGTH - 20)

    def test_timeout(self):
        for _ in range(Timer.LENGTH - 1):
            self.timer.update()
        self.assertTrue(self.timer.update())


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(0)

    def test_len(self):
        for i in range(3):
            self.hand.add(i)
        self.assertEqual(len(self.hand.cards), 3)

    def test_cycle(self):
        for i in range(3):
            self.hand.add(i)
        for _ in range(4):
            self.hand.cycle_right()
        self.assertEqual(self.hand.selected, 1)
        for _ in range(2):
            self.hand.cycle_left()
        self.assertEqual(self.hand.selected, 2)
        self.hand.remove(0)
        self.assertEqual(self.hand.selected, 1)




if __name__ == "__main__":
    unittest.main()

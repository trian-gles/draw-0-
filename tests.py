import unittest
from gui_items import Arrow, Text, MessageBox, Hand, TimeTimer
from freezegun import freeze_time
import time


class TestArrow(unittest.TestCase):
    def setUp(self):
        self.arrow = Arrow((0, 0), False, None)

    def test_color_before(self):
        self.assertEqual(self.arrow.color, Arrow.DEF_COLOR)

    def test_mouse(self):
        self.assertTrue(self.arrow.check_mouse((25, 25)))
        self.assertEqual(self.arrow.color, Arrow.HOVER_COLOR)


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(0)
        self.hand.update([0])
        self.hand.update([0, 1, 2, 3])

    def test_len(self):
        self.assertEqual(len(self.hand.cards), 4)
        self.hand.update([0, 1])
        self.assertEqual(len(self.hand.cards), 2)

    def test_cycle(self):
        self.assertEqual(self.hand.selected, 0)
        self.hand.cycle_left()
        self.assertEqual(self.hand.selected, 3)
        for _ in range(3):
            self.hand.cycle_right()
        self.assertEqual(self.hand.selected, 2)
        self.hand.update([0, 1])
        self.assertEqual(self.hand.selected, 1)


@freeze_time("2012-01-15 12:00:00")
class TestTimeTimer(unittest.TestCase):
    def setUp(self):
        self.timer = TimeTimer(0)
        self.time_start = time.time()

    def test_start(self):
        self.timer.update()
        self.assertEqual(self.timer.start_time, time.time())
        self.assertEqual(self.timer.lap, 0)

    @freeze_time("2012-01-15 12:00:03", as_kwarg="frozen_time")
    def test_move(self, **kwargs):
        self.assertIsNone(self.timer.update())
        self.assertEqual(self.timer.start_time, self.time_start)
        kwargs.get('frozen_time').move_to("2012-01-15 12:00:09")
        self.assertTrue(self.timer.update())
        self.timer.update()
        self.assertEqual(self.timer.lap, 0)


if __name__ == "__main__":
    unittest.main()

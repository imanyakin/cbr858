import unittest
import datetime

from cbr858.utilities import DatetimeInterval


class TestUtilities(unittest.TestCase):

    def test_date_membership(self):

        date = datetime.date(2024,9,1)

        interval_a = DatetimeInterval(
            start=datetime.date(2023, 9, 1),
            end = datetime.date(2024, 9, 2)
        )

        self.assertTrue(date in interval_a)

        interval_b = DatetimeInterval(
            start=datetime.date(2023, 9, 1),
            end=datetime.date(2024, 8, 31)
        )
        self.assertFalse(date in interval_b)
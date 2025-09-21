import datetime


class DatetimeInterval:

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def __contains__(self, item):
        """
        Check if item is in the required range
        :param item:
        :return:
        """
        assert isinstance(item, datetime.date)

        # note: relies on short-circuit of 'or' operator
        start_none = self.start is None
        end_none = self.end is None
        if (start_none or (item >= self.start)) and (end_none or (item <= self.end)):
            return True
        else:
            return False
# A list based of a Rolling List implementation which has a
# user specified size and once reached that size will delete
# the oldest element for a new one.
import collections


class BeaconList(collections.Sequence):
    def __init__(self, size):
        self._size = size
        self._items = []
        self._index = 0

    def __getitem__(self, index):
        return self._items[index]

    def __contains__(self, value):
        return self._items.__contains__(value)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return self._items.__iter__()

    def __str__(self):
        string = ""
        for val in self._items:
            string += val + "\n"
        return string

    def index(self, value):
        return super(BeaconList, self).index(value)

    def count(self, value):
        return super(BeaconList, self).count(value)

    def add(self, item):
        if len(self._items) < self._size:
            self._items.append(item)
        elif self._index < self._size:
            self._items[self._index] = item
        else:
            self._index = 0
            self._items[self._index] = item
        self._index += 1

    @property
    def items(self):
        return self._items

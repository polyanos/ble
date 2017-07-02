# A list based of a Rolling List implementation which has a
# user specified size and once reached that size will delete
# the oldest element for a new one.
import collections


class BeaconList(collections.Sequence):
    def __init__(self, size):
        self.size = size
        self.items = []
        self.index = 0

    def __getitem__(self, index):
        return super(BeaconList, self).__getitem__(index)

    def __reversed__(self):
        return self.items.__reversed__()

    def __contains__(self, value):
        self.items.__contains__(value)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def __str__(self):
        string = ""
        for val in self.items:
            string += val + "\n"
        return string

    def index(self, value):
        return super(BeaconList, self).index(value)

    def count(self, value):
        return super(BeaconList, self).count(value)

    def add(self, item):
        if len(self.items) < self.size:
            self.items.append(item)
        elif self.index < self.size:
            self.items[self.index] = item
        else:
            self.index = 0
            self.items[self.index] = item
        self.index += 1
# A list based of a Rolling List implementation which has a
# user specified size and once reached that size will delete
# the oldest element for a new one.


class BeaconList:
    def __init__(self, size):
        self.size = size
        self.items = []
        self.index = 0

    def add(self, item):
        if len(self.items) < self.size:
            self.items.append(item)
        elif self.index < self.size:
            self.items[self.index] = item
        else:
            self.index = 0
            self.items[self.index] = item
        self.index += 1

    def get(self, index):
        if index >= self.size or index < 0:
            raise IndexError("The specified index ({}) is bigger than the size of the list ({}) or the index is smaller than 0"
                             .format(index, self.size))
        return self.items[index]

    def items(self):
        return self.items

    def __str__(self):
        string = ""
        for val in self.items:
            string += val + "\n"
        return string

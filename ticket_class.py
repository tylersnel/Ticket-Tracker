class Ticket:

    def __init__(self, first,last, rank, date, unit, type):
        self.first = first
        self.last = last
        self.rank = rank
        self.date = date
        self.unit = unit
        self.type = type

    def first(self):
        return self.first

    def last(self):
        return self.last

    def rank(self):
        return self.rank

    def date(self):
        return self.date

    def unit(self):
        return self.unit

    def type(self):
        return self.type
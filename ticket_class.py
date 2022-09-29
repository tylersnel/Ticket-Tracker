class Ticket:

    def __init__(self, first,last, rank, date, unit, act_type):
        self.first = first
        self.last = last
        self.rank = rank
        self.date = date
        self.unit = unit
        self.act_type = act_type

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

    def act_type(self):
        return self.act_type
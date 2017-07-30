from matplotlib import pyplot as plt


class job():
    def __init__(self, processing_time=1, release_date=0, color=None):
        assert processing_time > 0, 'pt must be greater than zero'
        assert release_date >= 0, 'rd must be greater than or equal to zero.'
        assert type(processing_time) == int, 'pt must be int'
        assert type(release_date) == int, 'rd must be int'
        self.pt = processing_time
        self.rd = release_date
        self.ct = []
        self.c = color
        if color == None:
            self.c = '#4B0082'


    def __str__(self):
        return 'pt: ' + str(self.pt) + ', rd: ' + str(self.rd)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.pt == other.pt:
                return self.rd < other.rd
            return self.pt < other.pt
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def draw(self):
        for s, t in self.ct:
            plt.gca().add_patch(plt.Rectangle((s, 0), t-s, 0.2, color=self.c))

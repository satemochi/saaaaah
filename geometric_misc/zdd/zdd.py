import networkx as nx
from matplotlib import pyplot as plt


class zdd:
    """ Simple representation for Zero-suppressed decision diagrams
    """
    def __init__(self, verifier):
        self.v = verifier
        self.__initialize_dd()
        self.__build()

    def __initialize_dd(self):
        self.dd = nx.DiGraph()
        self.dd.add_node('zero', label='zero')
        self.dd.add_node('one', label='one')

    def __build(self):
        for t, e in enumerate(self.v.universe):
            self.v.classification(self.dd, t, e)

    def all_paths(self):
        s, t = self.v.get_root(), 'one'
        for p in nx.all_simple_paths(self.dd, source=s, target=t):
            yield p

    def draw(self, ax=None):
        pos = nx.nx_pydot.graphviz_layout(self.dd, prog='dot')
        nx.draw(self.dd, pos, ax=plt.gca(), node_color='#3333cc')

        el = nx.get_edge_attributes(self.dd, 'sign')
        nx.draw_networkx_edge_labels(self.dd, pos, edge_labels=el)

        vl = nx.get_node_attributes(self.dd, 'label')
        nx.draw_networkx_labels(self.dd, pos, labels=vl)

    def element_labels(self):
        return {e: i for i, e in enumerate(self.v.universe)}

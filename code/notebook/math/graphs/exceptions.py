from ...exceptions import NotebookCodeError


class GraphError(NotebookCodeError):
    pass


class VertexExistsError(GraphError):
    pass


class MissingVertexError(GraphError):
    pass


class EdgeExistsError(GraphError):
    pass


class MissingEdgeError(GraphError):
    pass


class GraphWalkError(GraphError):
    pass

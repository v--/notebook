from collections.abc import Callable, Collection
from typing import Any, overload

from .base_edge import BaseEdgeView


class BinaryEdgeViewMeta[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT](type):
    edge_class: type[EdgeT]

    def normalize_edge(cls, edge: tuple[VertT, VertT] | EdgeT) -> EdgeT:
        if isinstance(edge, cls.edge_class):
            return edge

        return cls.edge_class(*edge)

    def __new__[T: BinaryEdgeViewMeta](
        meta: type[T],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        edge_class: type[Collection] = tuple,
    ) -> T:
        attrs['edge_class'] = edge_class
        attrs['normalize_edge'] = meta.normalize_edge
        return type.__new__(meta, name, bases, attrs)


class BinaryEdgeView[VertT, EdgeT: Collection, VertLabelT, EdgeSymbolT](BaseEdgeView[VertT, EdgeT, VertLabelT, EdgeSymbolT], metaclass=BinaryEdgeViewMeta):
    edge_class: type[EdgeT]
    normalize_edge: Callable[[tuple[VertT, VertT] | EdgeT], EdgeT]

    def _add_edge(self, edge: tuple[VertT, VertT] | EdgeT) -> None:
        super().add(self.normalize_edge(edge))

    def _add_src_dest(self, src: VertT, dest: VertT) -> None:
        self._add_edge((src, dest))

    @overload
    def add(self, edge: tuple[VertT, VertT] | EdgeT) -> None: ...
    @overload
    def add(self, src: VertT, dest: VertT) -> None: ...
    def add(self, *args, **kwargs) -> None:
        if len(args) + len(kwargs) == 1:
            self._add_edge(*args, **kwargs)
        else:
            self._add_src_dest(*args, **kwargs)

    def _remove_edge(self, edge: tuple[VertT, VertT] | EdgeT) -> None:
        super().remove(self.normalize_edge(edge))

    def _remove_src_dest(self, src: VertT, dest: VertT) -> None:
        self._remove_edge(self.normalize_edge((src, dest)))

    @overload
    def remove(self, edge: tuple[VertT, VertT] | EdgeT) -> None: ...
    @overload
    def remove(self, src: VertT, dest: VertT) -> None: ...
    def remove(self, *args, **kwargs) -> None:
        if len(args) + len(kwargs) == 1:
            self._remove_edge(*args, **kwargs)
        else:
            self._remove_src_dest(*args, **kwargs)

    def __contains__(self, edge: tuple[VertT, VertT] | EdgeT) -> bool:
        return super().__contains__(self.normalize_edge(edge))

    def __getitem__(self, edge: tuple[VertT, VertT] | EdgeT) -> EdgeSymbolT:
        return super().__getitem__(self.normalize_edge(edge))

    def __setitem__(self, edge: tuple[VertT, VertT] | EdgeT, label: EdgeSymbolT) -> None:
        return super().__setitem__(self.normalize_edge(edge), label)

    def __delitem__(self, edge: tuple[VertT, VertT] | EdgeT) -> None:
        return super().__delitem__(self.normalize_edge(edge))

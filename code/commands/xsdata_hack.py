from typing import Any, get_type_hints

from xsdata.exceptions import XmlContextError
from xsdata.formats.dataclass.models.builders import XmlMetaBuilder


# TODO: Remove when this gets fixed upstream
def find_declared_class_patched(cls: type, clazz: type, name: str) -> Any:  # noqa: ARG001,ANN401
    """Find the user class that matches the name.

    Todo: Honestly I have no idea why we needed this.
    """
    for base in clazz.__mro__:
        # ann = base.__dict__.get("__annotations__")
        ann = get_type_hints(base)  # Only this line is modified

        if ann and name in ann:
            return base

    raise XmlContextError(f'Failed to detect the declared class for field {name}')



setattr(XmlMetaBuilder, 'find_declared_class', classmethod(find_declared_class_patched))  # noqa: B010

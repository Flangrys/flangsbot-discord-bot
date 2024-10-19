import typing


class Element(typing.TypedDict):
    """Represents the pizes of an HTML tag."""

    nametag: str
    """Represents a literal name tag. i.e: 'div' or 'fieldset'."""

    clazz: list[str] | None
    """Represents an dictionary with style classes."""

    id: str | None
    """Represents the element id."""

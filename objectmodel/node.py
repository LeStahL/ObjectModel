from typing import (
    Self,
    Any,
    List,
    Optional,
)
from enum import (
    Enum,
    Flag,
)
from inspect import isclass
from functools import reduce
from PyQt6.QtCore import QFileInfo

class Node:
    def __init__(
        self: Self,
        value: Any,
        index: int = -1,
        name: str = 'root',
        parent: Optional[Self] = None,
    ) -> None:
        self._value: Any = value
        self._parent: Optional[Self] = parent
        self._name: str = name
        self._index: int = index

        self._path: str = self._name if parent is None else '.'.join((parent.path, self._name)) 
        self._type = type(value)

        self.updateChildren()

    def updateChildren(self) -> None:
        if self.isObject:
            self._children = list(map(
                lambda key: Node(
                    value=getattr(self._value, key),
                    name=key,
                    parent=self,
                    index=list(self._value.__dict__.keys()).index(key),
                ),
                self._value.__dict__.keys(),
            ))
        elif self.isArray:
            self._children = list(map(
                lambda index: Node(
                    value=self._value[index],
                    name='[{}]'.format(index),
                    parent=self,
                    index=index,
                ),
                range(len(self._value)),
            ))
        else:
            self._children = []

    @property
    def path(self: Self) -> str:
        return self._path

    @property
    def children(self: Self) -> List[Self]:
        return self._children

    @property
    def name(self: Self) -> str:
        return self._name

    @property
    def parent(self: Self) -> str:
        return self._parent

    @property
    def depth(self: Self) -> int:
        return len(self._path.split('.'))

    @property
    def value(self: Self) -> Any:
        return self._value
    
    @value.setter
    def value(self: Self, value: Any) -> None:
        self._value = value

        if self._parent is not None:
            setattr(self._parent.value, self._name, value)

    @property
    def type(self: Self) -> Any:
        return self._type

    @property
    def index(self: Self) -> int:
        return self._index
    
    @property
    def maxDepth(self: Self) -> int:
        return reduce(
            lambda accumulator, addition: max(accumulator, addition),
            map(lambda child: child.maxDepth, self.children),
            self.depth,
        )

    @property
    def isEnum(self: Self) -> bool:
        return isinstance(self._value, Enum) and not isinstance(self._value, Flag)
    
    @property
    def isFlag(self: Self) -> bool:
        return isinstance(self._value, Flag)
    
    @property
    def isArray(self: Self) -> bool:
        return isinstance(self._value, list)
    
    @property
    def isBool(self: Self) -> bool:
        return isinstance(self._value, bool)

    @property
    def isObject(self: Self) -> bool:
        return isclass(self._type) and not (
            self.isEnum or \
            self.isFlag or \
            self.isArray or \
            self.isFloat or \
            self.isInt or \
            self.isString or \
            self.isBool or \
            self.isFilePath
        )

    @property
    def isString(self: Self) -> bool:
        return self._type == str
    
    @property
    def isInt(self: Self) -> bool:
        return self._type == int
    
    @property
    def isFloat(self: Self) -> bool:
        return self._type == float
    
    @property
    def isFilePath(self: Self) -> bool:
        return isinstance(self._value, QFileInfo)

    def childWithName(self: Self, name: str) -> Optional[Self]:
        for child in self._children:
            if child.name == name:
                return child
        return None

    def fromPath(self: Self, path: str) -> Optional[Self]:
        if not path.startswith(self.name):
            return None

        if self._name == path:
            return self

        pathComponents: List[str] = path.split('.')

        if len(pathComponents) <= 1:
            return None

        return self.childWithName(pathComponents[1]).fromPath('.'.join(pathComponents[1:]))

    def insertArrayElement(self: Self, at: int, value: Any) -> None:
        if self.isArray:
            self._value.insert(at, value)
            self.updateChildren()

    def removeArrayElement(self: Self, at: int) -> None:
        if self.isArray:
            del self._value[at]
            self.updateChildren()

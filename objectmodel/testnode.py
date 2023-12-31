from unittest import (
    TestCase,
    main,
)
from objectmodel.node import Node
from typing import (
    Self,
    List,
)
from enum import (
    StrEnum,
    IntFlag,
    IntEnum,
    auto,
)
from PyQt6.QtCore import QFileInfo

class AnEnum(StrEnum):
    Option1 = 'foo'
    Option2 = 'bar'

class AnIntEnum(IntEnum):
    A = auto()
    B = auto()

class AFlag(IntFlag):
    Nothing = 0
    First = auto()
    Second = auto()
    Third = auto()

class OtherDataClass:
    def __init__(
        self: Self,
        variable: str,
    ) -> None:
        self.AVariable = variable

class DataClass:
    ClassVariable: int = 0

    def __init__(self: Self) -> None:
        self.InstanceVariable: int = 1
        self.StringVariable: str = "hello, world!"
        self.FloatVariable: float = 1.337
        self.BoolVariable: bool = False
        self.ArrayVariable: List[OtherDataClass] = [
            OtherDataClass("foo"),
            OtherDataClass("bar"),
            OtherDataClass("baz"),
            OtherDataClass("bad"),
        ]
        self.EnumVariable: AnEnum = AnEnum.Option2
        self.IntEnumVariable: AnIntEnum = AnIntEnum.B
        self.FlagVariable: AFlag = AFlag.Second | AFlag.Third
        self.FileVariable: QFileInfo = QFileInfo()

    def anotherFunc(self: Self) -> None:
        pass

class NodeTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.node: Node = Node(value=DataClass(), name='Root')

    def testChildren(self: Self) -> None:
        firstChild: Node = self.node.children[0]

        self.assertEqual(firstChild.name, 'InstanceVariable')
        self.assertEqual(firstChild.path, 'Root.InstanceVariable')

    def testFromPath(self: Self) -> None:
        self.assertIsNone(self.node.fromPath('UnknownNode'))        
        instanceVariableNode: Node = self.node.fromPath('Root.InstanceVariable')
        self.assertIsNotNone(instanceVariableNode)
        self.assertEqual(instanceVariableNode.name, 'InstanceVariable')

        arrayElementNode: Node = self.node.fromPath('Root.ArrayVariable.[2].AVariable')
        self.assertEqual(arrayElementNode.value, 'baz')

    def testIntEnumVariable(self: Self) -> None:
        enumNode: Node = self.node.fromPath('Root.IntEnumVariable')
        self.assertTrue(enumNode.isEnum)
        self.assertFalse(enumNode.isFlag)
        self.assertFalse(enumNode.isObject)
        self.assertFalse(enumNode.isArray)
        self.assertFalse(enumNode.isFloat)
        self.assertFalse(enumNode.isInt)
        self.assertFalse(enumNode.isString)
        self.assertFalse(enumNode.isBool)
        self.assertFalse(enumNode.isFilePath)

    def testEnumVariable(self: Self) -> None:
        enumNode: Node = self.node.fromPath('Root.EnumVariable')
        self.assertTrue(enumNode.isEnum)
        self.assertFalse(enumNode.isFlag)
        self.assertFalse(enumNode.isObject)
        self.assertFalse(enumNode.isArray)
        self.assertFalse(enumNode.isFloat)
        self.assertFalse(enumNode.isInt)
        self.assertFalse(enumNode.isString)
        self.assertFalse(enumNode.isBool)
        self.assertFalse(enumNode.isFilePath)

    def testFlagVariable(self: Self) -> None:
        flagNode: Node = self.node.fromPath('Root.FlagVariable')
        self.assertTrue(flagNode.isFlag)
        self.assertFalse(flagNode.isEnum)
        self.assertFalse(flagNode.isObject)
        self.assertFalse(flagNode.isArray)
        self.assertFalse(flagNode.isFloat)
        self.assertFalse(flagNode.isInt)
        self.assertFalse(flagNode.isString)
        self.assertFalse(flagNode.isBool)
        self.assertFalse(flagNode.isFilePath)

    def testArrayVariable(self: Self) -> None:
        arrayNode: Node = self.node.fromPath('Root.ArrayVariable')
        self.assertTrue(arrayNode.isArray)
        self.assertFalse(arrayNode.isEnum)
        self.assertFalse(arrayNode.isFlag)
        self.assertFalse(arrayNode.isObject)
        self.assertFalse(arrayNode.isFloat)
        self.assertFalse(arrayNode.isInt)
        self.assertFalse(arrayNode.isString)
        self.assertFalse(arrayNode.isBool)
        self.assertFalse(arrayNode.isFilePath)

    def testObjectVariable(self: Self) -> None:
        objectNode: Node = self.node
        self.assertTrue(objectNode.isObject)
        self.assertFalse(objectNode.isEnum)
        self.assertFalse(objectNode.isFlag)
        self.assertFalse(objectNode.isArray)
        self.assertFalse(objectNode.isFloat)
        self.assertFalse(objectNode.isInt)
        self.assertFalse(objectNode.isString)
        self.assertFalse(objectNode.isBool)
        self.assertFalse(objectNode.isFilePath)

    def testFloatVariable(self: Self) -> None:
        node: Node = self.node.fromPath('Root.FloatVariable')
        self.assertFalse(node.isObject)
        self.assertFalse(node.isEnum)
        self.assertFalse(node.isFlag)
        self.assertFalse(node.isArray)
        self.assertTrue(node.isFloat)
        self.assertFalse(node.isInt)
        self.assertFalse(node.isString)
        self.assertFalse(node.isBool)
        self.assertFalse(node.isFilePath)

    def testIntVariable(self: Self) -> None:
        node: Node = self.node.fromPath('Root.InstanceVariable')
        self.assertFalse(node.isObject)
        self.assertFalse(node.isEnum)
        self.assertFalse(node.isFlag)
        self.assertFalse(node.isArray)
        self.assertFalse(node.isFloat)
        self.assertTrue(node.isInt)
        self.assertFalse(node.isString)
        self.assertFalse(node.isBool)
        self.assertFalse(node.isFilePath)

    def testStringVariable(self: Self) -> None:
        node: Node = self.node.fromPath('Root.StringVariable')
        self.assertFalse(node.isObject)
        self.assertFalse(node.isEnum)
        self.assertFalse(node.isFlag)
        self.assertFalse(node.isArray)
        self.assertFalse(node.isFloat)
        self.assertFalse(node.isInt)
        self.assertTrue(node.isString)
        self.assertFalse(node.isBool)
        self.assertFalse(node.isFilePath)

    def testBoolVariable(self: Self) -> None:
        node: Node = self.node.fromPath('Root.BoolVariable')
        self.assertFalse(node.isObject)
        self.assertFalse(node.isEnum)
        self.assertFalse(node.isFlag)
        self.assertFalse(node.isArray)
        self.assertFalse(node.isFloat)
        self.assertFalse(node.isInt)
        self.assertFalse(node.isString)
        self.assertTrue(node.isBool)
        self.assertFalse(node.isFilePath)

    def testFilePathVariable(self: Self) -> None:
        node: Node = self.node.fromPath('Root.FileVariable')
        self.assertFalse(node.isObject)
        self.assertFalse(node.isEnum)
        self.assertFalse(node.isFlag)
        self.assertFalse(node.isArray)
        self.assertFalse(node.isFloat)
        self.assertFalse(node.isInt)
        self.assertFalse(node.isString)
        self.assertFalse(node.isBool)
        self.assertTrue(node.isFilePath)

if __name__ == '__main__':
    main()

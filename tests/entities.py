import sys
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import (Collection,
                    Deque,
                    Dict,
                    FrozenSet,
                    List,
                    NewType,
                    Optional,
                    Set,
                    Tuple,
                    TypeVar,
                    Union,
                    Any)
from uuid import UUID
if sys.version_info >= (3, 9):
    from collections import Counter
else:
    from typing import Counter

from marshmallow import fields

from dataclasses_json import (DataClassJsonMixin, LetterCase, dataclass_json)
from dataclasses_json.cfg import config

A = TypeVar('A')
UUIDWrapper = NewType('UUIDWrapper', UUID)
UUIDWrapperWrapper = NewType('UUIDWrapperWrapper', UUIDWrapper)


@dataclass(frozen=True)
class DataClassWithDecimal(DataClassJsonMixin):
    x: Decimal


@dataclass(frozen=True)
class DataClassWithNewType(DataClassJsonMixin):
    id: UUIDWrapper


@dataclass(frozen=True)
class DataClassWithNestedNewType(DataClassJsonMixin):
    id: UUIDWrapperWrapper


@dataclass(frozen=True)
class DataClassWithList(DataClassJsonMixin):
    xs: List[int]


@dataclass(frozen=True)
class DataClassWithListBuiltin(DataClassJsonMixin):
    xs: list


@dataclass(frozen=True)
class DataClassWithListUnbound(DataClassJsonMixin):
    xs: List


@dataclass(frozen=True)
class DataClassWithListDefaultFactory(DataClassJsonMixin):
    xs: List[int] = field(default_factory=list)


@dataclass(frozen=True)
class DataClassWithListStr(DataClassJsonMixin):
    xs: List[str]


@dataclass(frozen=True)
class DataClassWithDict(DataClassJsonMixin):
    kvs: Dict[str, str]


@dataclass(frozen=True)
class DataClassWithDictBuiltin(DataClassJsonMixin):
    kvs: Dict


@dataclass(frozen=True)
class DataClassWithDictUnbound(DataClassJsonMixin):
    kvs: Dict


@dataclass(frozen=True)
class DataClassWithDictInt(DataClassJsonMixin):
    kvs: Dict[int, str]


@dataclass(frozen=True)
class DataClassWithDictDefaultFactory(DataClassJsonMixin):
    kvs: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DataClassWithSet(DataClassJsonMixin):
    xs: Set[int]


@dataclass(frozen=True)
class DataClassWithSetBuiltin(DataClassJsonMixin):
    xs: set


@dataclass(frozen=True)
class DataClassWithSetUnbound(DataClassJsonMixin):
    xs: Set


@dataclass(frozen=True)
class DataClassWithTuple(DataClassJsonMixin):
    xs: Tuple[int]


@dataclass(frozen=True)
class DataClassWithTupleBuiltin(DataClassJsonMixin):
    xs: tuple


@dataclass(frozen=True)
class DataClassWithTupleUnbound(DataClassJsonMixin):
    xs: Tuple


@dataclass(frozen=True)
class DataClassWithFrozenSet(DataClassJsonMixin):
    xs: FrozenSet[int]


@dataclass(frozen=True)
class DataClassWithFrozenSetBuiltin(DataClassJsonMixin):
    xs: frozenset


@dataclass(frozen=True)
class DataClassWithFrozenSetUnbound(DataClassJsonMixin):
    xs: FrozenSet


@dataclass(frozen=True)
class DataClassWithDeque(DataClassJsonMixin):
    xs: Deque[int]


@dataclass(frozen=True)
class DataClassWithDequeCollections(DataClassJsonMixin):
    xs: deque


@dataclass(frozen=True)
class DataClassWithDequeUnbound(DataClassJsonMixin):
    xs: Deque[int]


@dataclass(frozen=True)
class DataClassWithOptional(DataClassJsonMixin):
    x: Optional[int]


@dataclass(frozen=True)
class DataClassWithOptionalWithDefault(DataClassJsonMixin):
    x: Optional[int] = None


@dataclass(frozen=True)
class DataClassWithOptionalUnbound(DataClassJsonMixin):
    x: Optional


@dataclass
class DataClassWithOptionalStr(DataClassJsonMixin):
    x: Optional[str] = None


@dataclass(frozen=True)
class DataClassWithOptionalNested(DataClassJsonMixin):
    x: Optional[DataClassWithOptional]


@dataclass(frozen=True)
class DataClassWithOptionalNestedWithDefault(DataClassJsonMixin):
    x: Optional[DataClassWithOptional] = None


@dataclass(frozen=True)
class DataClassWithUnionIntNone(DataClassJsonMixin):
    x: Union[int, None]


@dataclass(frozen=True)
class DataClassWithDataClass(DataClassJsonMixin):
    dc_with_list: DataClassWithList


@dataclass(frozen=True)
class DataClassX(DataClassJsonMixin):
    x: int


@dataclass(frozen=True)
class DataClassXs(DataClassJsonMixin):
    xs: List[DataClassX]


@dataclass(frozen=True)
class DataClassIntImmutableDefault(DataClassJsonMixin):
    x: int = 0


@dataclass(frozen=True)
class DataClassBoolImmutableDefault(DataClassJsonMixin):
    x: bool = False


@dataclass(frozen=True)
class DataClassMutableDefaultList(DataClassJsonMixin):
    xs: List[int] = field(default_factory=list)


@dataclass(frozen=True)
class DataClassMutableDefaultDict(DataClassJsonMixin):
    xs: Dict[str, int] = field(default_factory=dict)


class MyCollection(Collection[A]):
    def __init__(self, xs: Collection[A]) -> None:
        self.xs = xs

    def __contains__(self, item):
        return False

    def __iter__(self):
        return iter(self.xs)

    def __len__(self):
        return len(self.xs)

    def __eq__(self, other):
        return type(self) == type(other) and self.xs == other.xs


@dataclass(frozen=True)
class DataClassWithMyCollection(DataClassJsonMixin):
    xs: MyCollection[int]


@dataclass_json
@dataclass
class DataClassJsonDecorator:
    x: str


@dataclass_json
@dataclass
class DataClassWithConfigManual:
    id: float = field(
        metadata={'dataclasses_json': {
            'mm_field': fields.Integer()
        }})


@dataclass_json
@dataclass
class DataClassWithConfigHelper:
    id: float = field(metadata=config(encoder=str))


@dataclass_json
@dataclass
class DataClassWithErroneousDecode:
    # Accepts no arguments, so passing in a single argument will result in a TypeError.
    id: float = field(metadata=config(decoder=lambda: None))


def split_str(data: str, *_args, **_kwargs):
    return data.split(',')


@dataclass_json
@dataclass
class DataClassDifferentTypeDecode:
    lst: List[str] = field(default=None, metadata=config(decoder=split_str))


@dataclass_json
@dataclass
class DataClassMappingBadDecode:
    map: Dict[str, DataClassWithErroneousDecode]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DataClassWithConfigDecorator:
    id_field: str


@dataclass_json
@dataclass
class DataClassWithUuid:
    id: UUID


@dataclass_json
@dataclass
class DataClassDefaultListStr:
    value: List[str] = field(default_factory=list)


@dataclass_json
@dataclass
class DataClassChild:
    name: str


@dataclass_json
@dataclass
class DataClassDefaultOptionalList:
    children: Optional[List[DataClassChild]] = None


@dataclass_json
@dataclass
class DataClassList:
    children: List[DataClassChild]


@dataclass_json
@dataclass
class DataClassOptional:
    a: int
    b: Optional[int]


@dataclass_json
@dataclass
class DataClassWithOptionalDatetime:
    a: Optional[datetime]


@dataclass_json
@dataclass
class DataClassWithOptionalDecimal:
    a: Optional[Decimal]


@dataclass_json
@dataclass
class DataClassWithOptionalUuid:
    a: Optional[UUID]


@dataclass_json
@dataclass
class DataClassWithNestedAny:
    a: Dict[str, Any]


@dataclass_json
@dataclass
class DataClassWithNestedOptionalAny:
    a: Dict[str, Optional[Any]]


@dataclass_json
@dataclass
class DataClassWithNestedOptional:
    a: Dict[str, Optional[int]]


@dataclass_json
@dataclass
class DataClassWithNestedDictWithTupleKeys:
    a: Dict[Tuple[int], int]


@dataclass_json
@dataclass
class DataClassWithCounter:
    c: Counter[str]

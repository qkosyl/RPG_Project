from typing import Dict, Any, Callable, Iterable

DataType = Iterable[Dict[str, Any]]
ModifierFunc = Callable[[DataType], DataType]


def query(data: DataType, selector: ModifierFunc,
          *filters: ModifierFunc) -> DataType:
    result = selector(data)

    for f in filters:
        result = f(result)
    print(result)
    return result
def select(*columns: str) -> ModifierFunc:
    def selector(data):
        result = []
        for x in data:
            new_row = {}
            for col in columns:
                if col in x:
                    new_row[col] = x[col]
            result.append(new_row)
        return result
    return selector


def field_filter(column: str, *values: Any) -> ModifierFunc:
    def filterFunc(data):
        result = []
        for row in data:
            if row[column] in values:
                result.append(row)
        return result
    return filterFunc
def test_query():
    friends = [
        {'name': 'Sam', 'gender': 'male', 'sport': 'Basketball'}
    ]
    value = query(
        friends,
        select(*('name', 'gender', 'sport')),
        field_filter(*('sport', *('Basketball', 'volleyball'))),
        field_filter(*('gender', *('male',))),
    )
    assert [{'gender': 'male', 'name': 'Sam', 'sport': 'Basketball'}] == value


if __name__ == "__main__":
    test_query()

enum=[
    [
        '****',
        '*  *',
        '*  *',
        '*  *',
        '****',
    ],
    [
        '   *',
        '   *',
        '   *',
        '   *',
        '   *',
    ],
    [
        '****',
        '   *',
        '****',
        '*   ',
        '****',
    ],
    [
        '****',
        '   *',
        '****',
        '   *',
        '****',
    ],
    [
        '*  *',
        '*  *',
        '****',
        '   *',
        '   *',
    ],
    [
        '****',
        '*   ',
        '****',
        '   *',
        '****',
    ],
    [
        '****',
        '*   ',
        '****',
        '*  *',
        '****',
    ],
    [
        '****',
        '   *',
        '   *',
        '   *',
        '   *',
    ],
    [
        '****',
        '*  *',
        '****',
        '*  *',
        '****',
    ],
    [
        '****',
        '*  *',
        '****',
        '   *',
        '****',
    ],
]
def concat(enum1: list, enum2: list):
    output = list()
    for i in range(len(enum1)):
        output.append(enum1[i] +' '+enum2[i])
    return output
_input = [int(_) for _ in input()]
result = enum[_input.pop(0)]
for num in _input :
    result = concat(result, enum[num])
print('\n'.join(result))
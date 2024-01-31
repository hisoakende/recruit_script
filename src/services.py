def serialize(data):
    serialized_data = _serialize_dict(data)
    return len(serialized_data).to_bytes(length=2, byteorder='big') + serialized_data


def deserialize(serialized_data: bytes) -> dict:
    if not serialized_data:
        return {}

    length = int.from_bytes(serialized_data[:2], byteorder='big', signed=False)
    if length != len(serialized_data) - 2:
        raise ValueError
    return _deserialize_dict(serialized_data[2:], length)


def _serialize_dict(data):
    serialized_data = b''
    for key, value in data.items():
        if type(value) == str:
            value = value.encode('utf-8')
            type_code = b'\x00'

        elif type(value) == int:
            value = _encode_leb128(value)
            type_code = b'\x01'

        elif type(value) == dict:
            value = _serialize_dict(value)
            type_code = b'\x02'

        else:
            raise ValueError

        key = key.encode('utf-8')

        key_length = len(key).to_bytes(length=2, byteorder='big')
        value_length = len(value).to_bytes(length=2, byteorder='big')

        serialized_data += key_length + value_length + type_code + key + value

    return serialized_data


def _deserialize_dict(serialized_data: bytes, length: int) -> dict:
    deserialized_data = {}
    offset = 0
    while offset < length:
        key_length = int.from_bytes(serialized_data[offset:offset + 2], byteorder='big')
        offset += 2

        value_length = int.from_bytes(serialized_data[offset:offset + 2], byteorder='big')
        offset += 2

        type_code = serialized_data[offset]
        offset += 1

        key = serialized_data[offset:offset + key_length].decode('utf-8')
        offset += key_length

        if type_code == 0:
            value = serialized_data[offset:offset + value_length].decode('utf-8')

        elif type_code == 1:
            value = _decode_leb128(serialized_data[offset:offset + value_length])

        elif type_code == 2:
            value = _deserialize_dict(serialized_data[offset:offset + value_length], value_length)

        else:
            raise ValueError
        print(key)
        deserialized_data[key] = value
        offset += value_length

    return deserialized_data


def _encode_leb128(value: int) -> bytes:
    result = b''
    while True:
        byte = value & 0x7F
        value >>= 7

        if value != 0:
            byte |= 0x80
        result += bytes([byte])

        if value == 0:
            break

    return result


def _decode_leb128(data: bytes) -> int:
    result = 0
    shift = 0
    for byte in data:
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            break

        shift += 7

    return result

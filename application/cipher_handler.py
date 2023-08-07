from dataclasses import dataclass, field, asdict
from itertools import count
import json
from typing import Union


class Buffer:
    buffer = []

    @staticmethod
    def add(value):
        Buffer.buffer.append(value)

    @staticmethod
    def delete_id_from_buffer(id_to_delete: str) -> None:
        if not Buffer.check_id_ok(id_to_delete):
            return
        Buffer.buffer.pop(int(id_to_delete)-1)

    @staticmethod
    def check_id_ok(id_nr: str) -> bool:
        try:
            id_nr = int(id_nr)
            if id_nr > len(Buffer.buffer) or id_nr < 1:
                raise InvalidIdNumber
            return True
        except ValueError:
            print(f"number {id_nr} can not be converted to number")
        except InvalidIdNumber:
            print(f"id number {id_nr} is not in buffer")
        return False

    @staticmethod
    def show_buffer() -> None:
        for idx, data_object in enumerate(Buffer.buffer, start=1 ):
            print(f"{idx} - {data_object.text} - {data_object.encryption_type}")

    @staticmethod
    def clear_buffer() -> None:
        Buffer.buffer.clear()

    @staticmethod
    def buffer_to_json() -> list[str]:
        result = []
        for data_object in Buffer.buffer:
            x = asdict(data_object)
            x = json.dumps(x)
            result.append(x)
        print(result)
        return result

    @staticmethod
    def buffer_from_json(read_file) -> None:
        if not Buffer.__check_read_file_ok(read_file):
            return
        Buffer.clear_buffer()
        for json_str in read_file:
            json_object = json.loads(json_str)
            Text(**json_object)

    @staticmethod
    def __check_read_file_ok(read_file: str) -> bool:
        try:
            for idx, line in enumerate(read_file, start=1):
                json.loads(line)
            return True
        except ValueError:
            print(f"input line {idx} from file is not json type")
        return False


@dataclass
class Text:
    text: str
    encryption_type: Union[str, None] = None
    encrypted: bool = False

    def __post_init__(self):
        Buffer.add(self)

    def __eq__(self, other):
        return self.text == other.text and self.encryption_type == other.encryption_type and \
               self.encrypted == other.encrypted

    def __hash__(self):
        return hash((self.text, self.encryption_type, self.encrypted))


class Cipher:
    @staticmethod
    def encrypt(data_object: Text, shift: str) -> None:
        result = ""
        shift = int(shift)
        for i in range(len(data_object.text)):
            char = data_object.text[i]
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            elif char == " ":
                result += char
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
        data_object.text = result
        data_object.encryption_type = f"ROT{str(shift)}"
        data_object.encrypted = True

    @staticmethod
    def decrypt(data_object: Text) -> None:
        result = ""
        shift = int(data_object.encryption_type[3:])
        for i in range(len(data_object.text)):
            char = data_object.text[i]
            if char.isupper():
                result += chr((ord(char) - shift - 65) % 26 + 65)
            elif char == " ":
                result += char
            else:
                result += chr((ord(char) - shift - 97) % 26 + 97)
        data_object.text = result
        data_object.encryption_type = None
        data_object.encrypted = False

    @staticmethod
    def encrypt_to_rot_shift(shift: str, id_nr: str) -> None:
        if not (Buffer.check_id_ok(id_nr) and Cipher.__check_encryption_shift_ok(shift)):
            return
        data_object = Buffer.buffer[int(id_nr)-1]
        if not data_object.encrypted:
            Cipher.encrypt(data_object=data_object, shift=shift)
        elif data_object.encrypted:
            print("sentence already encrypted")

    @staticmethod
    def decrypt_from_rot_shift(id_nr: str) -> None:
        if not Buffer.check_id_ok(id_nr):
            return
        data_object = Buffer.buffer[int(id_nr)-1]
        if data_object.encrypted:
            Cipher.decrypt(data_object)
        elif not data_object.encrypted:
            print("sentence already decrypted")

    @staticmethod
    def __check_encryption_shift_ok(shift: str) -> bool:
        try:
            shift = int(shift)
            if shift < 0:
                raise ValueError
            return True
        except ValueError:
            print(f"number {shift} can not be converted to number or is not greater/equal than 1")
        return False




class InvalidIdNumber(Exception):
    pass



"""
Cipher("hello moto")
Cipher("good day")
Cipher("my mutter is computer")

print(buffer)
"""



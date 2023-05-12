from dataclasses import dataclass, field, asdict
from itertools import count
import json
from typing import Union



buffer = []


@dataclass
class Cipher:

    text: str
    encryption_type: Union[str, None] = None
    encrypted: bool = False
    id: int = field(default_factory=count(1).__next__, init=True)

    def __post_init__(self):
        buffer.append(self)

    @classmethod
    def delete_id_from_buffer(cls, id_to_delete: str) -> None:
        if not cls.check_id_ok(id_to_delete):
            return
        for data_object in buffer:
            if data_object.id == int(id_to_delete):
                buffer.remove(data_object)
                break

    @classmethod
    def show_buffer(cls) -> None:
        for data_object in buffer:
            print(f"{data_object.id} - {data_object.text} - {data_object.encryption_type}")

    @staticmethod
    def encrypt_to_rot_shift(shift: str, id_nr: str) -> None:
        if not (Buffer.check_id_ok(id_nr) and Cipher.__check_encryption_shift_ok(shift)):
            return
        result = ""
        s = int(s)
        for data_object in buffer:
            if data_object.id == int(id_nr) and not data_object.encrypted:
                for i in range(len(data_object.text)):
                    char = data_object.text[i]
                    if char.isupper():
                        result += chr((ord(char) + s - 65) % 26 + 65)
                    elif char == " ":
                        result += char
                    else:
                        result += chr((ord(char) + s - 97) % 26 + 97)
                data_object.text = result
                data_object.encryption_type = "ROT" + str(s)
                data_object.encrypted = True
                break
            elif data_object.id == int(id_nr) and data_object.encrypted:
                print("sentence already encrypted")
                break

    @staticmethod
    def decrypt_from_rot_shift(id_nr: str) -> None:
        result = ""
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



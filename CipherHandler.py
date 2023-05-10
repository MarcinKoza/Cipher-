from dataclasses import dataclass, field, asdict
from itertools import count
import json


buffer = []

@dataclass
class Cipher:

    text: str
    encryption_type: str = None
    encrypted: bool = False
    id: int = field(default_factory=count(1).__next__, init=False)


    def __post_init__(self):
        buffer.append(self)

    @classmethod
    def delete_id_from_buffer(cls, id_to_delete):
        if not cls.check_id_ok(id_to_delete):
            return
        for data_object in buffer:
            if data_object.id == int(id_to_delete):
                buffer.remove(data_object)
                break

    @classmethod
    def show_buffer(cls):
        for data_object in buffer:
            print(f"{data_object.id} - {data_object.text} - {data_object.encryption_type}")

    @classmethod
    def encrypt_to_rot_shift(cls, s: str, id_nr: str):
        if not (cls.check_id_ok(id_nr) and cls.check_encryption_ok(s)):
            print("nie ok",cls.check_id_ok(id_nr),cls.check_encryption_ok(s))
            return
        result = ""
        s = int(s)
        for data_object in buffer:
            if data_object.id == int(id_nr):
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

    @classmethod
    def decrypt_from_rot_shift(cls, id_nr: str):
        result = ""
        if not cls.check_id_ok(id_nr):
            return
        for data_object in buffer:
            if data_object.id == int(id_nr):
                s = int(data_object.encryption_type[3:])
                for i in range(len(data_object.text)):
                    char = data_object.text[i]
                    if char.isupper():
                        result += chr((ord(char) - s - 65) % 26 + 65)
                    elif char == " ":
                        result += char
                    else:
                        result += chr((ord(char) - s - 97) % 26 + 97)
                data_object.text = result
                data_object.encryption_type = None
                data_object.encrypted = False
                break


    @classmethod
    def clear_buffer(cls):
        buffer.clear()

    @classmethod
    def buffer_to_json(cls):
        result = []
        for data_object in buffer:
            x = asdict(data_object)
            del x["id"]
            x = json.dumps(x)
            result.append(x)
        return result

    @classmethod
    def buffer_from_json(cls, read_file):
        if not cls.check_read_file_ok(read_file):
            return
        cls.clear_buffer()
        for json_str in read_file:
            json_object = json.loads(json_str)
            Cipher(**json_object)

    @classmethod
    def check_id_ok(cls, id_nr: str) -> bool:
        try:
            id_nr = int(id_nr)
            for data_object in buffer:
                if data_object.id == id_nr:
                    break
            else:
                raise InvalidIdNumber
            return True
        except ValueError:
            print(f"number {id_nr} can not be converted to number")
        except InvalidIdNumber:
            print(f"id number {id_nr} is not in buffer")
        return False

    @classmethod
    def check_encryption_ok(cls, s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            print(f"number {s} can not be converted to number")
        return False

    @classmethod
    def check_read_file_ok(cls, read_file: str) -> bool:
        try:
            for idx, line in enumerate(read_file, start=1):
                json.loads(line)
            return True
        except ValueError:
            print(f"input line {idx} from file is not json type")
        return False


class InvalidIdNumber(Exception):
    pass






from typing import Union


class FileHandler:
    not_permitted = ["\"", "/", "\\", "<", ">", "?", ":", "*", "|"]
    save_directory = "saves/"

    @classmethod
    def read_json_from_file(cls, file_name: str) -> Union[list[str], None]:
        result = []
        if not cls.check_file_name_ok(file_name):
            return None
        try:
            with open(cls.save_directory + file_name + ".txt", "r") as file:
                for line in file:
                    result.append(line)
        except FileNotFoundError:
            print(f"File {file_name} does not exist")
            return None
        return result

    @classmethod
    def write_json_to_file(cls, file_name: str, data: list[dict]) -> Union[list[str], None]:
        if not cls.check_file_name_ok(file_name):
            return None
        for json in data:
            with open(cls.save_directory + file_name + ".txt", "a") as file:
                file.write(f'{json}\n')

    @classmethod
    def check_file_name_ok(cls, file_name: str) -> bool:
        try:
            if len(file_name) > 250:
                raise ValueError
            for sign in file_name:
                if sign in cls.not_permitted:
                    raise TypeError
            return True
        except ValueError:
            print(f"File {file_name} is too long")
        except TypeError:
            print(f"File {file_name} contains of not permitted chars {cls.not_permitted}")
        return False



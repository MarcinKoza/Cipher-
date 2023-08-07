from typing import Union


class FileHandler:
    NOT_PERMITTED = ('"', "/", "\\", "<", ">", "?", ":", "*", "|")
    SAVE_DIRECTORY = "saves/"

    @classmethod
    def read_json_from_file(cls, file_name: str) -> Union[list[str], None]:
        result = []
        if not cls.__validate_file_name(file_name):
            return None
        try:
            with open(cls.SAVE_DIRECTORY + file_name + ".txt", "r") as file:
                for line in file:
                    result.append(line)
        except FileNotFoundError:
            print(f"File {file_name} does not exist")
            return None
        return result

    @classmethod
    def write_json_to_file(
        cls, file_name: str, data: list[str]
    ) -> Union[list[str], None]:
        if not cls.__validate_file_name(file_name):
            return None
        for json in data:
            with open(cls.SAVE_DIRECTORY + file_name + ".txt", "a") as file:
                file.write(f"{json}\n")

    @staticmethod
    def has_forbidden_chars(file_name: str) -> bool:
        return any([sign for sign in file_name if sign in FileHandler.NOT_PERMITTED])

    @classmethod
    def __validate_file_name(cls, file_name: str) -> bool:
        try:
            if len(file_name) > 250:
                raise FileNameTooLongError
            if cls.has_forbidden_chars(file_name):
                raise NotPermittedCharsError
            return True
        except FileNameTooLongError:
            print(f"File {file_name} is too long")
        except NotPermittedCharsError:
            print(
                f"File {file_name} contains of not permitted chars {cls.NOT_PERMITTED}"
            )
        return False


class FileNameTooLongError(ValueError):
    pass


class NotPermittedCharsError(TypeError):
    pass
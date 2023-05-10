from Menu import Menu
from CipherHandler import Cipher
from FileHandler import FileHandler
import sys


class Manager:

    def __init__(self) -> None:
        self.menu = Menu()
        print("Program intialization...")

    def quit_program(self) -> None:
        sys.exit("Exiting the program ...")

    def read_command(self) -> str:
        command = input()
        return command

    def run_command(self, command: str) -> None:
        match command.split():
            case ["help"]:
                self.menu.hlp()
            case ["quit"]:
                self.quit_program()
            case ["print_buffer"]:
                Cipher.show_buffer()
            case ["new_sentence", *text]:
                text = " ".join(text)
                Cipher(text)
            case ["del_sentence", text]:
                id_number = text
                Cipher.delete_id_from_buffer(id_number)
            case ["encrypt_sentence", encryption_type, id_number]:
                print(encryption_type,"---", id_number)
                Cipher.encrypt_to_rot_shift(encryption_type, id_number)
            case ["decrypt_sentence", id_number]:
                Cipher.decrypt_from_rot_shift(id_number)
            case ["save_to_file", filename]:
                FileHandler.write_json_to_file(filename, Cipher.buffer_to_json())
            case ["read_from_file", filename]:
                Cipher.buffer_from_json(FileHandler.read_json_from_file(filename))
            case _:
                print(f"Sorry, I couldn't understand {command!r}")


    def start_program(self) -> None:
        print("Your program is started type \"help\" for available commands")
        while True:
            self.run_command(self.read_command())
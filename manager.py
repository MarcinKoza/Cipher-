from menu import Menu
from application.cipher_handler import Cipher, Buffer, Text
from application.file_handler import FileHandler
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
                Buffer.show_buffer()
            case ["new_sentence", *text]:
                text = " ".join(text)
                Text(text)
            case ["del_sentence", text]:
                id_number = text
                Buffer.delete_id_from_buffer(id_number)
            case ["encrypt_sentence", encryption_type, id_number]:
                print(f"processing encrypting ROT{encryption_type} on sentence {id_number}")
                Cipher.encrypt_to_rot_shift(encryption_type, id_number)
            case ["decrypt_sentence", id_number]:
                Cipher.decrypt_from_rot_shift(id_number)
            case ["save_to_file", filename]:
                FileHandler.write_json_to_file(filename, Buffer.buffer_to_json())
            case ["read_from_file", filename]:
                Buffer.buffer_from_json(FileHandler.read_json_from_file(filename))
            case _:
                print(f"Sorry, I couldn't understand {command!r}")

    def start_program(self) -> None:
        print("Your program is started type \"help\" for available commands")
        while True:
            self.run_command(self.read_command())

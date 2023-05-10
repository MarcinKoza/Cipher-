class Menu:
    menu_commands = {"new_sentence": "add new sentence",
                     "del_sentence <sentence identifier>": "delete sentence",
                     "encrypt_sentence <ROT13/ROT37> <sentence identifier>": "encrypt existing sentence",
                     "decrypt_sentence <sentence identifier>": "decrypt existing sentence",
                     "print_buffer": "print buffer",
                     "save_to_file <file_name>": "saving whole buffer to file",
                     "read_from_file <file_name>": "reading whole buffer to file",
                     "quit": "exit"}

    def hlp(self) -> None:
        for menu_cmd, menu_desc in self.menu_commands.items():
            print(f"{menu_cmd} - {menu_desc}")



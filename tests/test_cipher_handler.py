import json
from application.cipher_handler import Cipher, Buffer, Text
from unittest.mock import Mock, patch


create_temp_buffer_inst_str = """Text('hello motor biker', None, False)\n
                                Text('good day to all people', None, False)\n
                                Text('my mutter is not computer', None, False)\n""".replace('  ', '')
create_temp_buffer_cmd = compile(create_temp_buffer_inst_str, 'sumstring', 'exec')


class TestBufferAdd:
    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()

    def test_should_add__elements_to_the_buffer(self):
        exec(create_temp_buffer_cmd)
        assert len(Buffer.buffer) == 3
        exec(create_temp_buffer_cmd)
        assert len(Buffer.buffer) == 6


class TestBufferDeleteIdFromBuffer:
    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()
        exec(create_temp_buffer_cmd)

    @pytest.mark.parametrize('test_input', ['2', '3'])
    def test_should_delete_correct_elements_from_buffer(self, test_input):
        del_object = Buffer.buffer[int(test_input)-1]
        Buffer.delete_id_from_buffer(test_input)
        assert len(Buffer.buffer) == 2
        assert not any([True for text_object in Buffer.buffer if text_object == del_object])

    @pytest.mark.parametrize('test_input', ['4', '0'])
    def test_should_not_delete_elements_from_buffer(self, test_input):
        Buffer.delete_id_from_buffer(test_input)
        assert len(Buffer.buffer) == 3


class TestBufferBufferToJson:
    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()
        exec(create_temp_buffer_cmd)

    def test_should_convert_all_elements_to_dict_list(self):
        assert len(Buffer.buffer_to_json()) == 3
        try:
            assert len([json.loads(dict_object) for dict_object in Buffer.buffer_to_json()]) == 3
        except json.JSONDecodeError:
            pytest.fail()


class TestBufferBufferFromJson:
    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()
        exec(create_temp_buffer_cmd)

    def test_should_read_buffer_from_json_list(self):
        result_buffer_json = Buffer.buffer_to_json()
        result = Buffer.buffer.copy()
        Buffer.clear_buffer()
        assert len(Buffer.buffer) == 0
        Buffer.buffer_from_json(result_buffer_json)
        assert len(Buffer.buffer) == 3
        for start_object, loaded_object in zip(result, Buffer.buffer):
            assert start_object == loaded_object

    @pytest.mark.parametrize('row_number, failing_test_string', [('0', 'a'), ('2', "")])
    def test_should_not_read_buffer_from_json_list(self,row_number, failing_test_string):
        result_buffer_json = Buffer.buffer_to_json()
        result_buffer_json[int(row_number)] = failing_test_string
        Buffer.clear_buffer()
        assert len(Buffer.buffer) == 0
        Buffer.buffer_from_json(result_buffer_json)
        assert len(Buffer.buffer) == 0


class TestCipherEncryptToRotShift(TestWithBuffer):
    def setup_method(self):
        super().setup_method()
        # exec(create_temp_buffer_cmd)

    @pytest.mark.parametrize('shift, id_nr, result', [('13', '1', "uryyb zbgbe ovxre"),
                                                      ('47', "2", "bjjy yvt oj vgg kzjkgz")])
    def test_should_encrypt_sentence_in_buffer(self, shift, id_nr, result):
        Cipher.encrypt_to_rot_shift(shift, id_nr)
        assert Buffer.buffer[int(id_nr)-1].text == result

    def test_should_not_encrypt_sentence_second_time(self):
        Cipher.encrypt_to_rot_shift("13", "1")
        Cipher.encrypt_to_rot_shift("13", "1")
        assert Buffer.buffer[0].text == "uryyb zbgbe ovxre"

    @pytest.mark.parametrize('shift, id_nr', [('a', '1'), ('', "2"), ('13', "2a"), ('47', "")])
    def test_should_not_encrypt_any_sentence_when_inputs_incorrect(self, shift, id_nr):
        result = Buffer.buffer.copy()
        Cipher.encrypt_to_rot_shift(shift, id_nr)
        assert Buffer.buffer == result


class TestCipherDecryptFromRotShift(TestWithBuffer):

    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()
        exec(create_temp_buffer_cmd)
        Cipher.encrypt_to_rot_shift("13", "1")

    def test_should_decrypt_sentence_from_buffer(self):
        Cipher.decrypt_from_rot_shift("1")
        assert Buffer.buffer[0].text == "hello motor biker"

    def test_should_not_decrypt_sentence_second_time(self):
        Cipher.decrypt_from_rot_shift("1")
        Cipher.decrypt_from_rot_shift("1")
        assert Buffer.buffer[0].text == "hello motor biker"

    @pytest.mark.parametrize('id_nr', ['a', ""])
    def test_should_not_decrypt_sentence_when_inputs_incorrect(self, id_nr):
        result = Buffer.buffer.copy()
        Cipher.decrypt_from_rot_shift(id_nr)
        assert Buffer.buffer == result

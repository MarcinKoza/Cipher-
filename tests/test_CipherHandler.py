import pytest, json
from CipherHandler import Cipher, Buffer, Text
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


class TestCipherHandlerDeleteIdFromBuffer:
    result_buffer0 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n','')\
        .replace('  ', '')
    result_buffer1 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n','')\
        .replace('  ', '')
    result_buffer2 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2)]""".replace('\n','')\
        .replace('  ', '')

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


class TestBufferBufferBromJson:
    @staticmethod
    def setup_method(self):
        Buffer.clear_buffer()
        exec(create_temp_buffer_cmd)

    def test_should_read_buffer_from_json_list(self):
        result_buffer_json = Buffer.buffer_to_json()
        result = Buffer.buffer
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




class TestCipherEncryptToRotShift:
    result_buffer0 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n','')\
        .replace('  ', '')
    result_buffer1 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='tbbq qnl gb nyy crbcyr', encryption_type='ROT13', encrypted=True, id=2), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n', '')\
        .replace('  ', '')
    result_buffer2 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2), 
    Cipher(text='ht hpoozm dn ijo xjhkpozm', encryption_type='ROT47', encrypted=True, id=3)]""".replace('\n', '')\
        .replace('  ', '')

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_result',
                             [('13', '2', result_buffer1),
                              ('47', '3', result_buffer2)])
    def test_should_encrypt_correct_elements_from_buffer(self, test_input_rot_shift, test_input_rot_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_result',
                             [('13a', '2', result_buffer0),
                              ('', '3', result_buffer0),
                              ('47', '3a', result_buffer0),
                              ('47', '', result_buffer0)])
    def test_should_not_encrypt_any_elements_from_buffer_if_values_not_int_convertable(self, test_input_rot_shift,
                                                                                       test_input_rot_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_result',
                             [('13', '0', result_buffer0),
                              ('47', '4', result_buffer0)])
    def test_should_not_encrypt_any_elements_from_buffer_if_id_value_out_of_range(self, test_input_rot_shift,
                                                                                  test_input_rot_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_result',
                             [('13', '2', result_buffer1),
                              ('47', '3', result_buffer2)])
    def test_should_not_encrypt_any_elements_from_buffer_if_encrypted_is_true(self, test_input_rot_shift,
                                                                              test_input_rot_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.clear_buffer()



class TestCipherDecryptFromRotShift:
    result_buffer0 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n','')\
        .replace('  ', '')
    result_buffer1 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='tbbq qnl gb nyy crbcyr', encryption_type='ROT13', encrypted=True, id=2), 
    Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)]""".replace('\n', '')\
        .replace('  ', '')
    result_buffer2 = """[Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1), 
    Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2), 
    Cipher(text='ht hpoozm dn ijo xjhkpozm', encryption_type='ROT47', encrypted=True, id=3)]""".replace('\n', '')\
        .replace('  ', '')

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_result',
                             [('13', '2', result_buffer1),
                              ('47', '3', result_buffer2)])
    def test_should_decrypt_correct_elements_from_buffer(self, test_input_rot_shift, test_input_rot_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.decrypt_from_rot_shift(test_input_rot_id)
        assert str(buffer) == self.result_buffer0
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_input_dec_id, test_result',
                           [('13', '2', '4', result_buffer1),
                            ('47', '3', '0', result_buffer2),
                            ('47', '3', 'a', result_buffer2),
                            ('47', '3', '',  result_buffer2)])
    def test_should_not_decrypt_any_elem_with_incorrect_id(self, test_input_rot_shift,test_input_rot_id,
                                                           test_input_dec_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.decrypt_from_rot_shift(test_input_dec_id)
        assert str(buffer) == test_result
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input_rot_shift,test_input_rot_id, test_input_dec_id, test_result',
                           [('13', '2', '2', result_buffer1),
                            ('47', '3', '3', result_buffer2)])
    def test_should_not_decrypt_any_elem_when_already_decrypted(self, test_input_rot_shift, test_input_rot_id,
                                                                test_input_dec_id, test_result):
        exec(code_temp_buffer)
        Cipher.encrypt_to_rot_shift(test_input_rot_shift, test_input_rot_id)
        assert str(buffer) == test_result
        Cipher.decrypt_from_rot_shift(test_input_dec_id)
        Cipher.decrypt_from_rot_shift(test_input_dec_id)
        assert str(buffer) == self.result_buffer0
        Cipher.clear_buffer()
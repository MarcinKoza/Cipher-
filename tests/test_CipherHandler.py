import pytest
from CipherHandler import Cipher, buffer
from unittest.mock import Mock, patch

create_temp_buffer_int_str = """Cipher(text='hello motor biker', encryption_type=None, encrypted=False, id=1)\n
                                Cipher(text='good day to all people', encryption_type=None, encrypted=False, id=2)\n
                                Cipher(text='my mutter is not computer', encryption_type=None, encrypted=False, id=3)\n
                             """.replace('  ','')

code_temp_buffer = compile(create_temp_buffer_int_str, 'sumstring', 'exec')


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

    @pytest.mark.parametrize('test_input, test_result', [('2', result_buffer1),
                                                         ('3', result_buffer2)])
    def test_should_delete_correct_elements_from_buffer(self, test_input, test_result):
        exec(code_temp_buffer)
        Cipher.delete_id_from_buffer(test_input)
        assert str(buffer) == test_result
        Cipher.clear_buffer()

    @pytest.mark.parametrize('test_input, test_result', [('4', result_buffer0),
                                                         ('0', result_buffer0)])
    def test_should_not_delete_elements_from_buffer(self, test_input, test_result):
        exec(code_temp_buffer)
        Cipher.delete_id_from_buffer(test_input)
        assert str(buffer) == test_result
        Cipher.clear_buffer()


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
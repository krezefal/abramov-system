import sys
import unittest
import logging

from abramov_system.keygen import generate_abramov_keypair
from abramov_system.utils import is_number, is_zero


class TestMath(unittest.TestCase):
    reference_base = 9
    reference_degree = 8

    @classmethod
    def setUpClass(cls):  # Keypair will be generated once for all these test cases
        cls.log = logging.getLogger("TestMath")
        cls.private_key, cls.public_key = \
            generate_abramov_keypair(cls.reference_base, cls.reference_degree)

        cls.test_number1 = 197
        cls.test_number2 = 27

        cls.encrypted_number1 = cls.public_key.encrypt(cls.test_number1)
        cls.encrypted_number2 = cls.public_key.encrypt(cls.test_number2)

    def test_addition(self):
        addition_result = self.test_number1 + self.test_number2
        enc_addition_result = self.encrypted_number1 + self.encrypted_number2
        dec_addition_result = self.private_key.decrypt(enc_addition_result)

        self.log.debug(f"\nAddition result: {addition_result}\n")
        self.log.debug(f"\nDecrypted result: {dec_addition_result}\n")

        self.assertEqual(addition_result, dec_addition_result)

    def test_subtraction(self):
        subtraction_result = self.test_number1 - self.test_number2
        enc_subtraction_result = self.encrypted_number1 - self.encrypted_number2
        dec_subtraction_result = self.private_key.decrypt(enc_subtraction_result)

        self.log.debug(f"\nSubtraction result: {subtraction_result}\n")
        self.log.debug(f"\nDecrypted result: {dec_subtraction_result}\n")

        self.assertEqual(subtraction_result, dec_subtraction_result)

    def test_multiplication(self):
        multiplication_result = self.test_number1 * self.test_number2
        enc_multiplication_result = self.encrypted_number1 * self.encrypted_number2
        dec_multiplication_result = self.private_key.decrypt(enc_multiplication_result)

        self.log.debug(f"\nMultiplication result: {multiplication_result}\n")
        self.log.debug(f"\nDecrypted result: {dec_multiplication_result}\n")

        self.assertEqual(multiplication_result, dec_multiplication_result)

    def test_division(self):
        if is_zero(self.encrypted_number2):
            raise ZeroDivisionError()

        division_result = self.test_number1 / self.test_number2
        enc_q, enc_r = self.encrypted_number1 / self.encrypted_number2

        dec_q = self.private_key.decrypt(enc_q)
        dec_r = self.private_key.decrypt(enc_r)
        dec_num2 = self.private_key.decrypt(self.encrypted_number2)

        if is_number(self.encrypted_number1) and is_number(self.encrypted_number2):
            self.log.debug(f"\nDivision result: {division_result}\n")
            self.log.debug(f"\nDecrypted result: {dec_q}\n")
            self.assertEqual(round(division_result, 10), round(dec_q, 10))  # ROUNDING!
            return

        dec_division_result = dec_q + dec_r / dec_num2

        self.log.debug(f"\nDivision result: {division_result}\n")
        self.log.debug(f"\nDecrypted result: {dec_division_result}\n")

        self.assertEqual(round(division_result, 10), round(dec_division_result, 10))


if __name__ == '__main__':
    # Change logging level from DEBUG to INFO to see less details
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)

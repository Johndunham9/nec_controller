import unittest
from nec_controller import calculate_bcc, convert_to_ascii, volume_four_byte_calculator


class TestUnit(unittest.TestCase):
    # Unit tests for controller helper functions
    def test_calculate_bcc(self):
        """Unit test for calculate BCC function"""
        hex_array = [0x30, 0x41, 0x30, 0x45, 0x30, 0x41, 0x02, 0x30, 0x30, 0x31, 0x30, 0x30, 0x30, 0x36, 0x34, 0x03]
        self.assertEqual(calculate_bcc(hex_array), 119)

    def test_convert_to_ascii(self):
        """Unit test for convert to ascii function"""
        hex_array = [0x30, 0x41, 0x30, 0x45, 0x30, 0x41, 0x02, 0x30, 0x30, 0x31, 0x30, 0x30, 0x30, 0x36, 0x34, 0x03, 0x77, 0x0D]
        self.assertEqual(convert_to_ascii(hex_array), '0A0E0A\x0200100064\x03w\r')

    def test_volume_four_byte_calculator(self):
        """Unit test for volume control function"""
        self.assertEqual(volume_four_byte_calculator(1), [48, 48, 48, 49])
        self.assertEqual(volume_four_byte_calculator(80), [48, 48, 53, 48])
        self.assertEqual(volume_four_byte_calculator(100), [48, 48, 54, 52])


if __name__ == '__main__':
    unittest.main()

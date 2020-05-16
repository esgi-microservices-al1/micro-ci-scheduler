import unittest

from dtos.IntervalDto import IntervalDto


class TestIntervalDto(unittest.TestCase):
    def test_deserialize(self):
        interval_data = {
            'unity': 'WEEK',
            'frequency': '2'
        }

        sut = IntervalDto.deserialize(interval_data)
        interval_dto = IntervalDto('WEEK', '2')
        self.assertEqual(sut, interval_dto)


if __name__ == '__main__':
    unittest.main()

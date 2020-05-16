import unittest

from bson import ObjectId

from dtos.IntervalDto import IntervalDto
from dtos.ScheduleDto import ScheduleDto


class ScheduleDtoTest(unittest.TestCase):
    def test_deserialize(self):
        schedule_data = {
            '_id': ObjectId('5eb5c7d28e1a208312c961bd'),
            'name': 'schedule name',
            'project': 'project name',
            'branch': 'branch name',
            'interval': {
                'unity': 'DAY',
                'frequency': '2'
            },
            'startDate': '2020-05-16T21:35:28'
        }
        sut = ScheduleDto.deserialize(schedule_data)
        schedule_dto = ScheduleDto('5eb5c7d28e1a208312c961bd', 'schedule name', 'project name',
                                   'branch name', IntervalDto('DAY', '2'), '2020-05-16T21:35:28')

        self.assertEqual(sut, schedule_dto)

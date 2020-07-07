import os
import platform

from crontab import CronTab
import json

from dtos.BuildMessageDto import BuildMessageDto

crontab_file = '/etc/crontab'


def isTestLaunched():
    return os.getenv('TESTING') is not None and os.environ['TESTING'] == "True"


class CrontabWriter:
    @staticmethod
    def add_schedule(schedule, id):
        if platform.system() != 'Linux' or isTestLaunched():
            print('crontab edit only works on UNIX systems')
            return

        cron = CronTab(user='root', tabfile=crontab_file)

        message = BuildMessageDto(project=schedule.project, branch=schedule.branch)
        message = json.dumps(message.__dict__, sort_keys=True, indent=4)

        # TODO jsonify this message
        job = cron.new(command='root . ' + os.environ['SCRIPTS_PATH'] +
                               '/build_order.env;' + ' python ' +
                               os.environ['SCRIPTS_PATH'] + '/build_order.py --message "\"' + message +'\""', comment=id)
        job = CrontabWriter.translate_schedule(schedule, job)
        if job.is_valid():
            cron.write()
        else:
            print('Invalid schedule : ' + str(schedule))
            return False
        return True

    @staticmethod
    def translate_schedule(schedule, job):
        job.minute.every(1)
        if schedule.interval.unity == 'DAY':
            job.day.every(schedule.interval.frequency)
        elif schedule.interval.unity == 'MONTH':
            job.month.every(schedule.interval.frequency)
        elif schedule.interval.unity == 'WEEK':
            if schedule.interval.frequency == 2:
                job.day.on(1, 15)
            else:
                # impossible de faire mieux, cron ne prend pas en charge 'every x weeks'
                job.dow.on('SUN')
        elif schedule.interval.unity == 'HOUR':
            job.hour.every(schedule.interval.frequency)
        elif schedule.interval.unity == 'MINUTE':
            job.minute.every(schedule.interval.frequency)
        return job

    @staticmethod
    def update_schedule(old_schedule, old_id, new_schedule=None, new_id=None):
        if platform.system() != 'Linux' or isTestLaunched():
            print('crontab edit only works on UNIX systems')
            return
        cron = CronTab(user='root', tabfile=crontab_file)
        old_job = cron.find_comment(old_id)
        cron.remove(old_job)
        cron.write()
        if new_schedule is not None and new_id is not None:
            CrontabWriter.add_schedule(new_schedule, new_id)

# class CrontabWriter:
#     @staticmethod
#     def add_schedule(schedule):
#         cron = open('/etc/crontab', 'r+')
#         print('opened /etc/crontab, content :' + str(cron.readlines()))
#         cron.write('\n')
#         cron.write(CrontabWriter.schedule_to_cron(schedule))
#         print('wrote : ' + CrontabWriter.schedule_to_cron(schedule) +
#               ' to /etc/crontab')
#         print('new /etc/crontab content : ' + str(cron.readlines()))
#         cron.close()
#
#     @staticmethod
#     def schedule_to_cron(schedule):
#         interval = '* *\t* * * '
#         if schedule.interval.unity == 'DAY':
#             interval = '0 0\t*/' + str(schedule.interval.frequency) + ' * * *'
#         elif schedule.interval.unity == 'MONTH':
#             interval = '0 0\t1 */' + str(schedule.interval.frequency) + ' *'
#         elif schedule.interval.unity == 'WEEK':
#             if str(schedule.interval.frequency) == 2:
#                 interval = '0 0\t1,15 * 0'
#             else:
#                 #impossible de faire mieux, cron ne prend pas en charge 'every x weeks'
#                 interval = '0 0\t* * 0'
#         elif schedule.interval.unity == 'HOUR':
#             interval = '0 */' + str(schedule.interval.frequency) + '\t* * *'
#         elif schedule.interval.unity == 'MINUTE':
#             interval = '*/' + schedule.interval.unity + ' *\t* * *'
#         command = ' root python ' + os.environ['API_LOCAL_PATH'] +
#                   '/scripts/build_order.py --message build:' +
#                   schedule.name + ':' + schedule.branch
#         return interval + command
#
#     @staticmethod
#     def update_schedule(old_schedule, new_schedule=None):
#         try:
#             cron_read = open('/etc/crontab', 'r')
#         except FileNotFoundError:
#             print('Can\'t find /etc/crontab')
#             return
#         lines = cron_read.readlines()
#         cron_read.close()
#         cron_write = open('/etc/crontab', 'w')
#         for line in lines:
#             if line.strip('\n') != CrontabWriter.schedule_to_cron(old_schedule):
#                 cron_write.write(line)
#         if new_schedule is not None:
#             cron_write.write('\n')
#             cron_write.write(CrontabWriter.schedule_to_cron(new_schedule))
#         cron_write.close()

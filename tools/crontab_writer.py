import os


class CrontabWriter:
    @staticmethod
    def add_schedule(schedule):
        try:
            cron = open('/etc/crontab', 'a')
        except FileNotFoundError:
            print('Can\'t find /etc/crontab')
            return
        cron.write('\n')
        cron.write(CrontabWriter.schedule_to_cron(schedule))
        cron.close()

    @staticmethod
    def schedule_to_cron(schedule):
        interval = '* *\t* * * '
        if schedule.interval.unity == 'DAY':
            interval = '0 0\t*/' + schedule.interval.frequency + ' * * *'
        elif schedule.interval.unity == 'MONTH':
            interval = '0 0\t1 */' + schedule.interval.frequency + ' *'
        elif schedule.interval.unity == 'WEEK':
            if schedule.interval.frequency == 2:
                interval = '0 0\t1,15 * 0'
            else:
                interval = '0 0\t* * 0'  # impossible de faire mieux, cron ne prend pas en charge 'every x weeks'
        elif schedule.interval.unity == 'HOUR':
            interval = '0 */' + schedule.interval.frequency + '\t* * *'
        elif schedule.interval.unity == 'MINUTE':
            interval = '*/' + schedule.interval.unity + ' *\t* * *'
        command = ' root python ' + os.environ['API_LOCAL_PATH'] + '/scripts/build_order.py --message build:' + schedule.name + ':' + schedule.branch
        return interval + command

    @staticmethod
    def update_schedule(old_schedule, new_schedule=None):
        try:
            cron_read = open('/etc/crontab', 'r')
        except FileNotFoundError:
            print('Can\'t find /etc/crontab')
            return 
        lines = cron_read.readlines()
        cron_read.close()
        cron_write = open('/etc/crontab', 'w')
        for line in lines:
            if line.strip('\n') != CrontabWriter.schedule_to_cron(old_schedule):
                cron_write.write(line)
        if new_schedule is not None:
            cron_write.write('\n')
            cron_write.write(CrontabWriter.schedule_to_cron(new_schedule))
        cron_write.close()




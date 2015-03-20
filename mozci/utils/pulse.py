import logging
import getpass
import sys

from mozillapulse.config import PulseConfiguration
from mozillapulse.consumers import GenericConsumer

LOG = logging.getLogger()

class TreeherderJobActionsConsumer(GenericConsumer):

    def __init__(self, **kwargs):
        super(TreeherderJobActionsConsumer, self).__init__(
            PulseConfiguration(**kwargs), 'exchange/treeherder/v1/job-actions', **kwargs)


def run_pulse(repo_name):
    user = raw_input('Please type your pulse username: ')
    password = getpass.getpass('Pulse password: ')
    label = 'mozci'
    topic = 'buildbot.{}.retrigger'.format(repo_name)
    pulse_args = {
        'applabel': label,
        'topic': topic,
        'durable': False,
        'user': user,
        'password': password
    }
    def on_build_event(data, message):
        LOG.info('Retrigger requested by %s received for job %s' % (
            data['requester'], data['job_id']))

    pulse = TreeherderJobActionsConsumer(callback=on_build_event, **pulse_args)
    try:
        while True:
            pulse.listen()
    except KeyboardInterrupt:
        sys.exit(1)

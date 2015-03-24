import logging
import getpass

from mozillapulse.consumers import NormalizedBuildConsumer

LOG = logging.getLogger()
CREDENTIALS = []


def get_pulse_credentials():
    global CREDENTIALS
    if not CREDENTIALS:
        user = raw_input("Please type your pulse username: ")
        password = getpass.getpass("Pulse password: ")
        CREDENTIALS = [user, password]
    else:
        LOG.debug('Accessing saved in-memory pulse credentials')
    return CREDENTIALS


def run_pulse(repo_name, topic_type, buildername, rev):
    label = 'mozci'
    topic = '{}.{}.#'.format(topic_type, repo_name)
    user, password = get_pulse_credentials()
    pulse_args = {
        'applabel': label,
        'topic': topic,
        'durable': False,
        'user': user,
        'password': password
    }
    def on_build_event(data, message):
        payload = data['payload']
        if payload['buildername'] != buildername or not payload['revision'].startswith(rev):
             return
        LOG.info('%s completed' % buildername)
        if 'blobber_files' in payload:
            structured_logs = [url for fn, url in payload['blobber_files'].iteritems()
                               if fn.endswith('_raw.log')]
            if structured_logs:
                LOG.info('Structured logs for %s available in %s' %
                         (payload['buildername'], structured_logs[0]))
                exit()
    pulse = NormalizedBuildConsumer(callback=on_build_event, **pulse_args)
    LOG.info('Listening on %s' % topic)
    while True:
        pulse.listen()

get_pulse_credentials()

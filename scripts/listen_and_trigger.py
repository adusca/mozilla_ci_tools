import logging
from argparse import ArgumentParser

from mozci.utils.pulse import run_pulse
from mozci.mozci import trigger_range, query_repo_name_from_buildername
from mozci.platforms import is_downstream

LOG = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(levelname)s:\t %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')
LOG.setLevel(logging.INFO)

def parse_args(argv=None):
    """Parse command line options."""
    parser = ArgumentParser()

    # Required arguments
    parser.add_argument('-b', "--buildername",
                        dest="buildername",
                        required=True,
                        type=str,
                        help="The buildername used in Treeherder.")

    parser.add_argument("-r", "--revision",
                        dest="rev",
                        required=True,
                        help='The 12 character represneting a revision (most recent).')

    options = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = parse_args()
    trigger_range(buildername=options.buildername,
                  revisions=[options.rev],
                  times=2,
                  dry_run=False)
    repo = query_repo_name_from_buildername(options.buildername)
    if is_downstream(options.buildername):
        topic = 'unittest'
    else:
        topic = 'build'
    run_pulse(repo, topic, options.buildername, options.rev)

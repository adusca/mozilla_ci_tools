"""
This module allow us to interact with taskcluster through the taskcluster
client.
"""
import datetime
import json
import logging
import sys
import traceback

import taskcluster as taskcluster_client

LOG = logging.getLogger('mozci')
TASKCLUSTER_TOOLS_HOST = 'https://tools.taskcluster.net'


def retrigger_task(task_id, dry_run=False):
    """ Given a task id (our uuid) we  query it and build
    a new task based on the old one which we schedule on TaskCluster.

    We don't call the rerun API since we can't rerun a task past
    its deadline, instead we create a new task with a new taskGroupId,
    expiration, creation and deadline values.

    http://docs.taskcluster.net/queue/api-docs/#createTask
    """
    try:
        queue = taskcluster_client.Queue()
        task = queue.task(task_id)

        LOG.debug("Original task:")
        LOG.debug(json.dumps(task))
        new_task_id = taskcluster_client.slugId()

        artifacts = task['payload'].get('artifacts', {})
        for artifact, definition in artifacts.iteritems():
            # XXX: We should check with gardnt if we got expiration dates
            # lined up properly with the task expiration date
            definition['expires'] = taskcluster_client.fromNow('364 days')

        # The task group will be identified by the ID of the only
        # task in the group
        task['taskGroupId'] = new_task_id
        # TC workers
        task['expires'] = taskcluster_client.fromNow('366 days')
        task['created'] = taskcluster_client.stringDate(datetime.datetime.utcnow())
        task['deadline'] = taskcluster_client.fromNow('24 hours')
        # XXX: task['payload']['command'] might need to manipulate to
        # extract any of the artifacts that were generated by the build that
        # triggered this test job

        LOG.debug("Contents of new task:")
        LOG.debug(task)
        if not dry_run:
            LOG.info("Attempting to schedule new task with task_id: {}".format(new_task_id))
            result = queue.createTask(new_task_id, task)
            LOG.debug(result)
            LOG.info("/{}/task-inspector/#{}/".format(
                TASKCLUSTER_TOOLS_HOST,
                new_task_id)
            )
        else:
            LOG.info("Dry-run mode: Nothing was retriggered.")

    except taskcluster_client.exceptions.TaskclusterRestFailure as e:
        traceback.print_exc()

    except taskcluster_client.exceptions.TaskclusterAuthFailure as e:
        # Hack until we fix it in the issue
        if str(e) == "Authorization Failed":
            LOG.info("The taskclaster client that you specified is lacking "
                     "the right set of scopes.")
            LOG.info("Run this same command with --debug and you will see "
                     "the missing scopes (the output comes from the "
                     "taskcluster python client)")
        elif str(e) == "Authentication Error":
            LOG.info("Make sure that you create permanent credentials and you "
                     "set these environment variables: TASKCLUSTER_CLIENT_ID, "
                     "TASKCLUSTER_ACCESS_TOKEN")
        sys.exit(1)

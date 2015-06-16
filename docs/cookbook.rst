Cookbook
========

.. contents:: Table of Contents
   :depth: 2
   :local:


I want to trigger one job in one revision N times
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need the job's buildername and the first 12 characters of the
revision hash.

You can find the buildername in Treeherder by clicking on the job and
then clicking on 'Job Details'. There will be a 'Buildername' key in
there for completed jobs.

Buildernames are consistent inside a branch, for example, every
mochitest-4 job on Linux x64 debug on try will have the buildername::
  "Ubuntu VM 12.04 x64 try debug test mochitest-4"

To trigger this job in the revision 123456abcdef 5 times::
  mozci-trigger -b "Ubuntu VM 12.04 x64 try debug test mochitest-4" -r 123456abcdef --times 5

--times is a paramater that can always be passed to the script

I want to trigger different jobs in the same revision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can pass multiple comma-separated buildernames to mozci-trigger::
  mozci-trigger -b "Ubuntu VM 12.04 x64 try debug test mochitest-4,Ubuntu VM 12.04 x64 try debug test mochitest-5" -r 123456abcdef

If you want to trigger several jobs with similar names, it may be a
good idea to use triggerbyfilters. If you want to

I want to trigger the same job across different revisions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* backfill

* from_change

* delta

* skips

I want to trigger every coalesced job in one revision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I want to trigger every talos job in one revision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# -*- coding: utf-8 -*-
# adapted from http://docs.openstack.org/developer/taskflow/examples.html

#    Copyright (C) 2015 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib

from random import randint
import os
import sys
from oslo_utils import uuidutils
from zake import fake_client
from taskflow.conductors import backends as conductor_backends
from taskflow import engines
from taskflow.jobs import backends as job_backends
from taskflow.patterns import linear_flow as lf
from taskflow.persistence import backends as persistence_backends
from taskflow.persistence import models
from taskflow import task
from taskflow.retry import Times

top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir))
sys.path.insert(0, top_dir)

JOBBOARD_CONF = {
    'board': 'zookeeper://localhost?path=/taskflow/jobs',
}

PERSISTENCE_URI = "sqlite:///{}".format(os.path.join(top_dir, 'db.sqlite3'))
LOGBOOK_NAME = 'fixture_logbook'
CONDUCTOR_NAME = 'conductor'
JOBS = 10


class ExampleTask(task.Task):
    def execute(self, message):
        print("Task message: {}".format(message))
        if randint(1, 2) == 1:
            message = "Failing task"
            print(message)
            raise RuntimeError(message)
        print("Task complete!")
        return message

    def revert(self, *args, **kwargs):
        print("Reverting task..")


def fixture_flow_factory():
    f = lf.Flow("fixture_flow", retry=Times(2))
    f.add(
        ExampleTask(
            "example_task_1"
        ),
        ExampleTask(
            "example_task_2",
            inject={
                'message': 'task 2 message'
            }
        ),
        ExampleTask(
            "example_task_3",
            inject={
                'message': 'Task 3. We might still make it this '
                           'far with the retry'
            }
        )
    )
    return f


def get_logbook_by_name(logbook_name, conn):
    return next(iter([i for i in conn.get_logbooks() if i.name == logbook_name]))


def print_con_event(event, details):
    print("Event '{}' has been received...".format(event))
    if event == 'job_consumed':
        print('Job completed!')


def run_conductor(c):
    print("Starting conductor")
    persist_backend = persistence_backends.fetch(PERSISTENCE_URI)
    with contextlib.closing(persist_backend):
        job_backend = job_backends.fetch(CONDUCTOR_NAME, JOBBOARD_CONF,
                                         persistence=persist_backend,
                                         client=c)

        job_backend.connect()
        with contextlib.closing(job_backend):
            cond = conductor_backends.fetch('nonblocking', CONDUCTOR_NAME, job_backend,
                                            persistence=persist_backend)
            cond.notifier.register(cond.notifier.ANY, print_con_event)
            try:
                cond.run(max_dispatches=JOBS - 1)
            finally:
                cond.stop()
                cond.wait()


def run_poster(c):
        persist_backend = persistence_backends.fetch(PERSISTENCE_URI)
        job_backend = job_backends.fetch(CONDUCTOR_NAME, JOBBOARD_CONF,
                                         persistence=persist_backend,
                                         client=c)
        job_backend.connect()
        for poster_number in range(JOBS):
            print("Posting job number {}".format(poster_number))
            with contextlib.closing(job_backend):
                # Create information in the persistence backend about the
                # unit of work we want to complete and the factory that
                # can be called to create the tasks that the work unit needs
                # to be done.
                with contextlib.closing(persist_backend.get_connection()) as conn:
                    lb = get_logbook_by_name(LOGBOOK_NAME, conn)
                    fd = models.FlowDetail("flow-from-{}".format(CONDUCTOR_NAME),
                                           uuidutils.generate_uuid())
                    fd.meta.update({
                        'store': {
                            'message': 'Injector message'
                        }
                    })
                    lb.add(fd)
                    conn.save_logbook(lb)

                engines.save_factory_details(
                    flow_detail=fd,
                    flow_factory=fixture_flow_factory,
                    factory_args=[],
                    factory_kwargs={},
                    backend=persist_backend
                )
                # Post the job to the backend
                job = job_backend.post(
                    "job-from-{}".format(CONDUCTOR_NAME), book=lb, details={
                            # Need this to find the job back in the logbook
                            # See _flow_detail_from_job
                            # http://pydoc.net/Python/taskflow/0.6.1/taskflow.conductors.base/
                            'flow_uuid': fd.uuid
                        }
                )
                print("Posted: {}".format(job))


def create_logbook():
    persist_backend = persistence_backends.fetch(PERSISTENCE_URI)
    with contextlib.closing(persist_backend.get_connection()) as conn:
        conn.upgrade()
        try:
            get_logbook_by_name(LOGBOOK_NAME, conn)
        except StopIteration:
            lb = models.LogBook(LOGBOOK_NAME)
            conn.save_logbook(lb)


def main():
    # Use an in-memory fake ZooKeeper using threads
    with contextlib.closing(fake_client.FakeClient()) as c:
        create_logbook()
        run_poster(c)
        run_conductor(c)


if __name__ == '__main__':
    main()

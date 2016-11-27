import contextlib
from django.conf import settings
from taskflow.persistence import backends as persistence_backends


def get_logbook_by_name(logbook_name, conn=None):
    def get_lb_from_conn(connection):
        return next(
            iter([i for i in connection.get_logbooks() if i.name == logbook_name])
        )

    if conn is None:
        with _get_persistence_backend() as conn:
            return get_lb_from_conn(conn)
    return get_lb_from_conn(conn)


@contextlib.contextmanager
def _get_persistence_backend():
    persist_backend = persistence_backends.fetch(settings.PERSISTENCE_URI)
    with contextlib.closing(persist_backend.get_connection()) as conn:
        yield conn


def get_logbooks():
    with _get_persistence_backend() as conn:
        return conn.get_logbooks()


def get_atoms_for_flow(flow):
    with _get_persistence_backend() as conn:
        return conn.get_atoms_for_flow(flow.uuid)


def get_flows_from_logbook(logbook):
    with _get_persistence_backend() as conn:
        return conn.get_flows_for_book(logbook.uuid)


def get_all_jobs():
    return {
        'logbooks': [
            {
                'name': lb.name,
                'meta': lb.meta,
                'flow_details': [
                    {
                        'uuid': f.uuid,
                        'atom_details': [
                            {
                                'uuid': a.uuid,
                                'name': a.name,
                                'state': a.state,
                            } for a in get_atoms_for_flow(f)
                        ],
                        'meta': f.meta,
                        'state': f.state,
                    } for f in get_flows_from_logbook(lb)
                ]
            } for lb in get_logbooks()
        ]
    }

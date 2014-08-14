# monitord
 
monitord is an application and process monitoring daemon. It is capable of
monitoring individual process on a machine as well as "pinging" web applications
to monitor application health. monitord is *not* responsible for launching
processes. Rather, it monitors processes always expected to be running.

# Quickstart

To register a process and application to be monitored by monitord, create a
config file entry like so:

```json
{
    'processes': [{
        'name': 'work_queue',
        'description': 'The distributed work queue for webapp',
        'pattern': '/usr/bin/python work_queue'
    }],
    'applications':  [{
        'name': 'webapp',
        'checks': [{
            'title': 'homepage',
            'description': 'Make sure we can hit the homepage',
            'url': 'http://localhost:5000/'
            'method': 'GET',
            'message': None,
            'expected_status': 200,
            }, {
            'title': 'post page',
            'description': 'Make sure we can properly process an HTTP POST sent to the /post_test/ endpoint',
            'url': 'http://localhost:5000/post_test/',
            'method': 'POST',
            'message': {'key': 'value'},
            'expected_status': 201,
            }, {
            'title': 'authorization',
            'description': 'Make sure we get a HTTP 401 when we try to access the admin page',
            'url': 'http://localhost:5000/admin'
            'method': 'GET',
            'message': None,
            'expected_status': 401,
            }]
    }]
}

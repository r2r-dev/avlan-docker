from json import loads
from subprocess import (
    CalledProcessError,
    Popen,
    PIPE,
)


def jsonize(func):
    def wrap(self, *args, **kwargs):
        payload = kwargs['payload']
        if isinstance(
                payload,
                basestring,
        ):
            kwargs['payload'] = loads(payload)
        return func(self, *args, **kwargs)
    return wrap


class AvlanBaseApi(object):
    def __init__(self, dao, redis=None):
        self._dao = dao
        self._redis = redis

    @staticmethod
    def _run_cmd(cmd):
        """
        Exercise command, grab its standard output
        and exit code.

        Returns:
            stdout (str): standard output

        Raises:
            CalledProcessError: in case of command failure
        """
        process = Popen(
            cmd,
            stdout=PIPE,
        )
        stdout, stderr = process.communicate()
        return_code = process.poll()
        if return_code:
            raise CalledProcessError(
                return_code,
                cmd,
                stderr,
            )
            pass
        return stdout


class AvlanApiException(Exception):
    pass

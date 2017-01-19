from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.messenger.view.AvlanMessengerShowView import \
    AvlanMessengerShowView
from webob import Response


# Open database connection
class AvlanMessengerShowController(AvlanAuthorizedController):
    def get(self):
        response = Response()
        execution_status = self.redis.get('command')
        execution_node_ip = self.redis.get('ip')
        execution_node_name = self.redis.get('name')
        command_output = self.redis.get('output')

        empty_output = (
            execution_status is None
            or
            execution_status is ''
        )

        if empty_output:
            return response

        view = AvlanMessengerShowView()

        view._full = not self.request.is_xhr

        view.command = execution_status
        view.output = command_output
        view.ip = execution_node_ip
        view.name = execution_node_name

        response.body = view.render()
        return response

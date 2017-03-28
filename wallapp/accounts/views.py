from rest_framework import response, status
from rest_framework.views import APIView

from djoser.views import ActivationView as OldActivationView


class SuspendAccountView(APIView):

    def post(self, request, *args, **kwargs):
        self.request.user.is_active = False
        self.request.user.save()
        return response.Response({'message': 'success'}, status=status.HTTP_200_OK)


class ActivationView(OldActivationView):
    """
    Use this endpoint to activate user account.
    """

    def _action(self, serializer):
        '''
        On activation, both email_verified, and is_active should be set to True
        '''
        serializer.user.email_verified = True
        return super()._action(serializer)

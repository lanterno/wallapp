from rest_framework.viewsets import ModelViewSet

from .serializers import PostSerializer
from .models import Post


class PostViewset(ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        super().check_object_permissions(request, obj)

        if self.action in ['update', 'partial_update'] and obj.owner != request.user:
            self.permission_denied(
                request, message="Only owner can update/delete object"
            )

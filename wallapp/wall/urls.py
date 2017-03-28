from rest_framework_extensions.routers import ExtendedSimpleRouter

from .views import PostViewset

router = ExtendedSimpleRouter()
router.register(r'posts', PostViewset, base_name='posts')


urlpatterns = router.urls

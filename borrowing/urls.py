from rest_framework.routers import DefaultRouter
from .views import IssuedBookViewSet

router = DefaultRouter()
router.register(r"issued-books", IssuedBookViewSet, basename="issued-books")

urlpatterns = router.urls

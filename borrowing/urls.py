from rest_framework.routers import DefaultRouter
from .views import IssuedBookViewSet

router = DefaultRouter()
router.register("issued-books", IssuedBookViewSet, basename="issued-book")

urlpatterns = router.urls

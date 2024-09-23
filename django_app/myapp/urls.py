from django.urls import include, path

from rest_framework import routers
from myapp.resources import (
  AnalysisViewSet,
  FileViewSet,
  SampleViewSet,
)

class BaseRouter(routers.DefaultRouter):
  """Override router to calculate properly the basename"""
  def register(self, prefix, viewset, basename=None):
    if hasattr(viewset, "queryset") and viewset.queryset is not None:
      basename = self.get_default_basename(viewset)
    self.registry.append((prefix, viewset, basename))

    # invalidate the urls cache
    if hasattr(self, "_urls"):
      del self._urls

router = BaseRouter()
router.register(r"^analyses", AnalysisViewSet, basename="analyses")
router.register(r"^files", FileViewSet, basename="files")
router.register(r"^samples", SampleViewSet, basename="samples")
urlpatterns = [
  path("", include(router.urls)),
]

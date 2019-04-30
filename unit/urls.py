from django.urls import path

from .views import unit_home, unit_detil, UnitNew,UnitUpdate,UnitDelete

urlpatterns = [
    path('', unit_home, name='unithome'),
    path('new', UnitNew.as_view(), name='unitnew'),
    path('<int:pk>', unit_detil, name='unitdetil'),
    path('<int:pk>/update',UnitUpdate.as_view(),name='unitupdate'),
    path('<int:pk>/delete',UnitDelete.as_view(),name='unitdelete'),
]
from home.views import *
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'persons', PeopleViewset, basename='person')
urlpatterns = router.urls

urlpatterns = [

    path('index/', index),
    path('people/', people),
    path('edit_people/', edit_people),
    path('delete/', delete),
    path('color/', color),
    path('login/', login),

    # For Class based view
    path('person-api/', PersonApi.as_view()),
    path('register/', RegisterAPI.as_view()),

    #For Viewset class
    path('',include(router.urls)),

]

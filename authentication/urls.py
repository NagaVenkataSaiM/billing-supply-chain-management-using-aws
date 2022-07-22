from django.urls import path,include
#now import the views.py file into this code
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('accounts', views.DropBoxViewset)

urlpatterns=[
  path('',views.home,name="home"),
  path('register/',views.register,name="register"),
  path('login/',views.login_x,name="login"),
  path('logout/',views.logout_x,name="logout"),
  path('',include(router.urls)),
  path('generatebill/',views.generatebill,name="generatebill"),
  path('viewbills/',views.viewbills,name="viewbills"),
  ]
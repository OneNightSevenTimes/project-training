from django.conf.urls import include,url
import views

urlpatterns = [
    url(r'^add_host',views.add_host,name='add_host'),
    url(r"^del_host",views.del_host,name='del_host')

]

"""
URL configuration for URLlibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Main import views as main_views
from Sign_up import views as signup_views
# define paths for all pages
urlpatterns = [
    path('admin/', admin.site.urls),
    # main paths
    path('add/', main_views.add_url, name='add_url'),
    path('library/', main_views.url_library, name='url_library'),
    path('my_library', main_views.myurls_library, name='myurls_library'),
    path('update/<int:pk>/', main_views.update_url, name='update_url'),
    path('delete/<int:pk>/', main_views.delete_url, name='delete_url'),
    path('about', main_views.about_view, name='how_it_works'),


    # sign_up paths
    path('login/', signup_views.login, name='login'),
    path('signup/', signup_views.signup, name='signup'),
    path('logout/', signup_views.logout, name='logout'),
    path('', signup_views.login, name='home'),  # Redirect root URL to login page
    

]
## define path for qr images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

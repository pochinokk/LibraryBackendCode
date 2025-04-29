from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from library_app import views

handler404 = 'library_app.views.page_not_found'
handler500 = 'library_app.views.server_error'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('about_us/', views.about, name='about'),
    path('authentication/', views.custom_login_view, name='authentication'),
    path('registration/', views.register_reader, name='registration'),
    path('admin/', admin.site.urls),
    path('librarian_account/', views.librarian_account, name='librarian_account'),
    path('reader_account/', views.reader_account, name='reader_account'),
    path('account/', views.role_redirect_view, name='role_redirect'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('add_reservation/<int:book_id>/', views.add_reservation, name='add_reservation'),
    path('cancel_reservation/<int:book_id>/', views.cancel_reservation, name='cancel_reservation'),

    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),

    path('readers/<int:pk>/edit/', views.edit_reader, name='edit_reader'),
    path('readers/<int:pk>/delete/', views.delete_reader, name='delete_reader'),

    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


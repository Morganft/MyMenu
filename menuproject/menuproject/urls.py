"""menuproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from accounts import views as account_views
from menu import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html', email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt'
         ),
         name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,6}-[0-9A-Za-z]{1,32})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='password_reset_confirm.html'
            ),
            name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    re_path(r'^receipts/(?P<pk>\d+)/$', views.receipt, name='receipt'),
    re_path(r'^receipts/(?P<pk>\d+)/edit/$', views.ReceiptUpdateView.as_view(), name='edit_receipt'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/new_ingredient/$',
            views.new_ingredient, name='new_ingredient'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/ingredients/(?P<ingredient_pk>\d+)/edit/$',
            views.IngredientUpdateView.as_view(), name='edit_ingredient'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/ingredients/(?P<pk>\d+)/delete/$',
            views.IngredientDeleteView.as_view(), name='delete_ingredient'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/new_step/$',
            views.new_step, name='new_step'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/steps/(?P<step_pk>\d+)/edit/$',
            views.StepUpdateView.as_view(), name='edit_step'),
    re_path(r'^receipts/(?P<receipt_pk>\d+)/steps/(?P<pk>\d+)/delete/$',
            views.StepDeleteView.as_view(), name='delete_step'),
    path('receipts/', views.ReceiptsListView.as_view(), name='receipts'),
    path('receipts/new_receipt/', views.new_receipt, name="new_receipt"),
    path('ingredient_types/', views.IngredientTypesListView.as_view(), name='ingredient_types'),
    path('ingredient_types/new_ingredient_type/', views.new_ingredient_type, name="new_ingredient_type"),
    re_path(r'^ingredient_types/(?P<ingredient_type_pk>\d+)/edit/$',
            views.IngredientTypeUpdateView.as_view(), name='edit_ingredient_type'),
    path('admin/', admin.site.urls),
    path('settings/account/', account_views.UserUpdateView.as_view(), name='my_account'),
    path('receipts/tag/<int:tag_id>', views.ReceiptsListView.as_view(), name='receipts_tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

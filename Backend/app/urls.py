from django.urls import include, path
from rest_framework import routers

from .views import (AllDontaionView, AllHelpProgramView, DonationView,
                    HelpProgramView, MessagesView, OrganizationDetailsView,
                    OrganizationLoginView, OrganizationLogoutView,
                    OrganizationRegisterView, PingView, UserDetailsView,
                    UserLoginView, UserLogoutView, UserSignupView, 
                    AccpetDonationView, RegisterPhoneNo)

router = routers.DefaultRouter()


urlpatterns = [
    path("ping/", PingView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/signup/", UserSignupView.as_view()),
    path("user/logout/", UserLogoutView.as_view()),
    path("user/details/", UserDetailsView.as_view()),
    path("org/login/", OrganizationLoginView.as_view()),
    path("org/signup/", OrganizationRegisterView.as_view()),
    path("org/logout/", OrganizationLogoutView.as_view()),
    path("org/details/", OrganizationDetailsView.as_view()),
    path('donation/', DonationView.as_view()),
    path('donation/<int:pk>/', DonationView.as_view()),
    path('all_donations/', AllDontaionView.as_view()),
    path('help_prg/', HelpProgramView.as_view()),
    path('help_prg/<int:pk>/', HelpProgramView.as_view()),
    path('all_help_prg/', AllHelpProgramView.as_view()),
    path('view_messages/', MessagesView.as_view()),
    path('accept_donation/', AccpetDonationView.as_view()),
    path('register_phone_no/', RegisterPhoneNo.as_view())
]

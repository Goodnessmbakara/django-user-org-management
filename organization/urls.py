from django.urls import path
from .views import OrganisationView, SingleOrganisationView, CreateOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('api/organisations', OrganisationView.as_view(), name='organisations'),
    path('api/organisations/<int:orgId>', SingleOrganisationView.as_view(), name='organisation-detail'),
    path('api/organisations', CreateOrganisationView.as_view(), name='create-organisation'),
    path('api/organisations/<int:orgId>/users', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]

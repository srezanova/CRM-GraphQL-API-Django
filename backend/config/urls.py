from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
    path('login/', include('frontend.urls')),
    path('new-request/', include('frontend.urls')),
    path('requests/<str:id>/', include('frontend.urls')),
    path('requests/<str:id>/edit', include('frontend.urls')),
    path('', include('frontend.urls')),

]

from django.conf.urls import url

from geneinfo import views_api

app_name = "geneinfo"
api_urlpatterns = [
    url(
        regex=r"^api/lookup-gene/$", view=views_api.LookupGeneApiView.as_view(), name="lookup-gene"
    ),
    url(
        regex=r"^api/gene-infos/(?P<database>[a-z]+)/(?P<geneid>[0-9a-zA-Z]+)/?$",
        view=views_api.GeneInfosApiView.as_view(),
        name="api-gene-infos",
    ),
]

urlpatterns = api_urlpatterns

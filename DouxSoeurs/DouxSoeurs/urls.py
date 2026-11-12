from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

def robots_txt(request):
    # Dit aux moteurs de recherche : tout le site est explorable, sauf l'administration, et voici le sitemap
    contenu = (
        "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: "
        + request.build_absolute_uri("/sitemap.xml")
    )
    return HttpResponse(contenu, content_type="text/plain")


urlpatterns = [
    path("sitemap.xml", sitemap),   # liste de toutes les pages publiées
    path("robots.txt", robots_txt),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

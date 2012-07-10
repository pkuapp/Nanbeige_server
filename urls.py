from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nanbeige.views.home', name='home'),
    # url(r'^nanbeige/', include('nanbeige.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^app/version/api/$','nbg.views_app.version_api'),
    (r'^app/version/android/$','nbg.views_app.version_android'),
    (r'^app/version/ios/$','nbg.views_app.version_ios'),
    (r'^app/notice/$','nbg.views_app.notice'),
    (r'^user/login/email/$','nbg.views_user.login_email'),
    (r'^user/login/weibo/$','nbg.views_user.login_weibo'),
    (r'^university/list/$'.'nbg.views_university.list'),
    (r'^university/\d+/$','nbg.views_university.detail'),
)
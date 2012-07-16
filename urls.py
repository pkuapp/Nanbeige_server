from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^nanbeige/', include('nanbeige.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'nbg.views.doc_html'),
    (r'^status/$', 'nbg.views.status_html'),

    (r'^app/version/api/$', 'nbg.views_app.version_api'),
    (r'^app/version/android/$', 'nbg.views_app.version_android'),
    (r'^app/version/ios/$', 'nbg.views_app.version_ios'),
    (r'^app/notice/$', 'nbg.views_app.notice'),

    (r'^user/login/email/$', 'nbg.views_user.login_email'),
    (r'^user/login/weibo/$', 'nbg.views_user.login_weibo'),

    (r'^university/list/$', 'nbg.views_university.university_list'),
    (r'^university/(\d+)/$', 'nbg.views_university.detail'),

    (r'^course/list/$', 'nbg.views_course.course_list'),
    (r'^course/assignment/list/$', 'nbg.views_course.assignment_list'),
    (r'^course/assignment/(\d+)/finish/$', 'nbg.views_course.assignment_finish'),
    (r'^course/assignment/(\d+)/delete/$', 'nbg.views_course.assignment_delete'),
    (r'^course/assignment/(\d+)/modify/$', 'nbg.views_course.assignment_modify'),
    (r'^course/assignment/add/$', 'nbg.views_course.homework_add'),
    (r'^course/(\d+)/comment/add/$', 'nbg.views_course.comment_add'),
    (r'^course/(\d+)/comment/list/$', 'nbg.views_course.comment_list'),

    (r'^comment/address/$', 'nbg.views_comment.address'),

    (r'^study/building/list/$', 'nbg.views_study.building_list'),
    (r'^study/building/(\d+)/room/list/$', 'nbg.views_study.room_list'),

    (r'^event/query/$','nbg.views_event.query'),

    (r'^wiki/list/(\d+)/$', 'nbg.views_wiki.wiki_list'),
    (r'^wiki/node/(\d+)/$', 'nbg.views_wiki.wiki_node'),
)

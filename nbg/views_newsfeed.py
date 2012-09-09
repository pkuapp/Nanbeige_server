from nbg.helpers import json_response, auth_required
from nbg.models import NewsFeed
from django.core.cache import cache
from nbg.helpers import once_upon_a_time

@auth_required
@json_response
def newsfeed(request):
    after = request.GET.get('after', once_upon_a_time())
    newsfeed_list = cache.get(request.session.session_key+'_newsfeed')
    if newsfeed_list:
        sub_list = newsfeed_list.filter(time__gte=after).order_by('time')
    else:
        newsfeed_list = list()
        user_profile = request.user.get_profile()
        courses_id_list = user_profile.courses.all().values_list('id', flat=True).order_by('id')
        newsfeed_list = NewsFeed.objects.filter(object_id__in=courses_id_list, ref_model='Course')
        cache.set(request.session.session_key+'_newsfeed', newsfeed_list)
        sub_list = newsfeed_list.filter(time__gte=after).order_by('time')

    ret = [{
        'news_type': NewsFeed.NEWS_TYPE_CHOICES[x.news_type][1],
        'ref_model': 'Course',
        'object_id': x.object_id,
        'time': x.time.isoformat(' '),
    } for x in sub_list]

    return ret

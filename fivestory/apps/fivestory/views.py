import json
import requests
import string

from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.generic import View, TemplateView

from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from .models import Story

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
        
def hello(request):
    return HttpResponse('Hello world')

class StoryListView(TemplateView):
    template_name = "story_list.html"

class StoryDetailView(TemplateView):
    template_name = "story_detail.html"

class api(View):
    def get(self, request, story_id=None):
        if story_id:
            story = Story.objects.get(id=story_id)
            response = {
                'story': {
                    'frame1': {
                        'id': 1,
                        'text': story.tweet1_text,
                        'photo': story.tweet1_photo,
                    },
                    'frame2': {
                        'id': 2,
                        'text': story.tweet2_text,
                        'photo': story.tweet2_photo,
                    },
                    'frame3': {
                        'id': 3,
                        'text': story.tweet3_text,
                        'photo': story.tweet3_photo,
                    },
                    'frame4': {
                        'id': 4,
                        'text': story.tweet4_text,
                        'photo': story.tweet4_photo,
                    },
                    'frame5': {
                        'id': 5,
                        'text': story.tweet5_text,
                        'photo': story.tweet5_photo,
                    },
                }
            }
        else:
            response = {
                'stories': list(Story.objects.filter(is_active=True).order_by('-updated').values('id','name','tweet1_photo'))
            }

        return JsonResponse(response)
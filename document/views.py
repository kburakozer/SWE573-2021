from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from . models import Document, Tag
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity, TrigramDistance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Tag_form
# Create your views here.

# def index(request):
#     return HttpResponse("Hello my friend")


class IndexClassView(ListView):
    model = Document;
    template_name = 'document/document.html'
    context_object_name = 'document_list'
    paginate_by = 20


        


class DocDetailView(DetailView):
    model = Document;
    template_name = 'document/detail.html'


class Search(ListView):
    model = Document;
    template_name = 'document/search_result.html'
    paginate_by = 20
    def get_queryset(self):
        query = self.request.GET.get("q")
        # object_list = Document.objects.filter(title__search=query)
        

        vector = SearchVector('title', weight='A') + SearchVector('keywords', weight='B') + SearchVector('tokens', weight='C')
        query2 = SearchQuery(query)
        object_list = Document.objects.annotate(rank=SearchRank(vector, query2, cover_density=True)).order_by('-rank')
        object_list = Document.objects.annotate(distance=TrigramDistance('tokens', query2)).filter(distance__lte=0.3).order_by('distance')
        object_list = Document.objects.annotate(search=SearchVector('title','keywords','tokens'),).filter(search=SearchQuery(query))
        
        return object_list

@login_required      
def Tag_view(request, doc_id):
    if request.method =='POST':
        form = Tag_form(request.POST)
        
        # tag_request_from_browser = ''
        
        if form.is_valid():
            document = Document.objects.filter(doc_id = doc_id)

            query = form.cleaned_data['tag_name']
            api_url = "https://www.wikidata.org/w/api.php"

            params = {
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'en',
                'search': query
            }

            result = requests.get(api_url, params = params)
            try:
                tag_name = tag = result.json()['searchinfo']['search']
                tag_id = (result.json()['search'][0]["id"])
                tag_url = (result.json()['search'][0]["url"])
                tag = Tag(tag_name = tag_name, tag_url = tag_url)

            except:
                tag = Tag(tag_name = form.cleaned_data['tag_name'], tag_url = "")

            #tag = Tag(tag_name = form.cleaned_data['tag_name'], tag_url = form.cleaned_data['tag_url'])
            # # tag_request_from_browser = form.cleaned_data['tag_key'].split(':')
            # # tag_key = tag_request_from_browser[0]
            # # tag_value = 'http://www.wikidata.org/wiki/' + tag_request_from_browser[1]
            
            # tag = Tag(tag_key = tag_key,
            #         tag_value = tag_value
            #     )
            tag.save()
            if len(document) > 1:
                document[0].tags.add(tag)
                document[1].tags.add(tag)

            else:
                document.tags.add(tag)
            # TODO Httpresponseredirect
            return HttpResponse('/thanks')

    else:
        form = Tag_form()

    return render(request, 'document/tagging.html', {'form': form, 'doc_id': doc_id})


def register(request):
    #form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form. cleaned_data.get('username')
            messages.success(request, f'Welcome {username}')
            return redirect('document:login')
    else:
        form = UserCreationForm()
    return render(request,'document/register.html', {'form':form})
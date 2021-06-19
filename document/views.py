from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from . models import Document, Tag
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity, TrigramDistance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Tag_form
from . wikidata import Tag_suggestion

# Create your views here.

# home page view
class IndexClassView(ListView):
    model = Document;
    template_name = 'document/document.html'
    context_object_name = 'document_list'
    paginate_by = 20


        

# document detail view
class DocDetailView(DetailView):
    model = Document;
    template_name = 'document/detail.html'

# implements search
class Search(ListView):
    model = Document;
    template_name = 'document/search_result.html'
    paginate_by = 20
    def get_queryset(self):
        query = self.request.GET.get("q")
        # object_list = Document.objects.filter(title__search=query)
        


        vector = SearchVector('tags', weight='A') + SearchVector('title', weight='B') + SearchVector('keywords', weight='C') + SearchVector('tokens', weight='D')
        query2 = SearchQuery(query)
        
        object_list = Document.objects.annotate(distance=TrigramDistance('tokens', query2)).filter(distance__lte=0.3).order_by('distance')
        object_list = Document.objects.annotate(search=SearchVector('tags','title','keywords','tokens'),).filter(search=SearchQuery(query))
        object_list = Document.objects.annotate(rank=SearchRank(vector, query2, cover_density=True)).order_by('-rank')
        
        return object_list

@login_required      
def Tag_view(request, doc_id):
    if request.method =='POST':
        form = Tag_form(request.POST)
        
        if form.is_valid():
            document = Document.objects.filter(doc_id = doc_id)
            tag_str= form.cleaned_data['tag_name']
            tag_list = tag_str.split(' - ')
            tag_name = tag_list[1]
            custom_tag = form.cleaned_data['custom_tag']
            url = ""
            if len(tag_name) != 0 and len(custom_tag) != 0: 
                tag_name = custom_tag.lower()
                tag_url = ""
                try:
                    tag_url = 'http://www.wikidata.org/wiki/' + tag_list[0]
                except:
                    pass
                tag = Tag(tag_name = tag_name, tag_url = tag_url)
                tag.save()
                if len(document) > 1:
                    document[0].tags.add(tag)
                    document[1].tags.add(tag)
                else:
                    document.tags.add(tag)              
            
            elif len(tag_name) >=1:
                tag_url = ""
                try:
                    tag_url = 'http://www.wikidata.org/wiki/' + tag_list[0]
                except:
                    pass
                tag = Tag(tag_name = tag_name.lower(), tag_url = tag_url)
                tag.save()
                if len(document) > 1:
                    document[0].tags.add(tag)
                    document[1].tags.add(tag)
                    prim_key = document[0].pk
                    url = '/' +  str(prim_key) + '/'
                else:
                    document.tags.add(tag)
                    prim_key = document.pk
                    url = '/' +  str(prim_key) + '/'
                
                
                return redirect(url)
            else:
                pass
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





def autocompletion(request):
    if request.is_ajax():
        query = request.GET.get('query', '')
        tag_suggestions = Tag_suggestion.get_label(query)
        data = {
            'tag_suggestions':tag_suggestions,
        }
        return JsonResponse(data)

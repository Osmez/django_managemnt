from typing import KeysView
from .forms import MarketPostAddForm, MarketCommentAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views import View
from django.core.paginator import Paginator
from .models  import Markpost, Markcomments, Document,Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorations import allowed_users
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from test1.models import MarkCommentNotifi


def AddUserToGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="madmin")
        the_group.user_set.add(us)
        
        return redirect('marketing-home')
        
def RemoveUserFromGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="madmin")
        the_group.user_set.remove(us)
        
        return redirect('marketing-home')



@login_required
@allowed_users(allowed_roles=['Marketing'])
def marketing_home(request):
    all_posts = Markpost.objects.all()
    search_term = ''
    if 'title' in request.GET:
        all_posts = all_posts.order_by('title')

    if 'date' in request.GET:
        all_posts = all_posts.order_by('date_created')

    if 'first' in request.GET:
        all_posts = all_posts.order_by('-date_created')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_posts = all_posts.filter(title__icontains=search_term)    

    pagin = Paginator(all_posts, 5)
    page = request.GET.get('page')
    mposts = pagin.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    
    persons = User.objects.filter(groups__name='Marketing')

    context = {
        'mposts': mposts,
        'params': params,
        'search_term': search_term,
        'persons' : persons
    }
    return render(request, 'marketing/marketing-home.html',context)

@login_required
@allowed_users(allowed_roles=['Marketing'])
def marketing_detail_view(request, mpost_id, ):
    post = Markpost.objects.get(id=mpost_id)
    form = MarketCommentAddForm(request.POST)
    u = post.author

    if request.method == 'POST':
        form = MarketCommentAddForm(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            
            if post.author.is_superuser:
                u = User.objects.get(id=17)

            mnot = MarkCommentNotifi.objects.create(notification_type=2,to_user=u,from_user=request.user,mrk_post=post,stuff_name=post.author.username)

            
            return redirect('mark-detail',mpost_id=mpost_id)
    else:
        form = MarketCommentAddForm

    comments = Markcomments.objects.filter(post = post).order_by('-date')

    context = {
        'post':post,
        'form':form,
        'comments': comments
    }

    return render(request, 'marketing/marketing-detail.html', context)

@login_required
@allowed_users(allowed_roles=['Marketing'])
def marketingpost_add(request):
    if request.method == 'POST':
        form = MarketPostAddForm(request.POST,request.FILES)
        files = request.FILES.getlist('image')
        docs  = request.FILES.getlist('file')
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            for f in files:
                img = Image(image=f)
                img.save()
                post.image.add(img)
                
            for d in docs:
                doc = Document(docfile = d)
                doc.save()
                post.file.add(doc)
                
            post.save()
            u = User.objects.get(id=17)
            mot = MarkCommentNotifi.objects.create(notification_type=1,to_user=u,from_user=request.user,mrk_post=post)

            messages.success(request,"Added Post successfully")

            return redirect('marketing-home')
    else:
        form = MarketPostAddForm()

    context = {
        'form':form,
    }

    return render(request, 'marketing/marketing-new.html',context)

def not_allowed(request):
    return render(request,'test1/forbidden.html')

class MarkCommentReplyView(LoginRequiredMixin,View):
    def post(self, request, post_id, pk, *args, **kwargs):
        post = Markpost.objects.get(id = post_id)
        parent_comment = Markcomments.objects.get(pk = pk)
        form = MarketCommentAddForm(request.POST)
        u = parent_comment.author
    
        if form.is_valid():
            rep = form.save(commit=False)
            rep.post = post
            rep.author = request.user
            rep.parent = parent_comment
            rep.save()
            if parent_comment.author.is_superuser:
                u = User.objects.get(id=17)

            mot =MarkCommentNotifi.objects.create(notification_type=3,to_user=u,from_user=request.user,mrk_post=post,stuff_name=parent_comment.author.username)


        return redirect('mark-detail',mpost_id=post_id)

class MarkPostEditView(LoginRequiredMixin,UpdateView):
    model = Markpost
    fields = ['title','content']
    template_name = 'marketing/marketing-edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('mark-detail', kwargs={'mpost_id':pk})

class MarkPostDeleteView(LoginRequiredMixin,DeleteView):
    model = Markpost
    template_name = 'marketing/marketing-delete.html'
    success_url = reverse_lazy('marketing-home')

class MarkCommentDelete(LoginRequiredMixin,DeleteView):
    model = Markcomments
    template_name = 'marketing/marketing-comment-delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_id']
        return reverse_lazy('mark-detail', kwargs={'mpost_id':pk})


from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Graphpost, GraphComments, Image,Document
from .forms import GraphcommentAddForm,GraphicForm
from .decorations import allowed_users
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import View
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from test1.models import GraphCommentNotifi


def AddUserToGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="gadmin")
        the_group.user_set.add(us)
        
        return redirect('graph-home')

def RemoveUserFromGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="gadmin")
        the_group.user_set.remove(us)
        
        return redirect('graph-home')


@login_required
@allowed_users(allowed_roles=['GraphicDesign'])
def graphic_home(request):
    all_polls = Graphpost.objects.all()
    search_term = ''
    if 'title' in request.GET:
        all_polls = all_polls.order_by('title')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('date_created')

    if 'first' in request.GET:
        all_polls = all_polls.order_by('-date_created')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(title__icontains=search_term)        

    pagin = Paginator(all_polls, 3)
    page = request.GET.get('page')
    posts = pagin.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    
    persons = User.objects.filter(groups__name='GraphicDesign')

    context = {
        'posts': posts,
        'params': params,
        'search_term': search_term,
        'persons':persons
    }

    return render(request, 'graphdesign/graphdesign-home.html', context)

@login_required
@allowed_users(allowed_roles=['GraphicDesign'])
def graphic_detail_view(request, gpost_id, ):
    post = Graphpost.objects.get(id=gpost_id)
    form = GraphcommentAddForm(request.POST)
    u = post.author

    if request.method == 'POST':
        form = GraphcommentAddForm(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            
            if post.author.is_superuser:
                u = User.objects.get(id=17)

            mnot = GraphCommentNotifi.objects.create(notification_type=2,to_user=u,from_user=request.user,gr_post=post,stuff_name=post.author.username)

            
            return redirect('graph-detail',gpost_id=gpost_id)
    else:
        form = GraphcommentAddForm()

    comments = GraphComments.objects.filter(post = post).order_by('-date')

    context = {
        'post':post,
        'form':form,
        'comments': comments
    }

    return render(request, 'graphdesign/graphdesign-detail.html', context)

@login_required
@allowed_users(allowed_roles=['GraphicDesign'])
def graphic_add(request):
    if request.method == 'POST':
        form = GraphicForm(request.POST, request.FILES)
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
            got = GraphCommentNotifi.objects.create(notification_type=1,to_user=u,from_user=request.user,gr_post=post)


            messages.success(request,"Added Post successfully")

            return redirect('graph-home')
    else:
        form = GraphicForm()

    context = {
        'form':form,
    }

    return render(request, 'graphdesign/graphdesign-add.html',context)

def not_allowed(request):
    return render(request, 'test1/forbidden.html');

class GraphCommentReplyView(LoginRequiredMixin,View):
    def post(self, request, post_id, pk, *args, **kwargs):
        post = Graphpost.objects.get(id = post_id)
        parent_comment = GraphComments.objects.get(pk = pk)
        form = GraphcommentAddForm(request.POST)
        u = parent_comment.author
    
        if form.is_valid():
            rep = form.save(commit=False)
            rep.post = post
            rep.author = request.user
            rep.parent = parent_comment
            rep.save()
            if parent_comment.author.is_superuser:
                u = User.objects.get(id=17)

            got = GraphCommentNotifi.objects.create(notification_type=3,to_user=u,from_user=request.user,gr_post=post,stuff_name=parent_comment.author.username)


        return redirect('graph-detail',gpost_id=post_id)

class GraphPostEditView(LoginRequiredMixin,UpdateView):
    model = Graphpost
    fields = ['title','content','image']
    template_name = 'graphdesign/graphdesign-edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('graph-detail', kwargs={'gpost_id':pk})

class GraphPostDeleteView(LoginRequiredMixin,DeleteView):
    model = Graphpost
    template_name = 'graphdesign/graphdesign-delete.html'
    success_url = reverse_lazy('graph-home')

class GraphCommentDelete(LoginRequiredMixin,DeleteView):
    model = GraphComments
    template_name = 'graphdesign/graphdesign-comment-delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_id']
        return reverse_lazy('graph-detail', kwargs={'gpost_id':pk})

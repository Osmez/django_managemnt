from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from django.views import View
from django.core.paginator import Paginator
from .forms import ProgrmPostAddForm, ProgrmCommentAddForm
from .models  import Progrmpost, Progrmcomments,Document,Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorations import allowed_users
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from test1.models import ProgramCommentNotifi

def AddUserToGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="padmin")
        the_group.user_set.add(us)
        
        return redirect('progrm-home')
        
def RemoveUserFromGroupView(request,user_id):
        us = User.objects.get(pk=user_id)
        the_group = Group.objects.get(name="padmin")
        the_group.user_set.remove(us)
        
        return redirect('progrm-home')



@login_required
@allowed_users(allowed_roles=['Programming'])
def programming_home(request):
    all_posts = Progrmpost.objects.all()
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
    pposts = pagin.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    
    persons = User.objects.filter(groups__name='Programming')

    context = {
        'pposts': pposts,
        'params': params,
        'search_term': search_term,
        'persons':persons
    }
    return render(request, 'programming/progrm-home.html',context)

@login_required
@allowed_users(allowed_roles=['Programming'])
def programming_detail_view(request, ppost_id, ):
    post = Progrmpost.objects.get(id=ppost_id)
    form = ProgrmCommentAddForm(request.POST)
    u = post.author

    if request.method == 'POST':
        form = ProgrmCommentAddForm(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            
            if post.author.is_superuser:
                u = User.objects.get(id=17)

            pnot = ProgramCommentNotifi.objects.create(notification_type=2,to_user=u,from_user=request.user,prg_post=post,stuff_name=post.author.username)

            
            return redirect('progrm-detail',ppost_id=ppost_id)
    else:
        form = ProgrmCommentAddForm

    comments = Progrmcomments.objects.filter(post = post).order_by('-date')

    context = {
        'post':post,
        'form':form,
        'comments': comments
    }

    return render(request, 'programming/progrm-detail.html', context)

@login_required
@allowed_users(allowed_roles=['Programming'])
def programming_detail_view_reply(request, ppost_id, reply_id):
    post = Progrmpost.objects.get(id=ppost_id)
    form = ProgrmCommentAddForm(request.POST)
    u = post.author

    if request.method == 'POST':
        form = ProgrmCommentAddForm(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            
            if post.author.is_superuser:
                u = User.objects.get(id=17)

            pnot = ProgramCommentNotifi.objects.create(notification_type=2,to_user=u,from_user=request.user,prg_post=post,stuff_name=post.author.username)

            
            return redirect('progrm-detail',ppost_id=ppost_id)
    else:
        form = ProgrmCommentAddForm

    comments = Progrmcomments.objects.filter(post = post).order_by('-date')

    context = {
        'post':post,
        'form':form,
        'reply':reply_id,
        'comments': comments
    }

    return render(request, 'programming/progrm-detail-reply.html', context)
@login_required
@allowed_users(allowed_roles=['Programming'])
def programmingpost_add(request):
    if request.method == 'POST':
        form = ProgrmPostAddForm(request.POST,request.FILES)
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

            messages.success(request,"Added Post successfully")
            
            u = User.objects.get(id=17)
            pot = ProgramCommentNotifi.objects.create(notification_type=1,to_user=u,from_user=request.user,prg_post=post,stuff_name=post.author.username)


            return redirect('progrm-home')
    else:
        form = ProgrmPostAddForm()

    context = {
        'form':form,
    }

    return render(request, 'programming/progrm-new.html',context)

def not_allowed(request):
    return render(request,'test1/forbidden.html')

class ProgCommentReplyView(LoginRequiredMixin,View):
    def post(self, request, post_id, pk, *args, **kwargs):
        post = Progrmpost.objects.get(id = post_id)
        parent_comment = Progrmcomments.objects.get(pk = pk)
        form = ProgrmCommentAddForm(request.POST)
        u = parent_comment.author
    
        if form.is_valid():
            rep = form.save(commit=False)
            rep.post = post
            rep.author = request.user
            rep.parent = parent_comment
            rep.save()
            if parent_comment.author.is_superuser:
                u = User.objects.get(id=17)

            pot = ProgramCommentNotifi.objects.create(notification_type=3,to_user=u,from_user=request.user,prg_post=post,prg_Comment=parent_comment,stuff_name=parent_comment.author.username)


        return redirect('progrm-detail',ppost_id=post_id)

class ProgReplyReplyView(LoginRequiredMixin,View):
    def post(self, request, post_id, pk, rk, *args, **kwargs):
        post = Progrmpost.objects.get(id = post_id)
        parent_comment = Progrmcomments.objects.get(pk = pk)
        reply_comment = Progrmcomments.objects.get(pk = rk)
        form = ProgrmCommentAddForm(request.POST)
        u = reply_comment.author
    
        if form.is_valid():
            rep = form.save(commit=False)
            rep.post = post
            rep.author = request.user
            rep.parent = parent_comment
            rep.save()
            if reply_comment.author.is_superuser:
                u = User.objects.get(id=17)
            reply_comment = rep

            pot = ProgramCommentNotifi.objects.create(notification_type=3,to_user=u,from_user=request.user,prg_post=post,prg_Comment=reply_comment,stuff_name=reply_comment.author.username)


        return redirect('progrm-detail',ppost_id=post_id)


class ProgPostEditView(LoginRequiredMixin,UpdateView):
    model = Progrmpost
    fields = ['title','content']
    template_name = 'programming/progrm-edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('progrm-detail', kwargs={'ppost_id':pk})


class ProgPostDeleteView(LoginRequiredMixin,DeleteView):
    model = Progrmpost
    template_name = 'programming/progrm-delete.html'
    success_url = reverse_lazy('progrm-home')


class ProgCommentDelete(LoginRequiredMixin,DeleteView):
    model = Progrmcomments
    template_name = 'programming/progrm-comment-delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_id']
        return reverse_lazy('progrm-detail', kwargs={'ppost_id':pk})


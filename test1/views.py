from itertools import count
from django.http import HttpResponse
from django.shortcuts import redirect,render , get_object_or_404
from .models import post,ProgramCommentNotifi,MarkCommentNotifi,GraphCommentNotifi
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage
from django.views.generic import CreateView ,UpdateView  ,DeleteView
from .forms import  PostCreateForm 
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic.base import View
from user.models import Requests
from django.http import HttpResponse



def start(request):

    return render(request,'test1/start.html')


def home(request):
    posts1=post.objects.all()
    paginator=Paginator(posts1,5)
    page=request.GET.get('page')
    count = Requests.objects.count()
    cc = ProgramCommentNotifi.objects.first()
    print(cc.prg_Comment)
    try:
        posts1=paginator.page(page)
    except PageNotAnInteger:
        posts1=paginator.page(1)
    except EmptyPage:
        posts1=paginator.page(paginator.num_page)

    context={
        'title':'الصفحة الرئيسية',
        'posts':posts1,
        'page':page,
        'count':count
    }
    return render(request ,'test1/index.html', context)

def post_detail(request , post_id):
    post1 =get_object_or_404(post, pk=post_id)

    context={
        'title':post1,
        'post':post1,

        

    }
     
    return render(request,'test1/detail.html',context)

class PostCreateView(CreateView):
    model=post
    #fields=['title' ,'content']
    template_name='test1/new_post.html'
    form_class=PostCreateForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model=post
    template_name='test1/post_update.html'
    form_class=PostCreateForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post3=self.get_object()
        if self.request.user==post3.author:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = post
    # success_url='/'
    
    def test_func(self):
        post3=self.get_object()
        if self.request.user==post3.author:
            return True
        else:
            return False
            
            
class ProgNotifi(View):
    def get(self,request,n_pk,post_pk,*args,**kwargs):
        notification = ProgramCommentNotifi.objects.get(id=n_pk)
        notification.user_has_seen = False
        notification.save()

        return redirect('progrm-detail',ppost_id=post_pk)

class MarkNotifi(View):
    def get(self,request,n_pk,post_pk,*args,**kwargs):
        notification = MarkCommentNotifi.objects.get(id=n_pk)
        notification.user_has_seen = True
        notification.save()

        return redirect('mark-detail',mpost_id=post_pk)

class GraphNotifi(View):
    def get(self,request,n_pk,post_pk,*args,**kwargs):
        notification = GraphCommentNotifi.objects.get(id=n_pk)
        notification.user_has_seen = True
        notification.save()

        return redirect('graph-detail',gpost_id=post_pk)

class RemoveNotifi(View):
    def delete(self,request,n_pk,*args,**kwargs):
        notification = ProgramCommentNotifi.objects.get(id=n_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('success',content_type="text/plan")
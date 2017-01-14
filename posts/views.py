from urllib.parse import quote_plus as qp
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import PostForm
from .models import Post


def post_create(request):
    #  if not request.user.is_staff or not request.user.is_superuser:
    #    raise Http404
    if request.user.is_authenticated():
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Successfully Created :)")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        raise Http404
    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all()
    srch = request.GET.get("s")
    if srch:
        queryset_list = queryset_list.filter(
            Q(title__icontains=srch) |
            Q(content__icontains=srch) |
            Q(content_desc__icontains=srch) |
            Q(category__icontains=srch) |
            Q(keywords__icontains=srch) |
            Q(user__first_name__icontains=srch) |
            Q(user__last_name__icontains=srch)
        ).distinct()

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('p')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "<a href='/'>Ali GÖREN</a>"
    }

    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated():
        form = PostForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Item Saved :)", extra_tags="html_safe")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        raise Http404
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated():
        instance.delete()
        messages.success(request, "Successfully Deleted :)")
        return redirect("posts:list")
    else:
        raise Http404

def not_found(request):
    return render(request,'404.html')

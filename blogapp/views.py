from django.shortcuts import render, HttpResponse, redirect
from blogapp.models import Post, BlogComment
from django.contrib import messages
from blogapp.templatetags import extras
# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts}
    return render(request, 'blog/bloghome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict:
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {"post": post, "comments": comments, "user": request.user, "replyDict": replyDict}
    return render(request, 'blog/blogpost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSn = request.POST.get("postSn")
        post = Post.objects.get(sno=postSn)
        parentSn = request.POST.get("parentSn")

        if parentSn=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Comment Posted")
        else:
            parent= BlogComment.objects.get(sno=parentSn)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Reply Posted")

    return redirect(f"/blog/{post.slug}")
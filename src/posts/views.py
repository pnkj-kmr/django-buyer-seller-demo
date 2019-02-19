from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from .forms import *
import traceback


def home(request, *args, **kwargs):
    """This function helps to publish the home page after login success.
    """
    data = {}    
    try:
        if request.user.first_name in (0, '0', None, 'None', 'Buyer'):
            data = publish_buyer_view(request)
        else:
            data = publish_seller_view(request)
    except:
        traceback.print_exc()
    print("Data >>>",data)
    return render(request, 'home.html', data)


def publish_buyer_view(request):
    """Function helps to publish buyer view
    """
    data = {}
    data['url_name'] = "Add Post"
    data['url_uri'] = "add_post/"

    # print("User >>>", request.user.username)
    # posts = Posts.objects.all()
    posts = []
    posts_all = Posts.objects.filter(username=request.user.username)
    for post in posts_all:
        post.all = False
        posts.append(post)
    # print("Posts >>> ", posts)
    post_id_list = [x.id for x in posts]
    for obj in posts:
        # print("id", obj.id)
        obj.comments = Comments.objects.filter(postid=obj.id)
        # print("objs c>>", obj.comments)
    data['posts'] = posts

    return data


def publish_seller_view(request, isFollow=False):
    """Function helps to publish seller view
    """
    data = {}
    data['url_name'] = "All Posts"
    data['url_uri'] = "all/"

    username = request.user.username
    if isFollow:
        posts = []
        posts_all = Posts.objects.all()
        # Filtering the followed or not one
        for post in posts_all:
            obj_check = PostMap.objects.filter(username=username, postid=post.id)
            # print(">>>>>obj_check",obj_check, post.id, username)
            if obj_check:
                post.followed_post = True
            else:
                post.followed_post = False
            post.all = True
            posts.append(post)
    else:
        if request.method == 'POST':
            # saving follow method
            save_comment(request)
        # finding all post of user and posts 
        follow_objs = PostMap.objects.filter(username=username)
        # print("Followed objs >>", follow_objs)
        posts = []
        for f_obj in follow_objs:
            posts_ = Posts.objects.filter(id=f_obj.postid)
            posts += posts_
        # print("Followed Posts >>", posts)
        posts_all = posts
        posts = []
        for post in posts_all:
            post.all = False
            post.comment_up = True
            posts.append(post)
        # print("Followed Posts2 >>", posts)
        # Forming Comments Objs
        for post in posts:
            # print("id", obj.id)
            c_objs = []
            comments = Comments.objects.filter(username=username, postid=post)
            c_objs += comments
            follow_objs = CommentMap.objects.filter(username=username)
            for f_obj in follow_objs:
                comments = Comments.objects.filter(username=f_obj.username2, postid=post)
                # print("Comment obj>>", c_objs)
                c_objs += comments
            post.comments = c_objs
            # print("objs c>>", post.comments)

    data['posts'] = posts
    # print("Posts >>> ",posts)
    return data


def save_comment(request):
    """Function helps to save the comment objs
    """
    print("Commenting >>>", request.body)
    data_input = request.body
    if isinstance(data_input, bytes):
        data_input = data_input.decode('ascii').split('&')
    # print("Input >> ",data_input)
    username = request.user.username
    postid = 0
    comment_msg = ""
    for input_ in data_input:
        if input_.startswith('comment_msg='):
            comment_msg = input_.replace('comment_msg=', '')
        elif input_.startswith('postid='):
            postid = input_.replace('postid=', '')
    # print("Commenet input >>", username, postid, comment_msg)
    if comment_msg:
        # Getting post obj from database
        post = Posts.objects.filter(pk=postid)
        if post:
            post = post[0]
        if not post:
            return
        # print("Post check >>",post)
        # Saving into comment database
        obj = Comments(postid=post, username=username, comment=comment_msg)
        obj.save()
        print("Saved >>", obj)
    print("-- completed")


def all_posts(request, *args, **kwargs):
    """Function helps to publish all posts
    """
    data = {}
    # print("Request >>>", request)
    try:
        if request.method == 'POST':
            # saving follow method
            save_followup(request)
        if request.user.first_name in (0, '0', None, 'None', 'Buyer'):
            data = publish_buyer_view(request)
        else:
            data = publish_seller_view(request, isFollow=True)

        # forming user list
        username = request.user.username
        user_objs = User.objects.all()
        user_list = []
        for user in user_objs:
            obj_check = CommentMap.objects.filter(username=username, username2=user.username)
            if obj_check:
                user.followed_user = True
            else:
                user.followed_user = False
            user_list.append(user)
        data['user_list'] = user_list

    except:
        traceback.print_exc()
    data['url_name'] = "<< Home Page"
    data['url_uri'] = "/"
    return render(request, 'home.html', data)


def save_followup(request, *args, **kwargs):
    """function helps to save the follow up of posts
    """
    # print("Following >>>", request.body)
    data_input = request.body
    if isinstance(data_input, bytes):
        data_input = data_input.decode('ascii').split('&')
    # print("Input >> ",data_input)
    username = request.user.username
    username2 = ""
    postid = 0
    unfollow = 0
    for input_ in data_input:
        if input_.startswith('username='):
            username2 = input_.replace('username=', '')
        elif input_.startswith('postid='):
            postid = safe_int(input_.replace('postid=', ''))
        elif input_.startswith('unfollow='):
            unfollow = safe_int(input_.replace('unfollow=', ''))
    # print("Follow input >>", username, username2)
    # two types user follow up and post follow up
    # Saving into database
    if username and postid:
        if unfollow:
            obj = PostMap.objects.filter(username=username, postid=postid).delete()
            print("Delete Map Post >>", obj)
        else:
            obj_check = PostMap.objects.filter(username=username, postid=postid)
            # print("Map check >>", obj_check)
            if not obj_check:
                obj = PostMap(username=username, postid=postid)
                obj.save()
                print("Saved Map Post >>", obj)
    if username and username2:
        if unfollow:
            obj = CommentMap.objects.filter(username=username, username2=username2).delete()
            print("Delete Map User >>", obj)
        else:
            obj_check = CommentMap.objects.filter(username=username, username2=username2)
            # print("Map check >>", obj_check)
            if not obj_check:
                obj = CommentMap(username=username, username2=username2)
                obj.save()
                print("Saved Map User >>", obj)
    print("-- completed")
    

def new_post_add(request, *args, **kwargs):
    """Function helps to add new post into system.
    """
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # saving post into database
            form.save()
            # Need to save the user data as well
            post_text = form.cleaned_data.get('post')
            username = request.user.username
            usertype = request.user.first_name
            new_obj = Posts.objects.filter(post=post_text)
            id_list = [x.id for x in new_obj]
            if id_list and username and usertype:
                main_id = id_list[-1]
                # updating post with user info update
                Posts.objects.filter(id=main_id).update(username=username, usertype=usertype)

            return redirect('/')
    else:
        form = AddPostForm()

    return render(request, 'postadd.html', {'form': form})


def safe_int(a, default=0):
    try:
        return int(a)
    except:
        return default








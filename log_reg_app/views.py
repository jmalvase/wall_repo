from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, MessagePost, Comment

def index(request):
    return render(request, 'login.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'all_messages': MessagePost.objects.all()
    }
    return render(request, 'success.html', context)

## LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method=='POST':
        errors = User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        ## encrypting password
        ## store pw in variable
        user_pw = request.POST['password']
        ## hash pw
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        ## test
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/success')
    return redirect('/')

def login(request):
    ## Logging a user in
    if request.method=="POST":
        ## query for logged user:
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            ## compare the passwords
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/success')
    return redirect('/')


##WALL FUNCTIONALITY
def create_mess(request):
    if request.method=="POST":
        error = MessagePost.objects.message_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/success')
        MessagePost.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/success')
    return redirect('/')
def create_comm(request):
    if request.method=="POST":
        Comment.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']), message=MessagePost.objects.get(id=request.POST['message']))
        return redirect('/success')
    return redirect('/')

def like_post(request, message_id):
    liked_message = MessagePost.objects.get(id=message_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

## READ
def profile(request, user_id):
    context={
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'profile.html', context)

## DELETE
def delete_mess(request, message_id):
    MessagePost.objects.get(id=message_id).delete()
    return redirect('/success')
def delete_comm(request, comm_id):
    Comment.objects.get(id=comm_id).delete()
    return redirect('/success')

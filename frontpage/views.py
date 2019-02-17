from django.shortcuts import HttpResponse
import json
from .models import User, Discussion, Post


def index(request):
    return HttpResponse("Frontpage.")


def create_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        u = User(username=json_data["username"], email=json_data["email"])
        u.save()
        return HttpResponse("The user with id %d has been created."%u.id)
    else:
        return HttpResponse("Create user endpoint.")


def delete_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data["id"]
        User.objects.get(id=id).delete()
        return HttpResponse("The user with id %s has been deleted."%id)
    else:
        return HttpResponse("Delete user endpoint.")


def create_discussion(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        key_user = json_data["key_user"]
        title = json_data["title"]
        description = json_data["description"]
        is_private = json_data["is_private"]
        creator = User.objects.get(id=key_user)
        name = "r/subreddit/%s"%title
        d = Discussion(name=name,
                       title=title,
                       description=description,
                       is_private=is_private,
                       creator=creator)
        if is_private:
            d.whitelist.add(creator)
        d.save()
        return HttpResponse("The discussion with id %s has been created."%d.name)
    else:
        return HttpResponse("Create discussion endpoint.")


def add_contributor(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        key_user = json_data["key_user"]
        key_disc = json_data["key_disc"]
        contributor = User.objects.get(id=key_user)
        d = Discussion.objects.get(pk=key_disc)
        d.add_contributor(contributor)
        d.save()
        return HttpResponse("The user with id %s has been whitelisted." % key_user)
    else:
        return HttpResponse("Add contributor endpoint.")


def remove_discussion(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        pk = json_data["id"]
        Discussion.objects.get(pk=pk).delete()
        return HttpResponse("The discussion with id %s has been removed."%pk)
    else:
        return HttpResponse("Remove discussion endpoint.")


def create_post(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        description = json_data["description"]
        key_user = json_data["key_user"]
        key_disc = json_data["key_disc"]
        if "key_parent" in json_data.keys():
            key_parent = json_data["key_parent"]
            parent = Post.objects.get(pk=key_parent)
        else:
            parent = None

        creator = User.objects.get(pk=key_user)
        discussion = Discussion.objects.get(pk=key_disc)
        if discussion.user_can_contribute(creator):
            p = Post(creator = creator,
                     discussion = discussion,
                     parent = parent,
                     description = description)
            p.save()
            return HttpResponse("The post with id %s has been created."%p.id)
        else:
            return HttpResponse("The user with id %s can't contribute to the discussion."%key_user)
    else:
        return HttpResponse("Create post endpoint.")


def remove_post(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        pk = json_data["post"]
        Post.objects.filter(pk=pk).delete()
        return HttpResponse("The post with id %s has been deleted."%pk)
    else:
        return HttpResponse("Remove post endpoint.")


def vote(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        upvoted = json_data["upvoted"]
        element = json_data["element"]
        key_el = json_data["key_element"]
        if element == "discussion":
            el = Discussion.objects.get(pk=key_el)
        elif element == "post":
            el = Post.objects.get(pk=key_el)
        else:
            return "No element"
        if upvoted == '1':
            el.upvoted()
        else:
            el.downvoted()
        el.save()
        return HttpResponse("The vote has been recorded.")
    else:
        return HttpResponse("Vote element endpoint.")


def number_of_votes(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        element = json_data["element"]
        key_el = json_data["key_element"]
        if element == "discussion":
            el = Discussion.objects.get(pk=key_el)
        elif element == "post":
            el = Post.objects.get(pk=key_el)
        else:
            return "No element"
        return HttpResponse("Number of votes: %s" % el.votes())
    else:
        return HttpResponse("Number of votes endpoint.")


def number_of_messages(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        key_el = json_data["key_element"]
        el = Discussion.objects.get(pk=key_el)
        return HttpResponse("Number of messages: %s" % el.number_of_messages())
    else:
        return HttpResponse("Number of messages endpoint.")


def number_of_partecipants(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        key_el = json_data["key_element"]
        el = Discussion.objects.get(pk=key_el)
        return HttpResponse("Number of partecipants: %s" % el.number_of_partecipants())
    else:
        return HttpResponse("Number of partecipants endpoint.")

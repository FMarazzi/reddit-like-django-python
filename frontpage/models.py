from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Discussion(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.SET("[removed]"), related_name='original_poster')
    description = models.CharField(max_length=40000)
    is_private = models.BooleanField()
    whitelist = models.ManyToManyField(User, related_name='users_whitelisted')
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def user_can_contribute(self, user):
        if self.is_private and user not in list(self.whitelist.all()):
            return False
        else:
            return True

    def add_contributor(self, user):
        self.whitelist.add(user)

    def get_whitelisted(self):
        return self.whitelist.all()

    def number_of_messages(self):
        return self.post_set.count()

    def upvoted(self):
        self.like_count += 1

    def downvoted(self):
        self.like_count -= 1

    def votes(self):
        return self.like_count

    def number_of_partecipants(self):
        partecipants = set()
        partecipants.add(self.creator)
        for post in self.post_set.all():
            partecipants.add(post.creator)
        return len(partecipants)


class Post(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET("removed"))
    description = models.CharField(max_length=10000)
    created_date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.SET("removed"), blank=True, null=True)

    def __str__(self):
        return self.discussion.title+"#"+str(self.id)

    def upvoted(self):
        self.like_count += 1

    def downvoted(self):
        self.like_count -= 1

    def votes(self):
        return self.like_count

    def has_parent(self):
        return True if self.parent else False

    def number_of_parents(self):
        if not self.has_parent():
            return 0
        else:
            num = 1
            post = self.parent
            while post.has_parent():
                num += 1
                post = post.parent
            return num

# reddit-like-django-python
Small backend for a site like Reddit build with Django and Python

I built the provided application using Python and the Django framework. 
The requirements for it to work correctly are Python 3.7.2 and Django 2.1.5.

The important files in the package, which are all located in the reddit_like/frontpage folder, are:
  - models.py that contains the models as defined in the Technical document you provided.
  - url.py that enables the endpoints (also providing a nice summary).
  - views.py which contains the methods available for the application.
  - tests.py which contains the TestPipeline class, which is a testing pipeline that allows the user to test the application using the Django built-in test utility (https://docs.djangoproject.com/en/2.1/topics/testing/overview/#running-tests)

I exposed endpoints (as in the views.py file) that accept POST requests with a payload JSON-formatted.

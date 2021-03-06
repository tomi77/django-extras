==================
django-extra-tools
==================

.. image:: https://travis-ci.org/tomi77/django-extra-tools.svg?branch=master
   :target: https://travis-ci.org/tomi77/django-extra-tools
.. image:: https://coveralls.io/repos/github/tomi77/django-extra-tools/badge.svg
   :target: https://coveralls.io/github/tomi77/django-extra-tools?branch=master
.. image:: https://codeclimate.com/github/tomi77/django-extra-tools/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/django-extra-tools
   :alt: Code Climate

Table of contents
=================

* `Installation`_

* `Quick start`_

* `Template filters`_

  * `parse_datetime`_
  * `parse_date`_
  * `parse_time`_
  * `parse_duration`_

* `Aggregation`_

  * `First`_
  * `Last`_
  * `Median`_
  * `StringAgg`_

* `Model mixins`_

  * `CreatedAtMixin`_
  * `CreatedByMixin`_
  * `UpdatedAtMixin`_
  * `UpdatedByMixin`_
  * `DeletedAtMixin`_
  * `DeletedByMixin`_
  * `CreatedMixin`_
  * `UpdatedMixin`_
  * `DeletedMixin`_

* `Database functions`_

  * `batch_qs`_
  * `pg_version`_

* `HTTP Response`_

  * `HttpResponseGetFile`_

* `WSGI Request`_

  * `get_client_ip`_

* `Management`_

  * `OneInstanceCommand`_
  * `NagiosCheckCommand`_

* `Middleware`_

  * `XhrMiddleware`_

* `Auth Backend`_

  * `ThroughSuperuserModelBackend`_

* `Permissions`_

  * `view_(content_types) permissions`_

* `Lockers`_

  * `FileLocker`_
  * `CacheLocker`_

Installation
============

.. sourcecode:: sh

   pip install django-extra-tools

Quick start
===========

Enable ``django-extra-tools``

.. sourcecode:: python

   INSTALLED_APPS = [
       …
       'django_extra_tools',
   ]

Install SQL functions

.. sourcecode:: sh

   python manage.py migrate

Template filters
================

parse_datetime
--------------

Parse datetime from string.

.. sourcecode:: htmldjango

   {% load parse %}

   {{ string_datetime|parse_datetime|date:"Y-m-d H:i" }}

parse_date
----------

Parse date from string.

.. sourcecode:: htmldjango

   {% load parse %}

   {{ string_date|parse_date|date:"Y-m-d" }}

parse_time
----------

Parse time from string.

.. sourcecode:: htmldjango

   {% load parse %}

   {{ string_time|parse_time|date:"H:i" }}

parse_duration
--------------

Parse duration (timedelta) from string.

.. sourcecode:: htmldjango

   {% load parse %}

   {{ string_duration|parse_duration }}

Aggregation
===========

First
-----

Returns the first non-NULL item.

.. sourcecode:: python

   from django_extra_tools.db.models.aggregates import First

   Table.objects.aggregate(First('col1', order_by='col2'))

Last
----

Returns the last non-NULL item.

.. sourcecode:: python

   from django_extra_tools.db.models.aggregates import Last

   Table.objects.aggregate(Last('col1', order_by='col2'))

Median
------

Returns median value.

.. sourcecode:: python

   from django_extra_tools.db.models.aggregates import Median

   Table.objects.aggregate(Median('col1'))

StringAgg
---------

Combines the values as the text. Fields are separated by a "separator".

.. sourcecode:: python

   from django_extra_tools.db.models.aggregates import StringAgg

   Table.objects.aggregate(StringAgg('col1'))

Model mixins
============

CreatedAtMixin
--------------

Add ``created_at`` field to model.

.. sourcecode:: python

   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.CreatedAtMixin, models.Model):
       pass

   model = MyModel()
   print(model.created_at)

CreatedByMixin
--------------

Add ``created_by`` field to model.

.. sourcecode:: python

   from django.contrib.auth.models import User
   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.CreatedByMixin, models.Model):
       pass

   user = User.objects.get(username='user')
   model = MyModel(created_by=user)
   print(model.created_by)

UpdatedAtMixin
--------------

Add ``updated_at`` field to model.

.. sourcecode:: python

   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.UpdatedAtMixin, models.Model):
       operation = models.CharField(max_length=10)

   model = MyModel()
   print(model.updated_at)
   model.operation = 'update'
   model.save()
   print(model.updated_at)

UpdatedByMixin
--------------

Add ``updated_by`` field to model.

.. sourcecode:: python

   from django.contrib.auth.models import User
   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.UpdatedByMixin, models.Model):
       operation = models.CharField(max_length=10)

   user = User.objects.get(username='user')
   model = MyModel()
   print(model.updated_by)
   model.operation = 'update'
   model.save_by(user)
   print(model.updated_by)

DeletedAtMixin
--------------

Add ``deleted_at`` field to model.

.. sourcecode:: python

   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.DeletedAtMixin, models.Model):
       pass

   model = MyModel()
   print(model.deleted_at)
   model.delete()
   print(model.deleted_at)

DeletedByMixin
--------------

Add ``deleted_by`` field to model.

.. sourcecode:: python

   from django.contrib.auth.models import User
   from django.db import models
   from django_extra_tools.db.models import timestampable

   class MyModel(timestampable.DeletedByMixin, models.Model):
       pass

   user = User.objects.get(username='user')
   model = MyModel()
   print(model.deleted_by)
   model.delete_by(user)
   print(model.deleted_by)

CreatedMixin
------------

Add ``created_at`` and ``created_by`` fields to model.

UpdatedMixin
------------

Add ``updated_at`` and ``updated_by`` fields to model.

DeletedMixin
------------

Add ``deleted_at`` and ``deleted_by`` fields to model.

Database functions
==================

batch_qs
--------

Returns a (start, end, total, queryset) tuple for each batch in the given queryset.

.. sourcecode:: python

   from django_extra_tools.db.models import batch_qs

   qs = Table.objects.all()
   start, end, total, queryset = batch_qs(qs, 10)

pg_version
----------

Return tuple with PostgreSQL version of a specific connection.

.. sourcecode:: python

   from django_extra_tools.db.models import pg_version

   version = pg_version()

HTTP Response
=============

HttpResponseGetFile
-------------------

An HTTP response class with the "download file" headers.

.. sourcecode:: python

   from django_extra_tools.http import HttpResponseGetFile

   return HttpResponseGetFile(filename='file.txt', content=b'file content', content_type='file/text')

WSGI Request
============

get_client_ip
-------------

Get the client IP from the request.

.. sourcecode:: python

   from django_extra_tools.wsgi_request import get_client_ip

   ip = get_client_ip(request)

You can configure list of local IP's by setting ``PRIVATE_IPS_PREFIX``

.. sourcecode:: python

   PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

Management
==========

OneInstanceCommand
------------------

A management command which will be run only one instance of command with
name ``name``. No other command with name ``name`` can not be run in the
same time.

.. sourcecode:: python

   from django_extra_tools.management import OneInstanceCommand

   class Command(OneInstanceCommand):
       name = 'mycommand'

       def handle_instance(self, *args, **options):
           # some operations

       def lock_error_handler(self, exc):
           # Own error handler
           super(Command, self).lock_error_handler(exc)

NagiosCheckCommand
------------------

A management command which perform a Nagios check.

.. sourcecode:: python

   from django_extra_tools.management import NagiosCheckCommand

   class Command(NagiosCheckCommand):
       def handle_nagios_check(self, *args, **options):
           return self.STATE_OK, 'OK'

Middleware
==========

XhrMiddleware
-------------

This middleware allows cross-domain XHR using the html5 postMessage API.

.. sourcecode:: python

   MIDDLEWARE_CLASSES = (
       ...
       'django_extra_tools.middleware.XhrMiddleware'
   )

   XHR_MIDDLEWARE_ALLOWED_ORIGINS = '*'
   XHR_MIDDLEWARE_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
   XHR_MIDDLEWARE_ALLOWED_HEADERS = ['Content-Type', 'Authorization', 'Location', '*']
   XHR_MIDDLEWARE_ALLOWED_CREDENTIALS = 'true'
   XHR_MIDDLEWARE_EXPOSE_HEADERS = ['Location']

Auth Backend
============

ThroughSuperuserModelBackend
----------------------------

Allow to login to user account through superuser login and password.

Add ``ThroughSuperuserModelBackend`` to ``AUTHENTICATION_BACKENDS``:

.. sourcecode:: python

   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.ModelBackend',
       'django_extra_tools.auth.backends.ThroughSuperuserModelBackend',
   )

Optionally You can configure username separator (default is colon):

.. sourcecode:: python

   AUTH_BACKEND_USERNAME_SEPARATOR = ':'

Now You can login to user account in two ways:

* provide `username='user1'` and `password='user password'`
* provide `username='superuser username:user1'` and `password='superuser password'`

Permissions
===========

view_(content_types) permissions
--------------------------------

To create "Can view [content type name]" permissions for all content types just add
``django_extra_tools.auth.view_permissions`` at the end of ``INSTALLED_APPS``

.. sourcecode:: python

   INSTALLED_APPS = [
       …
       'django_extra_tools.auth.view_permissions'
   ]

and run migration

.. sourcecode:: sh

   python manage.py migrate

Lockers
=======

Function to set lock hook.

.. sourcecode:: python

   from django_extra_tools.lockers import lock

   lock('unique_lock_name')

Next usage of `lock` on the same lock name raises ``LockError`` exception.

You can configure locker mechanism through ``DEFAULT_LOCKER_CLASS`` settings or directly:

.. sourcecode:: python

   from django_extra_tools.lockers import FileLocker

   lock = FileLocker()('unique_lock_name')

FileLocker
----------

This is a default locker.

This locker creates a `unique_lock_name.lock` file in temp directory.

You can configure this locker through settings:

.. sourcecode:: python

   DEFAULT_LOCKER_CLASS = 'django_extra_tools.lockers.FileLocker'

CacheLocker
-----------

This locker creates a `locker-unique_lock_name` key in cache.

You can configure this locker through settings:

.. sourcecode:: python

   DEFAULT_LOCKER_CLASS = 'django_extra_tools.lockers.CacheLocker'

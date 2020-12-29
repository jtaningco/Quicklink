# Quicklink
Quicklink is a full-stack web project for our class, **ITMGT45: The Digital Economy**.

## Setup

1. Create a python environment with [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) or [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 

2. Activate the newly created virtual environment.

3. Setup a mySQL database. [Mac](https://medium.com/macoclock/mysql-on-mac-getting-started-cecb65b78e#:~:text=From%20System%20Preferences%2C%20open%20MySQL,launch%20MySQL%20from%20System%20Preferences.) [Windows](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_MySQL.htm) 
   
4. Create a new `.env` file in the `config/settings` folder. Template is in `.env.example`. 
  
5. Install dependencies with `pip install -r requirements/local.txt`.

6. Create a superuser with `python manage.py createsuperuser` 

7. Migrate database with `python manage.py migrate` 

8. Start development server with `python manage.py runserver`

## Directory Structure

    django-boilerplate/
        apps/
            foo/
                templates/
                     foo/
                        foo.html
                models.py
                views.py
                forms.py
        config/
            settings.py
            wsgi.py
            urls.py
        lib/
        static/
            css/
                vendor/
            js/
                vendor/
            images/
        requirements/
            common.txt
            dev.txt
            production.txt
        templates/
        environment.py
        fabfile.py
        manage.py
        settings.py

### apps

All of your Django "apps" go in this directory. These have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.

### config

Contains all the configuration of your Django installation. This includes the `settings.py` (Django app bootstrapper), `wsgi.py` (App production bootstrapper), and `urls.py` (Define URLs served by all apps and nodes)

### lib

Python packages and modules that aren't true Django 'apps' - i.e. they don't
have their own models, views or forms. These are just regular Python classes and
methods, and they don't go in the `INSTALLED_APPS` list of your project's
settings file. 

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.

### static

A subfolder each for CSS, Javascript and images. Third-party files (e.g. the
960.gs CSS or jQuery) go in a `vendor/` subfolder to keep your own code
separate.

### requirements

pip requirements files, optionally one for each app environment. The
`common.txt` is installed in every case.

Our Fabfile (see below) installs the project's dependencies from these files.
It's an attempt to standardize the location for dependencies like Rails'
`Gemfile`. We also specifically avoid listing the dependencies in the README of
the project, since a list there isn't checked programmatically or ever actually
installed, so it tends to quickly become out of date.

### templates

Project-wide templates (i.e. those not belonging to any specific app in the
`apps/` folder). The boilerplate includes a `base.html` template that defines
these blocks:

#### <head>

`title` - Text for the browser title bar. You can set a default here and
append/prepend to it in sub-templates using `{{ super }}`.

`site_css` - Primary CSS files for the site. By default, includes
`media/css/reset.css` and `media/css/base.css`. 

`css` - Optional page-specific CSS - empty by default. Use this block if a page
needs an extra CSS file or two, but doesn't want to wipe out the files already
linked via the `site_css` block.

`extra_head` - Any extra content for between the `<head>` tags.

#### <body>

`header` - Top of the body, inside a `div` with the ID `header`.

`content` - After the `header`, inside a `div` with the ID `content`.

`footer` - After `content`, inside a `div` with the ID `footer`.

`site_js` - After all body content, includes site-wide Javascript files. By
default, includes `media/js/application.js` and jQuery. In deployed
environments, links to a copy of jQuery on Google's CDN. If running in solo
development mode, links to a local copy of jQuery from the `media/` directory -
because the best way to fight snakes on a plane is with jQuery on a plane.

`js` - Just like the `css` block, use the `js` block for page-specific
Javascript files when you don't want to wipe out the site-wide defaults in
`site_js`.

### Files

#### environment.py

Modifies the `PYTHONPATH` to allow importing from the `apps/`, `lib/` and
`vendor/` directories. This module is imported at the top of `settings.py` to
make sure it runs for both local development (using Django's built-in server)
and in production (run through mod-wsgi, gunicorn, etc.).

#### fabfile.py

We use [Fabric](http://fabfile.org/) to deploy to remote servers in development,
staging and production environments. The boilerplate Fabfile is quite thin, as
most of the commands are imported from [buedafab](https://github.com/bueda/ops),
a collection of our Fabric utilities.

#### manage.py

The standard Django `manage.py`.

#### settings.py

Many good default settings for Django applications - check the file for more
detailed documentation.

#### urls.py

Barebones `url_patterns` to serve static media when in solo development mode.

*Boilerplate code from https://github.com/bueda/django-boilerplate and https://github.com/app-generator/boilerplate-code-django*

# Quicklink
Quicklink is a full-stack stand-alone web application for our class, **ITMGT45: The Digital Economy**.

## Setup

1. Create a python environment with [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) or [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 

2. Activate the newly created virtual environment. [Alternative tutorial](https://medium.com/@diwassharma/starting-a-python-django-project-on-mac-os-x-c089165cf010)

3. Setup a mySQL database. [Mac](https://medium.com/macoclock/mysql-on-mac-getting-started-cecb65b78e#:~:text=From%20System%20Preferences%2C%20open%20MySQL,launch%20MySQL%20from%20System%20Preferences.) [Windows](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_MySQL.htm) 
   
4. Create a new `.env` file in the `config/settings` folder. Template is in `.env.example`. 
  
5. Install dependencies with `pip install -r requirements/local.txt`.

6. Create a superuser with `python manage.py createsuperuser` 

7. Migrate database with `python manage.py migrate` 

8. Start development server with `python manage.py runserver`

## Directory Structure

    Quicklink/
        apps/                       # project-specific applications
            __init__.py
            foo/
                templates/
                     foo/
                        foo.html
                models.py
                views.py
                forms.py
        config/                     # site settings
            .env.example
            settings.py
            wsgi.py
            urls.py
        docs/                       # documentation
        static/                     # site-specific static files
            css/
                vendor/
            js/
                vendor/
            images/
        requirements/               # pip requirements files per environment
            base.txt
            local.txt
            production.txt
        templates/                  # site-specific templates
        fabfile.py
        manage.py

### apps

All of your Django "apps" go in this directory. These have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.

### config

Contains all the configuration of your Django installation. This includes the `settings.py` (Django app bootstrapper), `wsgi.py` (App production bootstrapper), and `urls.py` (Define URLs served by all apps and nodes)

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

I put these templates and static files into global templates/static directory, not inside each app. These files are usually edited by people, who doesn't care about project code structure or python at all. If you are full-stack developer working alone or in a small team, you can create per-app templates/static directory. It's really just a matter of taste.

The same applies for locale, although sometimes it's convenient to create separate locale directory.

Tests are usually better to place inside each app, but usually there is many integration/functional tests which tests more apps working together, so global tests directory does make sense.

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

#### fabfile.py

We use [Fabric](http://fabfile.org/) to deploy to remote servers in development,
staging and production environments. The boilerplate Fabfile is quite thin, as
most of the commands are imported from [buedafab](https://github.com/bueda/ops),
a collection of our Fabric utilities.

#### manage.py

The standard Django `manage.py`.

*Boilerplate code from 
https://github.com/bueda/django-boilerplate
https://github.com/app-generator/boilerplate-code-django*
https://stackoverflow.com/questions/22841764/best-practice-for-django-project-working-directory-structure

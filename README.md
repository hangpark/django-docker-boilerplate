# Boilerplate for Django with Docker

## Specification

### Django

* **Internalization** - django-modeltranslation
* **Localization** - Custom middleware
* **Template Engine** - Jinja2
* **WSGI** - uWSGI
* **Database Connector** - PyMySQL
* **Document** - Sphinx

### Frontend

* **Package Manager** - NPM, Bower
* **Build System** - gulp.js
* **Libraries** jQuery, Bootstrap-sass, Font Awesome

### Docker

* `Dockerfile` is given. Just build it!

## How to setup your own project in 10 steps

**1. Clone the repository on your local machine and delete git.**

```sh
$ git clone --depth=1 https://github.com/hangpark/django-docker-boilerplate.git {{your-proj-name}}
$ cd !$
$ rm -rf .git
```

**2. Change every occurrence `exampleproject` to your project name.**

```sh
$ mv exampleproject {{your-proj-name}}
$ find . -type f -exec sed -i 's/exampleproject/{{your-proj-name}}/g' {} \;
```

**3. Modify meta information of your project.** *(OPTIONAL to impatients)*

- `README.md`
- `docs/conf.py`
- `docs/index.rst`
- `package.json`
- `bower.json`

**4. Choose HTTP-only or HTTP/HTTPS support range.**

```sh
$ cp nginx-https-support.conf nginx.conf
```

OR

```sh
$ cp nginx-http-only.conf nginx.conf
```

**5. Pull MySQL docker image.**

```sh
$ sudo docker pull mysql/mysql-server:5.7
```

**6. Run database container.**

```sh
$ sudo docker run --name {{your-proj-name}}-db \
> -v {{abs-path-for-proj-dir}}/mysql.cnf:/etc/my.cnf \
> -e MYSQL_USER={{mysql-username}} \
> -e MYSQL_PASSWORD={{mysql-password}} \
> -e MYSQL_DATABASE={{your-proj-name}} \
> -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
> -d mysql/mysql-server:5.7
```

**7. Build docker image.**

```sh
$ sudo docker build --tag {{your-proj-name}} .
```

It takes a long time.

**8. Run web server container.**

```sh
$ sudo docker run --name {{your-proj-name}} \
> -v {{abs-path-for-cert}}:/etc/{{your-proj-name}} \
> --link {{your-proj-name}}-db:db \
> -p 80:80 \
> -p 443:443 \
> -d {{your-proj-name}}
```

`-v {{abs-path-for-cert}}:/etc/{{your-proj-name}}` and `-p 443:443` are only for HTTPS supporting. You need below files at `{{abs-path-for-cert}}` directory:

- `fullchain.pem`
- `privkey.pem`
- `dhparam.pem`

and you can make `dhparam.pem` easily by:

```sh
$ openssl dhparam -out dhparam.pem 4096
```

**9. Check `localhost` in your browser.**

- http://localhost/

Does it works?

**10. Make an initial commit.**

```sh
$ git init
$ git add .
$ git commit -m "Initial commit"
```

## How to run not using Docker in 10 steps

This boilerplate has two setting files for **local** and **production**, respectively and you can configure it inside `{{your-proj-name}}.settings` package. They're sharing common settings in `{{your-proj-name}}.settings.base`.

To run your project without docker (perhaps on your local machine), just follow few steps below.

From now on, we assume that you've done up to **step 3** above already.

**4. Install dependencies for back- and front-end.**

```sh
$ pip install -r requirements.txt
$ npm install
$ bower install
```

**5. Packaging front-end sources.**

```sh
$ gulp
```

If `gulp` is not founded globally, run following command instead:

```sh
$ ./node_modules/gulp/bin/gulp.js
```

**6. Compile documentation** *(Optional to whom not need docs)*

```sh
$ cd docs
$ make html
```

**7. Setting up Django project**

On your project's root directory,

```sh
$ export DJANGO_SETTINGS_MODULE={{your-proj-name}}.settings.local
$ python manage.py migrate
$ python manage.py collectstatic
```

Of course, you can specify setting files explicitly if you want like

```sh
$ python manage.py {{command}} --settings={{your-proj-name}}.settings.local
```

**8. Run server**

```sh
$ python manage.py runserver
```

**9. Check `localhost` in your browser.**

- http://localhost:8000/

Does it works?

**10. Develop your project!**

For stylesheets, you may want to see `./static/src/scss/*` which uses Bootstrap-sass that you can freely modify.

For javascripts, add your code in `./static/src/js`.

As we've done above, you can update your front-end sources via

```sh
$ gulp
$ python manage.py
```

more shortly,

```sh
$ gulp && ./manage.py --no-input
```
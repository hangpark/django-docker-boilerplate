# Boilerplate for Django with Docker

## Django

* **Internalization** - django-modeltranslation
* **Localization** - Custom middleware
* **Template Engine** - Jinja2
* **WSGI** - uWSGI
* **Database Connector** - PyMySQL
* **Document** - Sphinx

## Frontend

* **Package Manager** - NPM, Bower
* **Build System** - gulp.js
* **Libraries** jQuery, Bootstrap-sass, Font Awesome

## Docker

* Dockerfile is given. Just build it!

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

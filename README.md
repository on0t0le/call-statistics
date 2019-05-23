# Project for call-statistics
Consists of:
- WebSite on Angular
- WebApi on Python
- Proxy on Nginx

### Requirements:
For Api set proper environments in db.env:
```sh
- dbServer=db_location
- dbLogin=login_username
- dbPassword=youre_strong_password
```

In proxy config-file set proper IP-s of **Backend** and **Frontend**

Create Docker-volume and mount samba-folder w/ call recordings.
```sh
$ docker volume create sound
$ sudo mount //servername/sharename  /var/lib/docker/volumes/sound/_data  cifs  username=msusername,password=mspassword,iocharset=utf8,sec=ntlm,file_mode=0755,dir_mode=0755  0  0
```

### Run App
For starting app use docker-compose:
```sh
$ docker-compose up -d
```

Web site souce code located in [Github Repo](https://github.com/on0t0le/statistics-web-site).
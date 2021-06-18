GitLab
======== 

## Installing a GitLab runner locally as Docker container service 

[root@NetboX ~]# `docker run -d --name gitlab-runner --restart always \` <br/>
` -v /srv/gitlab-runner/config:/etc/gitlab-runner \` <br/>
` -v /var/run/docker.sock:/var/run/docker.sock \` <br/>
` gitlab/gitlab-runner:latest` <br/>
```
Unable to find image 'gitlab/gitlab-runner:latest' locally
latest: Pulling from gitlab/gitlab-runner
345e3491a907: Pull complete
57671312ef6f: Pull complete
5e9250ddb7d0: Pull complete
ae2adeb99b82: Pull complete
812317101c65: Pull complete
c6711e7ac28c: Pull complete
dd1fba12eaaa: Pull complete
Digest: sha256:44140075dbdb2208c8d7a2ea3cd48e0e30c8534f2b26716ea9604a5460ace936
Status: Downloaded newer image for gitlab/gitlab-runner:latest
2f4286e86cc07b3c6c4fa20a4fa232bcd224fc124b8c4174778b85cd70f5c784
[root@NetboX ~]#
```
[root@NetboX ~]# ` docker ps | grep gitlab `
```
2f4286e86cc0   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   21 seconds ago   Up 18 seconds                                                             gitlab-runner
[root@NetboX ~]#
```

## Registering GitLab runner to https://gitlab.com
 ### 1. First create repo in [Git](https://gitlab.com)
 ### 2. Get the registration token from Project > Settings > CI/CD > Runners (Expand) > Set up a specific runner manually

[root@NetboX ~]# ` docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner register `
```
Runtime platform                                    arch=amd64 os=linux pid=7 revision=7a6612da version=13.12.0
Running in system-mode.

Enter the GitLab instance URL (for example, https://gitlab.com/):
https://gitlab.com/
Enter the registration token:
v4yssoXXXXXXXXXXXXX
Enter a description for the runner:
[9e93d69ffdf0]: gitlab-runner-boburciu
Enter tags for the runner (comma-separated):
dell-switch-automation
Registering runner... succeeded                     runner=v4yssoSv
Enter an executor: virtualbox, docker+machine, docker-ssh, docker, parallels, shell, ssh, docker-ssh+machine, kubernetes, custom:
shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
[root@NetboX ~]#
```

 ### 3. The GitLab runner configuration
[root@NetboX ~]# ` ls -lt /srv/gitlab-runner/config/ `
```        
total 4
-rw-------. 1 root root 328 Jun 17 16:48 config.toml
```
[root@NetboX ~]# ` cat /srv/gitlab-runner/config/config.toml `
```
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "gitlab-runner-boburciu"
  url = "https://gitlab.com/"
  token = "3MZATrXXXXXXXXXXXXX"
  executor = "shell"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
[root@NetboX ~]#
```

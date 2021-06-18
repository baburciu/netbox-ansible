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

## Enabling GitLab runner Docker container to SSH other hosts with private key  

 ### There's a specific user called _gitlab-runner_ or _gitlab_ci_multi_runner_ used by the GitLab runner, per [Shell executor doc](https://docs.gitlab.com/runner/executors/shell.html#running-as-unprivileged-user)
 
[root@gitlab-runner-and-netbox ~]# ` docker ps | grep gitlab `  <br/>
```
4370c00a1815   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   54 minutes ago   Up 54 minutes                                                             gitlab-runner
```
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 4370c00a1815 sh ` <br/>
```
# cat /etc/passwd | grep gitlab
gitlab-runner:x:999:999:GitLab Runner:/home/gitlab-runner:/bin/bash
#
# ls -lat /home/gitlab-runner/
total 8
drwxr-xr-x. 3 gitlab-runner gitlab-runner   51 Jun 18 09:18 .
drwxrwxr-x. 3 gitlab-runner gitlab-runner   22 Jun 18 09:18 builds
drwxr-xr-x. 1 root          root            27 May 20 16:10 ..
-rw-r--r--. 1 gitlab-runner gitlab-runner 3771 Feb 25  2020 .bashrc
-rw-r--r--. 1 gitlab-runner gitlab-runner  807 Feb 25  2020 .profile
#
# mkdir /home/gitlab-runner/.ssh/
# chmod 700 /home/gitlab-runner/.ssh/
```
[root@gitlab-runner-and-netbox ~]# ` docker cp ~/.ssh/id_rsa 4370c00a1815:/home/gitlab-runner/.ssh/id_rsa ` <br/>
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 4370c00a1815 ls /home/gitlab-runner/.ssh/ ` <br/>
```
id_rsa
[root@gitlab-runner-and-netbox ~]#
```
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 4370c00a1815 sh `
```
# ssh -i /home/gitlab-runner/.ssh/id_rsa 192.168.200.23
The authenticity of host '192.168.200.23 (192.168.200.23)' can't be established.
ECDSA key fingerprint is SHA256:IfdH2PbTRJ9k+Bi+N9Q/7O4C+uEyBX55IaV/c3I2n7Y.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.200.23' (ECDSA) to the list of known hosts.
Last login: Fri Jun 18 13:31:18 2021 from 192.168.200.222
[root@NetboX ~]# exit
logout
Connection to 192.168.200.23 closed.
# 
# exit
[root@gitlab-runner-and-netbox ~]#
```

## Writing CI file assumes usage of [keyword reference for the .gitlab-ci.yml file](https://docs.gitlab.com/ee/ci/yaml/)

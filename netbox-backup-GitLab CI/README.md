GitLab runners
========
  - [Installing a GitLab runner locally as Docker container service](#installing-a-gitlab-runner-locally-as-docker-container-service)
  - [Registering GitLab runner to https://gitlab.com](#registering-gitlab-runner-to-httpsgitlabcom)
    - [1. First create repo in Git](#1-first-create-repo-in-git)
    - [2. Get the registration token from Project > Settings > CI/CD > Runners (Expand) > Set up a specific runner manually](#2-get-the-registration-token-from-project--settings--cicd--runners-expand--set-up-a-specific-runner-manually)
    - [3. The GitLab runner configuration](#3-the-gitlab-runner-configuration)
  - [Registering GitLab runner to private GitLab instance](#registering-gitlab-runner-to-private-gitlab-instance)
    - [1. Running behind Forward Proxy](#1-running-behind-forward-proxy)
      - [1.1 Configure Docker Daemon to use proxy (This configuration is used by docker daemon to pull images from Docker Hub)](#11-configure-docker-daemon-to-use-proxy-this-configuration-is-used-by-docker-daemon-to-pull-images-from-docker-hub)
      - [1.2 Restart docker](#12-restart-docker)
      - [1.3 Verify that the configuration has been loaded](#13-verify-that-the-configuration-has-been-loaded)
      - [1.4 Configure Docker Client to pass proxy information to containers](#14-configure-docker-client-to-pass-proxy-information-to-containers)
      - [New containers will have the HTTPS proxy set:](#new-containers-will-have-the-https-proxy-set)
    - [2. Configure GitLab server certificate as trusted for TLS handshake from runner](#2-configure-gitlab-server-certificate-as-trusted-for-tls-handshake-from-runner)
      - [2.1 Get cert from unmanaged GitLab from Mozilla browser: View Certificate -> Intermediate -> Download PEM (cert)](#21-get-cert-from-unmanaged-gitlab-from-mozilla-browser-view-certificate---intermediate---download-pem-cert)
      - [2.2 Save cert to the GitLab runner container location:](#22-save-cert-to-the-gitlab-runner-container-location)
    - [3. Get the registration token from Project > Settings > CI/CD > Runners (Expand) > Set up a specific runner manually and then register (via proxy and using certificate by option *--tls-ca-file=/path/to/cert*)](#3-get-the-registration-token-from-project--settings--cicd--runners-expand--set-up-a-specific-runner-manually-and-then-register-via-proxy-and-using-certificate-by-option---tls-ca-filepathtocert)
  - [To setup GitLab Pipeline you need to set the path to *.gitlab-ci.yml* in Project > Settings > CI/CD > General pipelines (Expand) > Custom CI configuration path, following the official guide, for example to *NetBox/NetBox config backup/.gitlab-ci.yml* for a CI file located in Project named *Admin/NetBox/NetBox config backup/.gitlab-ci.yml*](#to-setup-gitlab-pipeline-you-need-to-set-the-path-to-gitlab-ciyml-in-project--settings--cicd--general-pipelines-expand--custom-ci-configuration-path-following-the-official-guide-for-example-to-netboxnetbox-config-backupgitlab-ciyml-for-a-ci-file-located-in-project-named-adminnetboxnetbox-config-backupgitlab-ciyml)
  - [To have the GitLab runner SSH to another machine](#to-have-the-gitlab-runner-ssh-to-another-machine)
    - [1. You need to create SSH key pair, add the .pub one to *~/.ssh/authorized_keys* on the target machine and add the private key to the runner container](#1-you-need-to-create-ssh-key-pair-add-the-pub-one-to-sshauthorized_keys-on-the-target-machine-and-add-the-private-key-to-the-runner-container)
    - [2. Have the private key owned by the *gitlab-runner* user](#2-have-the-private-key-owned-by-the-gitlab-runner-user)
  - [Using Docker-in-Docker executor behind proxy](#using-docker-in-docker-executor-behind-proxy)

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

***

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

***

## Registering GitLab runner to private GitLab instance
 ### 1. Running behind Forward Proxy
 #### 1.1 Configure Docker Daemon to use proxy (This configuration is used by docker daemon to pull images from Docker Hub)
[root@gitlab-runner-and-netbox ~]# ` vim /etc/systemd/system/docker.service.d/http-proxy.conf ` <br/>
[root@gitlab-runner-and-netbox ~]# ` cat /etc/systemd/system/docker.service.d/http-proxy.conf ` <br/>
```
[Service]
Environment="HTTP_PROXY=http://192.168.X.X:8080"
Environment="HTTPS_PROXY=http://192.168.X.X:8080"
```
[root@gitlab-runner-and-netbox ~]#
 #### 1.2 Restart docker
[root@gitlab-runner-and-netbox ~]# ` systemctl daemon-reload ` <br/>
[root@gitlab-runner-and-netbox ~]# ` systemctl restart docker ` <br/>

 #### 1.3 Verify that the configuration has been loaded
 [root@gitlab-runner-and-netbox ~]# ` systemctl show --property=Environment docker `
Environment=HTTP_PROXY=http://192.168.X.X:8080 HTTPS_PROXY=https://192.168.X.X:8080

 #### 1.4 Configure Docker Client to pass proxy information to containers
[root@gitlab-runner-and-netbox ~]# ` vim ~/.docker/config.json ` <br/>
[root@gitlab-runner-and-netbox ~]# ` cat ~/.docker/config.json ` <br/>
```
{
 "proxies":
 {
   "default":
   {
     "httpProxy": "http://192.168.X.X:8080",
     "httpsProxy": "http://192.168.X.X:8080"
   }
 }
}
[root@gitlab-runner-and-netbox ~]#
```
 #### New containers will have the HTTPS proxy set:
[root@NetboX ~]# `docker run -d --name gitlab-runner-behind-feper-proxy --restart always \` <br/>
` -v /srv/gitlab-runner/config:/etc/gitlab-runner \` <br/>
` -v /var/run/docker.sock:/var/run/docker.sock \` <br/>
` gitlab/gitlab-runner:latest` <br/> 
```
08f8586e6fc5582e940fda04aa918bcd0bd1fe049cf8e4e1b43b7718a2fd0e23
[root@gitlab-runner-and-netbox ~]#
[root@gitlab-runner-and-netbox ~]# docker ps | grep gitlab-runner
08f8586e6fc5   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   4 seconds ago   Up 4 seconds             gitlab-runner-behind-feper-proxy
4370c00a1815   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   10 days ago     Up 3 minutes             gitlab-runner
[root@gitlab-runner-and-netbox ~]#
[root@gitlab-runner-and-netbox ~]#
```
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 08f8586e6fc5 curl -k https://private-gitlab.internal -v `    
```
* Uses proxy env variable https_proxy == 'http://192.168.X.X:8080' 
*   Trying 192.168.X.X:8080...
* TCP_NODELAY set
* Connected to 192.168.X.X (192.168.X.X) port 8080 (#0)
* allocate connect buffer!
* Establish HTTP proxy tunnel to private-gitlab.internal:443
> CONNECT private-gitlab.internal:443 HTTP/1.1
> Host: private-gitlab.internal:443
> User-Agent: curl/7.68.0
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 200 Connection established
<
* Proxy replied 200 to CONNECT request
* CONNECT phase completed!
:
:
<
* Connection #0 to host 192.168.X.X left intact
<html><body>You are being <a href="https://private-gitlab.internal/users/sign_in">redirected</a>.</body></html>[root@gitlab-runner-and-netbox ~]# 
```

 ### 2. Configure GitLab server certificate as trusted for TLS handshake from runner
 #### 2.1 Get cert from unmanaged GitLab from Mozilla browser: View Certificate -> Intermediate -> Download PEM (cert)
 #### 2.2 Save cert to the GitLab runner container location:
[root@gitlab-runner-and-netbox ~]# ` ls -lt /srv/gitlab-runner/config `
```
total 11
-rw-------. 1 root root  659 Jun 28 17:20 config.toml
[root@gitlab-runner-and-netbox ~]#
```
[root@gitlab-runner-and-netbox ~]# ` vim /srv/gitlab-runner/config/private-gitlab.internal.pem ` <br/>
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 08f8586e6fc5 ls -lt /etc/gitlab-runner ` <br/>
```
total 12
-rw-r--r--. 1 root root 6401 Jun 28 14:16 private-gitlab.internal.pem
-rw-------. 1 root root  321 Jun 18 09:13 config.toml
```

 ### 3. Get the registration token from Project > Settings > CI/CD > Runners (Expand) > Set up a specific runner manually and then register (via proxy and using certificate by option *--tls-ca-file=/path/to/cert*)
[root@gitlab-runner-and-netbox ~]# ` docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner register --tls-ca-file=/etc/gitlab-runner/private-gitlab.internal.pem `
```
Runtime platform                                    arch=amd64 os=linux pid=8 revision=7a6612da version=13.12.0
Running in system-mode.

Enter the GitLab instance URL (for example, https://gitlab.com/):
https://private-gitlab.internal/
Enter the registration token:
D91zGZBW6c3ed6Eo226y
Enter a description for the runner:
[8a9862ee6dc7]: feper-gitlab-runner
Enter tags for the runner (comma-separated):
feper-gitlab-runner
Registering runner... succeeded                     runner=D91zGZBW
Enter an executor: docker-ssh, shell, ssh, docker+machine, docker-ssh+machine, custom, parallels, virtualbox, kubernetes, docker:
shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
[root@gitlab-runner-and-netbox ~]# 
```

***

## To setup GitLab Pipeline you need to set the path to *.gitlab-ci.yml* in Project > Settings > CI/CD > General pipelines (Expand) > Custom CI configuration path, following the [official guide](https://docs.gitlab.com/ee/ci/pipelines/settings.html#custom-cicd-configuration-file), for example to *NetBox/NetBox config backup/.gitlab-ci.yml* for a CI file located in Project named *Admin/NetBox/NetBox config backup/.gitlab-ci.yml*

***

## To have the GitLab runner SSH to another machine
 ### 1. You need to create SSH key pair, add the .pub one to *~/.ssh/authorized_keys* on the target machine and add the private key to the runner container
 ### 2. Have the private key owned by the *gitlab-runner* user
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 08f8586e6fc5 chown -R gitlab-runner:gitlab-runner /home/gitlab-runner `
[root@gitlab-runner-and-netbox ~]# ` docker exec -it 08f8586e6fc5 stat /home/gitlab-runner/.ssh/id_rsa `
```
  File: /home/gitlab-runner/.ssh/id_rsa
  Size: 1675            Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d    Inode: 68192253    Links: 1
Access: (0600/-rw-------)  Uid: (  999/gitlab-runner)   Gid: (  999/gitlab-runner)
Access: 2021-06-28 16:57:36.078703652 +0000
Modify: 2021-06-28 16:57:17.909704589 +0000
Change: 2021-06-29 11:10:39.012321329 +0000
 Birth: -
[root@gitlab-runner-and-netbox ~]#
```

## Using Docker-in-Docker executor behind proxy
GitLab Runner does not require a restart when you change most options. This includes parameters in the [[runners]] section and most parameters in the global section, except for listen_address. If a runner was already registered, you don’t need to register it again.
GitLab Runner checks for configuration modifications every 3 seconds and reloads if necessary.
More on runner configuration on [advanced page](https://docs.gitlab.com/runner/configuration/advanced-configuration.html).
```shell
root@capi-bootstrap-capd-bb:/home/ubuntu/telco-cloud/capi-bootstrap# ip r sh dev docker0
172.17.0.0/16 proto kernel scope link src 172.17.0.1
root@capi-bootstrap-capd-bb:/home/ubuntu/telco-cloud/capi-bootstrap# cat /srv/gitlab-runner/config/config.toml
concurrent = 5
check_interval = 0
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "my-runner"
  url = "https://gitlab.com/"
  id = 20131826
  token = "XXXX"
  token_obtained_at = 2023-01-04T08:39:11Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  environment = ["HTTPS_PROXY=http://1.2.3.4:3128", "HTTP_PROXY=http://1.2.3.4:3128", "NO_PROXY=172.17.0.0/16"]    # will inject env vars to DinD containers, otherwise missing since ~/.docker/config.json is only for Docker Client to pass proxy information to containers, while DinD are created by GitLab .gitlab-ci.yml 
  pre_clone_script = "git config --global http.proxy $HTTP_PROXY; git config --global https.proxy $HTTPS_PROXY"    # have DinD containers run git commands behind proxy
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "alpine:3.15"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
root@capi-bootstrap-capd-bb:/home/ubuntu/telco-cloud/capi-bootstrap# 
```

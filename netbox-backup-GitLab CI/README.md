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
    - [runner config when behind a proxy](#runner-config-when-behind-a-proxy)
    - [have dockerd exposed on localhost tcp:2375](#have-dockerd-exposed-on-localhost-tcp2375)
  - [pipeline](#pipeline)

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
GitLab Runner does not require a restart when you change most options, including parameters in the [[runners]] section and most parameters in the global section, except for listen_address, it reloads config automatically if necessary. <br/>
More on runner configuration on [advanced page](https://docs.gitlab.com/runner/configuration/advanced-configuration.html).

### DinD architecture

if you use
```shell
[[runners]]
:
  executor = "docker"
:
  [runners.docker]
:
    volumes = ["/var/run/docker.sock:/var/run/docker.sock"]  # this should not be used for DinD
```
your cannot use pipeline jobs with 
```shell
  services:
    - name: docker:dind
      alias: docker
```
as the containers are not Docker in Docker, but Docker host, per [this note](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/4260#note_194153107). <br/>
But the gitlab runner should have the "/var/run/docker.sock:/var/run/docker.sock" mount, for it to access Docker daemon on the host.

In turn, the DinD client container would probably connect to DinD daemon container via `tcp://docker:2375/`. Here `docker` s a "service", i.e. running in a separate container, by default named after the image name. The following would work in the same way:
```shell
  services:
   - name: docker:dind
     alias: thedockerhost
	 
  variables:
    # Tell docker CLI how to talk to Docker daemon; see
    # https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-executor
    DOCKER_HOST: tcp://thedockerhost:2375/	 
```

### runner container cmds when behind a proxy
```shell
# to create GitLab runner:
docker run -d --name gitlab-runner --restart always \
--env HTTP_PROXY="$http_proxy" \
--env HTTPS_PROXY="$http_proxy" \
--env GIT_SSL_NO_VERIFY=true \
-v /srv/gitlab-runner/config:/etc/gitlab-runner \
-v /var/run/docker.sock:/var/run/docker.sock \   # <== when Docker in Docker (docker executor) is to be used, for runner to access Docker daemon
 gitlab/gitlab-runner:latest
 

# to unregister a runner described in config (/srv/gitlab-runner/config/config.toml) like:
[[runners]]
  name = "CAPO infra"
  url = "https://gitlab.com/"
  limit = 4
  id = 21447349
  token = "22KV9kh-XXXXXX"
  
ubuntu@telcocloud-runner:~$ sudo docker run --rm -it --env HTTP_PROXY="$http_proxy" --env HTTPS_PROXY="$http_proxy" --env GIT_SSL_NO_VERIFY=true -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner unregister --url https://gitlab.com/ --token 22KV9kh-XXXXXX
Updating CA certificates...
rehash: warning: skipping ca-certificates.crt,it does not contain exactly one certificate or CRL
Runtime platform                                    arch=amd64 os=linux pid=7 revision=6d480948 version=15.7.1
Running in system-mode.

Unregistering runner from GitLab succeeded          runner=22KV9kh-
ubuntu@telcocloud-runner:~$
 

# to register a runner when behind proxy
docker run --rm -it  \
--env HTTP_PROXY="$http_proxy" \
--env HTTPS_PROXY="$http_proxy" \
--env GIT_SSL_NO_VERIFY=true \
-v /srv/gitlab-runner/config:/etc/gitlab-runner \
 gitlab/gitlab-runner:latest register
```

### runner config when behind a proxy
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
  environment = ["HTTPS_PROXY=http://1.2.3.4:3128", "HTTP_PROXY=http://1.2.3.4:3128", "NO_PROXY=172.17.0.0/16, docker"]    # will inject env vars to DinD containers, otherwise missing since ~/.docker/config.json is only for Docker Client to pass proxy information to containers, while DinD are created by GitLab .gitlab-ci.yml. the "docker is needed" because "kind create cluster" would sent a request to the URL http://docker:2375/v1.24/containers/ and this one matches the proxy, if not present in no_proxy
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

### have dockerd exposed on localhost tcp:2375
```shell
root@capi-bootstrap-capd-bb:~# cat /etc/docker/daemon.json
{"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]}
root@capi-bootstrap-capd-bb:~# dockerd &> dockerd-logfile &
root@capi-bootstrap-capd-bb:~# docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS         PORTS           NAMES
7d194ae59ef1   c2a760fa8767                  "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes                   runner-yzy-j8u-project-37797811-concurrent-0-82cc1a9c03842dd2-build-3
4a32676a9a2a   d736edfbfb0c                  "dockerd-entrypoint.…"   2 minutes ago   Up 2 minutes   2375-2376/tcp   runner-yzy-j8u-project-37797811-concurrent-0-82cc1a9c03842dd2-docker-0
ad5f3f5dac51   gitlab/gitlab-runner:latest   "/usr/bin/dumb-init …"   9 months ago    Up 2 hours                     gitlab-runner
root@capi-bootstrap-capd-bb:~#
root@capi-bootstrap-capd-bb:~# netstat -tupan | grep 2375
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp6       0      0 :::2375                 :::*                    LISTEN      -
root@capi-bootstrap-capd-bb:~# docker exec -it 4a32676a9a2a sh -c "netstat -tupan | grep 2375"
tcp        0      0 :::2375                 :::*                    LISTEN      29/dockerd
tcp        0      0 ::ffff:172.17.0.3:2375  ::ffff:172.17.0.4:36390 ESTABLISHED 29/dockerd
root@capi-bootstrap-capd-bb:~# 
```

## pipeline
```shell
.create-kind:
  stage: deploy
  before_script:
    # FIXME: build an image with following tools (+clusterctl)
    - apk add --no-cache curl bash git gettext # for envsubst
    - curl -Lo /usr/local/bin/kind https://kind.sigs.k8s.io/dl/v0.15.0/kind-linux-amd64
    - chmod +x /usr/local/bin/kind
    - curl -Lo /usr/local/bin/kubectl https://dl.k8s.io/release/v1.25.0/bin/linux/amd64/kubectl
    - chmod +x /usr/local/bin/kubectl
    - curl -Lo /usr/local/bin/kubetail https://raw.githubusercontent.com/johanhaleby/kubetail/master/kubetail
    - chmod +x /usr/local/bin/kubetail
    - curl -L https://get.helm.sh/helm-v3.10.1-linux-amd64.tar.gz | tar xz
    - mv linux-amd64/helm /usr/local/bin/
    - curl -Lo /usr/bin/yq https://github.com/mikefarah/yq/releases/download/v4.30.6/yq_linux_amd64
    - chmod +x /usr/bin/yq

    - DOCKER_IP=$(getent hosts docker | awk '{print $1}')
    - |
      # create a cluster with access to API endpoint through docker-in-docker address
      cat <<EOF | kind create cluster --name capd --config=-
      kind: Cluster
      apiVersion: kind.x-k8s.io/v1alpha4
      networking:
        apiServerAddress: "$DOCKER_IP"
        apiServerPort: 6443
      EOF
    - kubectl cluster-info --context kind-capd

    - KIND_PREFIX=$(docker network inspect kind -f '{{ (index .IPAM.Config 0).Subnet }}')
    - ip route add $KIND_PREFIX via $DOCKER_IP

    - export DOCKER_HOST=tcp://$DOCKER_IP:2375
    - find somedir/*-some/ -name values.yaml -exec yq -i '.path.to.yaml.value = strenv(ENV_VAR_EXPORTED_ABOVE)' {} \;


test-w-kind:
  timeout: 60min
  extends: .create-kind
  script:
    - ./run.sh somedir/*-some/    
```

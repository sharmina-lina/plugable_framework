# 1.Install Docker

```
sudo su
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
docker ps

```
# 2. Install MySQL Server

```
apt-get install mysql-server
``` 

# 3. Run MySQL Docker Container
```
docker run -d \
  --name=mysql-container \
  -e MYSQL_ROOT_PASSWORD=123 \
  -e MYSQL_DATABASE=sysbench \
  -p 3306:3306 \
  mysql:latest
```
## Check Database
```
docker exec -it mysql-container mysql -uroot -p123 -e "SHOW DATABASES;"
```

# 4. Alternative: PostgreSQL Setup
```
sudo apt update
sudo apt install postgresql-client -y
```
## Run PostgreSQL Docker Container
```
docker run --name pg-sysbench \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=sysbench \
  -p 5432:5432 \
  -d postgres
```
## Verify Database
```
sql -h localhost -p 5432 -U root -d sysbench
```
# 5. Setup Load Balancer System
## Create Webserver Folders
```
mkdir webfolder1 webfolder2 webfolder3
echo "Hello from webserver 1" > webfolder1/index.html
echo "Hello from webserver 2" > webfolder2/index.html
echo "Hello from webserver 3" > webfolder3/index.html
```

## Run Webservers with Caddy
```
docker run -d --name webserver1 -p 10001:2015 -v /home/ubuntu/webfolder1:/srv abiosoft/caddy
docker run -d --name webserver2 -p 10002:2015 -v /home/ubuntu/webfolder2:/srv abiosoft/caddy
docker run -d --name webserver3 -p 10003:2015 -v /home/ubuntu/webfolder3:/srv abiosoft/caddy
```
## HAProxy Configuration
### 1.Create haproxy directory
```
mkdir haproxy
cd haproxy
```
### 2. Create haproxy.cfg

```
frontend main
   bind *:80
   mode http
   default_backend webservers
backend webservers
   mode http
   balance roundrobin
   server web-1 10.196.39.24:10001 check
   server web-2 10.196.39.24:10002 check
   server web-3 10.196.39.24:10003 check
```
### 3. Run HAProxy Container
docker run -d -p 80:80 -v /home/ubuntu/haproxy:/usr/local/etc/haproxy:ro --name haproxy haproxy

# 6. Deploy Microservice-Based Application
Use a different VM due to port conflicts (8080).
## Install Minikube
Follow: https://medium.com/@areesmoon/installing-minikube-on-ubuntu-20-04-lts-focal-fossa-b10fad9d0511

```
sudo apt update
sudo apt install -y curl wget apt-transport-https
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version
```

## Install kubectl

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version -o yaml
```

## Start Minikube
```
sudo minikube start --driver=docker --force
sudo minikube status
kubectl cluster-info
```

# 7. Deploy Application (Online Boutique)
```
git clone --depth 1 --branch v0 https://github.com/GoogleCloudPlatform/microservices-demo.git
cd microservices-demo
kubectl apply -f ./release/kubernetes-manifests.yaml
kubectl get pods
```
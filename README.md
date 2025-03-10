# plugable_framework
# Plugable Framework Setup Guide

## 1. Login to the VM

## Ensure you have access to your VM and log in via SSH.

```ssh ubuntu@your-vm-ip```

## 2. Add Server Names to Known Hosts

## Edit the /etc/hosts file to add the following server names:

```sudo vi /etc/hosts```

Add these lines:
```
10.196.243.193 server
10.196.243.24 application_server
```
Save and exit the file.

## 3. Establish Connection with Cloud System Server

If you do not have an SSH key, generate one using the following command:

```ssh-keygen```

## 4. Clone the Git Repository

If your private key is in /home/ubuntu/.ssh/id_ed25519, clone v2:

```git clone --branch v2 --single-branch https://github.com/sharmina-lina/plugable_framework.git```

If your private key is in /home/ubuntu/.ssh/id_rsa, clone v1:
```
git clone --branch v1 --single-branch https://github.com/sharmina-lina/plugable_framework.git
````
## 5. Navigate to the Project Directory

```cd plugable_framework```

## 6. Remove Existing Virtual Environment

```sudo rm -rf venv```

## 7. Create a New Virtual Environment
```
sudo apt-get update
sudo apt install python3.12-venv  # Or use sudo apt install python3-venv
python3 -m venv venv
```
## 8. Activate the Virtual Environment
```
source venv/bin/activate
```
## 9. Install Dependencies
```
pip install -r requirements.txt
```
## 10. (Optional) Configure and Run Prometheus & Grafana

Configure Prometheus

Navigate to the Prometheus directory:
```
cd prometheus
```
Edit the prometheus.yml file to add the IP of the machine.

Install Docker
```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```
Run Prometheus and Grafana Containers
```
sudo docker run -d --name=prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

sudo docker run -d --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```
## 11. Run the Framework
```
python3 main.py
```
Your plugable framework is now set up and ready to use!



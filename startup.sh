#!/bin/bash


gcloud compute instances create final --project=cisc5550gcloud --zone=us-central1-a --machine-type=e2-medium --network-interface=network-tier=PREMIUM,subnet=default --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=133938927518-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server --create-disk=auto-delete=yes,boot=yes,device-name=final,image=projects/debian-cloud/global/images/debian-11-bullseye-v20220406,mode=rw,size=10,type=projects/cisc5550gcloud/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any
gcloud compute firewall-rules create rule-allow-tcp-5001 --source-ranges 0.0.0.0/0 --target-tags http-server --allow tcp:5001

gcloud compute ssh final --zone=us-central1-a --command='
sudo apt install python3-pip
sudo apt-get install wget
sudo pip3 install flask
sudo pip3 install requests
sudo pip3 install urllib3
sudo apt-get install unzip
wget -nc https://raw.githubusercontent.com/dougymenns/cisc5550/main/todolistgit.zip
sudo unzip todolistgit.zip 
cd todolistgit
sudo chmod 777 todolist.db
sudo chmod 777 users.db
python3 todolist_api.py
'
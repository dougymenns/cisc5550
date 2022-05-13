export TODO_API=`gcloud compute instances list --filter="name=final" --format="value(EXTERNAL_IP)"`

docker build -t cisc-final:v1 --build-arg api_ip=${TODO_API} . 

docker tag cisc-final:v1 gcr.io/cisc5550gcloud/cisc-final:v1 
docker push gcr.io/cisc5550gcloud/cisc-final:v1 

gcloud container clusters create final --zone=us-central1-a
kubectl create deployment final --image=gcr.io/cisc5550gcloud/cisc-final:v1 
kubectl expose deployment final --type=LoadBalancer --port=80 --target-port=80

sleep 45
kubectl get services
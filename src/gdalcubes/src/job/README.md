```shell
cd src/job 
```

Create an image of a consumer, producer and notification services.

1. Create the image

Build and load to Hub the images
```shell
/bin/bash consumer/build.sh
```
```shell
/bin/bash producer/build.sh
```
```shell
/bin/bash notification/build.sh
```

Activate environment
```shell
. /opt/gdalcubes/.venv/bin/activate
```

Test library in container
```python
import gdalcubepy
```

1. Push image to Docker Hub

Login Docker Hub
```shell
docker login
```
View the config.json file created
```shell
cat ~/.docker/config.json
```

Push the image
For the Docker Hub, tag your app image with your username and push to the Hub with the below commands.
Replace <username> with your Hub username.
docker tag job-wq-2 <username>/job-wq-2
docker push <username>/job-wq-2
```shell
docker tag job-gdalcubepy mafehiza/job-gdalcubepy
docker push mafehiza/job-gdalcubepy
```
docker tag pub-gdalcubepy mafehiza/pub-gdalcubepy
docker push mafehiza/pub-gdalcubepy
docker tag sub-gdalcubepy mafehiza/sub-gdalcubepy
docker push mafehiza/sub-gdalcubepy
https://hub.docker.com/


1. Create new tasks

Enter to the redis pod
```shell
kubectl exec --stdin --tty temp -- /bin/bash
```


1. Create a job to run the tasks

Create a job
```shell
kubectl apply -f ./kubernetes/deployment.yaml
```

Delete a job when it finishes
```shell
kubectl delete -f ./kubernetes/deployment.yaml
```


1. Monitor pods

List of pods
```shell
kubectl get pods
```

Logs of a pod
```shell
kubectl logs job-gdalcubepy-whvn9
```

```shell
python3.10 -m venv mainenv
source mainenv/bin/activate
```

Enter to the pod
```shell
kubectl exec --stdin --tty job-gdalcubepy-tln7g -- sh
```

```shell
ls /app
```

kubectl cp <some-namespace>/<some-pod>:/tmp/foo /tmp/bar
```shell
kubectl cp job-gdalcubepy-xs5qz:/app/single_chunk_3.nc Python/results/single_chunk_3.nc
```



KAFKA

helm install my-release oci://registry-1.docker.io/bitnamicharts/kafka
helm delete my-release

kubectl run my-release-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.5.1-debian-11-r35 --namespace default --command -- sleep infinity

kubectl port-forward my-release-kafka-client 9092:9092

kubectl run my-release-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.5.1-debian-11-r35 --namespace default --command -- sleep infinity
kubectl -n kafkam run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 -rm-true
kubectl -n kafkam run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.36.1-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
kubectl -n kafkam run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning


kubectl delete namespace [your-namespace]
kubectl create namespace [your-namespace]

current context
kubectl config get-contexts
kubectl config current-context

kubectl config set-context --current --namespace=kafka
kubectl config set-context $(kubectl config current-context) --namespace=kafka

kubectl get ns

kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.36.1-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-2-kafka-bootstrap:9092 --topic my-topic



. .venv/bin/activate
pip install confluent-kafka

python


SECURITY_PROTOCOL = "SASL_SSL"
SASL_MECHANISM = "PLAIN"

conf = {
'bootstrap.servers' : 'my-release-kafka.default.svc.cluster.local:9092',
'sasl.mechanisms': 'SCRAM-SHA-256',
'security.protocol': 'SASL_PLAINTEXT',
'sasl.username': 'user1',
'sasl.password': 'UE3ynWg2aj',
'enable.ssl.certificate.verification': 'false'
}

conf2 = {
'bootstrap.servers': 'my-release-kafka.default.svc.cluster.local:9092',
'sasl.mechanisms': 'PLAIN',
'security.protocol': 'SASL_SSL',
'sasl.username': 'user1',
'sasl.password': 'UE3ynWg2aj',
'enable.ssl.certificate.verification': 'false'
}
conf2 = {
'bootstrap.servers': 'my-release-kafka.default.svc.cluster.local:9092',
}
conf2 = {
'bootstrap.servers': 'localhost:9092',
'enable.ssl.certificate.verification': 'false'
}

conf2 = {
'bootstrap.servers': 'my-cluster-2-kafka.kafka.svc.cluster.local:9092',
}

from confluent_kafka import Producer
p = Producer(conf2)




### Create context

1. Create namespace
kubectl create namespace [your-namespace]
```shell
kubectl create namespace gdalcubepy-kafka
```

1. Change context
Get current context
```shell
kubectl config get-contexts
```
```shell
kubectl config current-context
```
Set context
```shell
kubectl config set-context --current --namespace=gdalcubepy-kafka
```
or 
```shell
kubectl config set-context $(kubectl config current-context) --namespace=gdalcubepy-kafka
```

### Install kafka
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Install custom kafka service (This will create the controller pods)
```shell
helm install gdalcubepy-kafka bitnami/kafka \
--set persistence.enabled=false,zookeeper.persistence.enabled=false
```

Uninstall custom kafka service (This will delete the controller pods)
```shell
helm uninstall gdalcubepy-kafka
```

List of services (This list the kafka service)
```shell
helm list
```

Delete kafka client pod
```shell
kubectl delete pod gdalcubepy-kafka-client --namespace gdalcubepy-kafka
```

Create kafka client pod
```shell
kubectl run gdalcubepy-kafka-client \
    --restart='Never' \
    --image docker.io/bitnami/kafka:3.5.1-debian-11-r35 \
    --namespace gdalcubepy-kafka \
    --command \
    -- sleep infinity
```


### Config security kafka

1. Create `'client.properties'` file.
2. Copy file to kafka container.
   kubectl cp --namespace gdalcubepy-kafka /path/to/client.properties gdalcubepy-kafka-client:/tmp/client.properties
```shell
kubectl cp --namespace gdalcubepy-kafka client.properties gdalcubepy-kafka-client:/tmp/client.properties
```

1. Test producer
Enter to the container
```shell
kubectl exec --tty -i gdalcubepy-kafka-client --namespace gdalcubepy-kafka -- bash
```
```shell
opt/bitnami/kafka/bin/kafka-topics.sh
```
```shell
opt/bitnami/kafka/bin/kafka-console-producer.sh \
    --producer.config /tmp/client.properties \
    --broker-list kafka-local-controller-0.kafka-local-controller-headless.gdalcubepy-kafka.svc.cluster.local:9092,kafka-local-controller-1.kafka-local-controller-headless.gdalcubepy-kafka.svc.cluster.local:9092,kafka-local-controller-2.kafka-local-controller-headless.gdalcubepy-kafka.svc.cluster.local:9092 \
    --topic test
```

1. Test consumer
   Enter to the container
```shell
kubectl exec --tty -i gdalcubepy-kafka-client --namespace gdalcubepy-kafka -- bash
```
```shell
opt/bitnami/kafka/bin/kafka-console-consumer.sh \
    --consumer.config /tmp/client.properties \
    --bootstrap-server kafka-local.gdalcubepy-kafka.svc.cluster.local:9092 \
    --topic test \
    --from-beginning
```

### Get kafka version
```shell
kubectl exec --tty -i gdalcubepy-kafka-client --namespace gdalcubepy-kafka -- bash
```
```shell
opt/bitnami/kafka/bin/kafka-topics.sh --version
```
```shell
opt/bitnami/kafka/bin/kafka-broker-api-versions.sh \
   --consumer.config /tmp/client.properties \
   --bootstrap-server kafka-local.gdalcubepy-kafka.svc.cluster.local:9092
```



kubectl run gcpy-consumer --rm --tty -i \
--image mafehiza/gdalcubepy-consumer \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python3 -u ./consumer.py

kubectl run gcpy-notification --rm --tty -i \
--image mafehiza/gdalcubepy-notification \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python3 -u ./notification.py

kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python3 -u ./producer.py


kubectl run gcpy-consumer --rm --tty -i \
--image mafehiza/gdalcubepy-consumer \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python3 -u ./consumer.py

kubectl run gcpy-notification --rm --tty -i \
--image mafehiza/gdalcubepy-notification \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python3 -u ./notification.py

kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never \
--command \
-- python3 -u ./producer.py


## Updated deployments & send messages

```shell
kubectl apply -f src/job/kubernetes/deployment.yaml --namespace gdalcubepy-kafka
```

Start message
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never \
--namespace gdalcubepy-kafka \
--command \
-- python -u ./producer.py --source="/opt/gdalcubes/Python/L8_Amazon_mini"
```
python -u ./producer.py --source="/opt/gdalcubes/Python/L8_Amazon_mini"
python -u ./producer.py --source="/opt/gdalcubes/Python/file_list.txt"
python -u ./producer.py --source="file_list.txt"

## Autoscaling

```shell
kubectl autoscale deployment/gdalcubepy-deployment --min=1 --max=5 --cpu-percent=5
```

```shell
kubectl get hpa
```

```shell
kubectl scale deployment/gdalcubepy-deployment --replicas=1
```

```shell
kubectl delete hpa gdalcubepy-deployment
```

```shell
kubectl get deployments --watch
```



### Monitor & Results

Enter to consumer pod
```shell
kubectl exec --stdin --tty gdalcubepy-consumer-768b55c656-pp88c --namespace gdalcubepy-kafka -- bash
```

Follow consumer pod logs
```shell
kubectl logs gdalcubepy-consumer-768b55c656-pp88c --namespace gdalcubepy-kafka -f
```

Timestamp consumer pod logs
```shell
kubectl logs gdalcubepy-consumer-768b55c656-pp88c --namespace gdalcubepy-kafka --timestamps
```

Copy results from consumer pod to local
```shell
kubectl cp --namespace gdalcubepy-kafka gdalcubepy-consumer-768b55c656-pp88c:/tmp/ Python/results
```

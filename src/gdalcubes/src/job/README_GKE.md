
# Create namespace
```shell
kubectl create namespace datacubepy
```
```shell
kubens datacubepy
```

# Config zookeeper

1. Create zookeeper StatefulSet.
File `src/job/kubernetes/statefulset-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/statefulset-zookeeper.yaml -n datacubepy
```

1. Create zookeeper service (This open the port to use it from kafka brokers).
File `src/job/kubernetes/headless-service-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/headless-service-zookeeper.yaml -n datacubepy
```

# Config kafka

1. Get the serviceName from zookeeper StatefulSet
2. Create multi brokers kafka.
File `src/job/kubernetes/statefulset-multi-broker-kafka.yaml`
3. Update the `ZOOKEEPER_CONNECT` env variable with the value `<zookeeper serviceName>.<namespace>.svc:2181`

value: "<zookeeper serviceName>.<namespace>.svc:2181"
value: "zookeeper.datacubepy.svc:2181"

1. Update the `KAFKA_ADVERTISED_LISTENERS` env variable with the value `<kafka serviceName>.<namespace>.svc:9092`

INTERNAL://$(POD_NAME).<kafka serviceName>.<namespace>.svc:9092
INTERNAL://$(POD_NAME).kafka.datacubepy.svc:9092

1. Apply changes
```shell
kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
```

1. Create kafka service (This open the port to use it from python producers and consumers).
File `src/job/kubernetes/headless-service-kafka.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/headless-service-kafka.yaml -n datacubepy
```

1. (Optional) To access externally by using NodePort. Then `localhost:30003` can be used.
```shell
kubectl apply -f src/job/kubernetes/bootstrap-service-kafka.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-0-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-1-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-2-service.yaml -n datacubepy
```

# Check kafka consumer and producers locally

1. Install kafka application locally


1. Check topics
```shell
kafka-topics --list --bootstrap-server localhost:30003
```

1. Produce 
```shell
kafka-console-producer --topic my-topic --bootstrap-server localhost:30003
```

1. Consume
```shell
kafka-console-consumer --topic my-topic --bootstrap-server localhost:30003 --from-beginning
```

# Check kafka consumer and producers in a pod

`<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092` can be used as `bootstrap-server`
`kafka:9092` or `kafka-0.kafka.datacubepy:9092`

1. Enter to a pod
```shell
kubectl exec -it kafka-0 -- bash
```

1. Check topics
```shell
./bin/kafka-topics.sh --list --bootstrap-server kafka:9092
```

1. Produce
```shell
./bin/kafka-console-producer.sh --topic my-topic --bootstrap-server kafka-0.kafka.datacubepy.svc:9092
```

1. Consume
```shell
./bin/kafka-console-consumer.sh --topic my-topic --bootstrap-server kafka-2.kafka.datacubepy.svc:9092 --from-beginning
```


# Config producer for the initial task from python

1. Check `bootstrap_servers` parameter for Kafka producer in the producer python file.
File `src/job/kubernetes/producer/producer.py`.
If it is able external (using NodePort or LoadBalancer) it would be `localhost:30003`. 
If it is locally it could be `<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092`

bootstrap_servers="kafka:9092"
bootstrap_servers="kafka-0.kafka.datacubepy.svc:9092"

1. Build and push the image to Docker Hub. 
(To update the image in Docker Hub takes time, so change the tag name to test)
docker login
docker build --tag <tag> . -f Dockerfile
docker push <tag>
```shell
/bin/bash kubernetes/producer/build.sh
```

1. (Optional) To debug locally, run the container with `docker run -it --rm <tag>`
Note: if the `bootstrap_servers` is not well configure, 
the error `kafka.errors.NoBrokersAvailable: NoBrokersAvailable` will appear.
```shell
docker run -it --rm mafehiza/gdalcubepy-producer
```

1. Create the pod to send the initial task
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never
```
(Alternative) To change the last command
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never \
--command \
-- python -u ./producer.py --source="/opt/gdalcubes/Python/L8_Amazon_mini"
```
(Alternative) To create a pod from a manifest, but logs are not enable
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: send-chunks
spec:
  containers:
    - name: send-chunks
      image: mafehiza/gdalcubepy-producer
```
```shell
kubectl apply -f src/job/kubernetes/send-chunks-pod.yaml
```
(Alterntive) To create a deployment from a manifest.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: initial-task
  labels:
    app: send-chunks
spec:
  replicas: 1
  selector:
    matchLabels:
      app: send-chunks
  template:
    metadata:
      labels:
        app: send-chunks
    spec:
      containers:
        - name: send-chunks
          image: mafehiza/gdalcubepy-producer
```
```shell
kubectl apply -f src/job/kubernetes/send-chunks-deployment.yaml
```

1. See logs/prints
```shell
kubectl logs send-chunks
```

1. Enter into the pod
```shell
kubectl exec --tty -i send-chunks -- bash 
kubectl exec -it send-chunks -- bash
```

# Config Consumer

1. Check `bootstrap_servers` parameter for Kafka producer in the producer python file.
   File `src/job/kubernetes/producer/producer.py`.
   If it is able external (using NodePort or LoadBalancer) it would be `localhost:30003`.
   If it is locally it could be `<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092`

bootstrap_servers="kafka:9092"
bootstrap_servers="kafka-0.kafka.datacubepy.svc:9092"

1. Build and push the image to Docker Hub.
   (To update the image in Docker Hub takes time, so change the tag name to test)
   docker login
   docker build --tag <tag> . -f Dockerfile
   docker push <tag>
```shell
/bin/bash kubernetes/consumer/build.sh
```

1. (Optional) To debug locally, run the container with `docker run -it --rm <tag>`
   Note: if the `bootstrap_servers` is not well configure,
   the error `kafka.errors.NoBrokersAvailable: NoBrokersAvailable` will appear.
```shell
docker run -it --rm mafehiza/gdalcubepy-consumer
```

1. Create the pod
```shell
kubectl run gcpy-consumer --rm --tty -i \
--image mafehiza/gdalcubepy-consumer \
--restart Never \
--namespace datacubepy
```
(Alternative)
```shell
kubectl run gcpy-consumer --rm --tty -i \
--image mafehiza/gdalcubepy-consumer \
--restart Never \
--namespace datacubepy \
--command \
-- python -u ./consumer.py
```

# Config Notification

1. Check `bootstrap_servers` parameter for Kafka producer in the producer python file.
   File `src/job/kubernetes/producer/producer.py`.
   If it is able external (using NodePort or LoadBalancer) it would be `localhost:30003`.
   If it is locally it could be `<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092`

bootstrap_servers="kafka:9092"
bootstrap_servers="kafka-0.kafka.datacubepy.svc:9092"

1. Build and push the image to Docker Hub.
   (To update the image in Docker Hub takes time, so change the tag name to test)
   docker login
   docker build --tag <tag> . -f Dockerfile
   docker push <tag>
```shell
/bin/bash kubernetes/notification/build.sh
```

1. (Optional) To debug locally, run the container with `docker run -it --rm <tag>`
   Note: if the `bootstrap_servers` is not well configure,
   the error `kafka.errors.NoBrokersAvailable: NoBrokersAvailable` will appear.
```shell
docker run -it --rm mafehiza/gdalcubepy-notification
```

1. Create the pod
```shell
kubectl run gcpy-notification --rm --tty -i \
--image mafehiza/gdalcubepy-notification \
--restart Never \
--namespace datacubepy
```
(Alternative)
```shell
kubectl run gcpy-notification --rm --tty -i \
--image mafehiza/gdalcubepy-notification \
--restart Never \
--namespace datacubepy \
--command \
-- python -u ./notification.py
```



# Debug pods

kubectl logs <pod name>
kubectl describe pod <pod name>
kubectl get events


# Clean namespace

kubectl delete all -n datacubepy --all
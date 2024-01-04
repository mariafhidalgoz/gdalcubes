
# Create namespace
```shell
kubectl create namespace datacubepy
```

# Config zookeeper

1. Create zookeeper StatefulSet.
File `src/job/kubernetes/statefulset-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/statefulset-zookeeper.yaml
```

1. Create zookeeper service (This open the port to use it from kafka brokers).
File `src/job/kubernetes/headless-service-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/headless-service-zookeeper.yaml
```

# Config kafka

1. Get the serviceName from zookeeper StatefulSet
2. Create multi brokers kafka.
File `src/job/kubernetes/statefulset-multi-broker-kafka.yaml`
3. Update the `ZOOKEEPER_CONNECT` env variable with the value `<serviceName>.<namespace>.svc:2181`

value: "<serviceName>.<namespace>.svc:2181"
value: "zookeeper.kafka.svc:2181"

1. Update the `KAFKA_ADVERTISED_LISTENERS` env variable with the value `<serviceName>.<namespace>.svc:9092`

INTERNAL://$(POD_NAME).<serviceName>.<namespace>.svc:9092
INTERNAL://$(POD_NAME).kafka.kafka.svc:9092

1. Apply changes
```shell
kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml
```

# Config producer the initial task

1. Check `bootstrap_servers` parameter for Kafka producer in the producer python file.
File `src/job/kubernetes/producer/producer.py`.
If it is able external (using NodePort or LoadBalancer) it would be `localhost:30003`. 
If it is locally it could be `<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092`

bootstrap_servers="kafka:9092"
bootstrap_servers="kafka-0.kafka.kafka.svc:9092"

1. Build and push the image to Docker Hub. 
(To update the image in Docker Hub takes time, so change the tag name to test)
docker login
docker build --tag <tag> . -f Dockerfile
docker push <tag>
```shell
/bin/bash producer/build.sh
```

1. (Optional) To debug locally, run the container with `docker run -it --rm <tag>`
```shell
docker run -it --rm mafehiza/gdalcubepy-producer-2
```

1. Create the pod to send the initial task
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer-2 \
--restart Never
```
(Alternative) To change the last command
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer-2 \
--restart Never \
--command \
-- python3 -u ./producer.py
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
      image: mafehiza/gdalcubepy-producer-2
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
          image: mafehiza/gdalcubepy-producer-2
```
```shell
kubectl apply -f src/job/kubernetes/send-chunks-deployment.yaml
```

See logs/prints
```shell
kubectl logs send-chunks
```

Enter into the pod
```shell
kubectl exec --tty -i send-chunks -- bash 
kubectl exec -it send-chunks -- bash
```


# Debug pods

kubectl logs <pod name>
kubectl describe pod <pod name>
kubectl get events
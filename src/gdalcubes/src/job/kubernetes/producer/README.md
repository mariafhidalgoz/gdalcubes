
# Config producer for the initial task from python

1. Get the right url to connect kafka with python notification service.
(The service name can be use directly like `kafka:9092`)
Run another curl application to test this:
```shell
kubectl run curl --image=radial/busyboxplus:curl -i --tty --rm
```
Hit enter and run
```shell
nslookup kafka
```

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
To change the last command
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never \
--command \
-- python -u ./producer.py --source="/opt/gdalcubes/Python/L8_Amazon_mini"
```
(Alternative) 
```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never
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

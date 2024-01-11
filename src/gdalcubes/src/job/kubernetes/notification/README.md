
# Config Notification

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

1. Check `bootstrap_servers` parameter for Kafka notification in the notification python file.
   File `src/job/kubernetes/notification/notification.py`.
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

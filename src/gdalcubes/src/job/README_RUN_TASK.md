
1. Run producer pod

```shell
kubectl run send-chunks --rm --tty -i \
--image mafehiza/gdalcubepy-producer \
--restart Never
```

1. Run consumer pod

```shell
kubectl run gcpy-consumer --rm --tty -i \
--image mafehiza/gdalcubepy-consumer \
--restart Never \
--namespace datacubepy
```

# Config Notification

1. Create the pod
```shell
kubectl run gcpy-notification --rm --tty -i \
--image mafehiza/gdalcubepy-notification \
--restart Never \
--namespace datacubepy
```



1. Enter to consumer pod
```shell
kubectl exec -it gcpy-consumer -- bash
```
Into the pod
```shell
cd ls tmp/
```


```shell
kubectl apply -f ./src/gdalcubes/src/job/kubernetes/pvc/pv-volume.yaml -n datacubepy
```

```shell
kubectl apply -f ./src/gdalcubes/src/job/kubernetes/pvc/pv-claim.yaml -n datacubepy
```


```shell
kubectl apply -f ./src/gdalcubes/src/job/kubernetes/pvc/pv.yaml -n datacubepy
```

```shell
kubectl delete -f ./src/gdalcubes/src/job/kubernetes/pvc/pv.yaml -n datacubepy
```


```shell
kubectl delete -f ./src/gdalcubes/src/job/kubernetes/pvc/pv-volume.yaml -n datacubepy
kubectl delete -f ./src/gdalcubes/src/job/kubernetes/pvc/pv-claim.yaml -n datacubepy
```


```shell
kubectl apply -f ./src/gdalcubes/src/job/kubernetes/pvc/pv-pod.yaml -n datacubepy
```
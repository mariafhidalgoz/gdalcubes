```shell
cd src/gdalcubes/src/job/kubernetes/redis/
```

1. Run redis pod and service
```shell
kubectl apply -f ./service/redis-pod.yaml -n datacubepy
kubectl apply -f ./service/redis-service.yaml -n datacubepy
```

1. Build the image to process chunks and update it in Docker Hub
```shell
/bin/bash ./worker/build.sh
/bin/bash ./app/build.sh
```
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


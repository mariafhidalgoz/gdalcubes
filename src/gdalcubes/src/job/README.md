```shell
cd src/job 
```

1. Create the image

Build the image
```shell
docker build -t job-gdalcubepy .
```
Run container
```shell
docker run -t job-gdalcubepy
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
https://hub.docker.com/


1. Create new tasks

Enter to the redis pod
```shell
kubectl exec --stdin --tty temp -- /bin/bash
```

Enter to the redis service
```shell
redis-cli -h redis
```

Lunch tasks
```shell
rpush job2 "3"
rpush job2 "1"
```

List of current tasks
```shell
lrange job2 0 -1
```


1. Create a job to run the tasks

Create a job
```shell
kubectl apply -f ./kubernetes/job.yaml
```

Delete a job when it finishes
```shell
kubectl delete -f ./kubernetes/job.yaml
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
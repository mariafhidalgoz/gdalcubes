https://devopscube.com/setup-grafana-kubernetes/

Create the configmap using the following command.

```shell
kubectl create -f src/job/grafana/grafana-datasource-config.yaml -n datacubepy
```

Create the deployment

```shell
kubectl create -f src/job/grafana/deployment.yaml -n datacubepy
```
Create the service.

```shell
kubectl create -f src/job/grafana/service.yaml -n datacubepy
```


# Config Prometheus in Grafana

Change `localhost` by `http://host.docker.internal:9090`
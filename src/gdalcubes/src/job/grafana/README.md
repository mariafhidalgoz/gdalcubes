https://devopscube.com/setup-grafana-kubernetes/

Get datasource url


Create the configmap using the following command using the previous datasource url.

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

# Check prometheus service with kafka metrics

Run port forward
```shell
kubectl --namespace datacubepy port-forward grafana-657b7b7c76-qkrtt 3000
```

Go to `localhost:9090` and check the kafka-metrics are there


# Config Prometheus in Grafana

Change `localhost` by `http://host.docker.internal:9090`
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
kubectl --namespace datacubepy port-forward grafana-698df9ff6-rp8s2 3000
```

Go to `localhost:3000`


# Config Prometheus in Grafana
Dashboard used
https://grafana.com/grafana/dashboards/721-kafka/

Config datasource in grafana
Change `localhost` by `http://host.docker.internal:9090`
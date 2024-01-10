

# Config prometheus service
https://artifacthub.io/packages/helm/prometheus-community/prometheus?modal=install

Add repository
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

Install chart
```shell
helm install dcp-prometheus prometheus-community/prometheus --version 25.8.2 --namespace datacubepy
```

User the pod server for port-forward
```shell
kubectl get pods --namespace datacubepy -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=dcp-prometheus" -o jsonpath="{.items[0].metadata.name}"
```
```shell
export POD_NAME=$(kubectl get pods --namespace datacubepy -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=dcp-prometheus" -o jsonpath="{.items[0].metadata.name}")
```


## Add kafka service to prometheus

Download current config file from the prometheus server pod
```shell
kubectl get configmaps dcp-prometheus-server -o yaml > src/job/prometheus/dcp-prometheus-server_base.yaml
```

Get the right target name to connect kafka with zookeeper service.
- Run another curl application to test this:
```shell
kubectl run curl --image=radial/busyboxplus:curl -i --tty --rm
```
- Hit enter and run
nslookup <service name>
```shell
nslookup kafka-jmx-metrics-service
```

Make a file copy and add a new scrape_configs in the config file
File: `src/job/prometheus/dcp-prometheus-server_base.yaml`
```yaml
    scrape_configs:
    - job_name: 'kafka-metrics'
      scrape_interval: 5s
      static_configs:
#      - targets: ['host.docker.internal:32000'] # local machine
      - targets: ['kafka:8088'] # local kubernetes same pod
      - targets: ['kafka-prometheus.datacubepy.svc.cluster.local:32000'] # GKE
```

Apply the configuration with the command
```shell
kubectl apply -f src/job/prometheus/dcp-prometheus-server_base.yaml
```
NOTE:
With ERROR: `Operation cannot be fulfilled on configmaps "dcp-prometheus-server": the object has been modified; please apply your changes to the latest version and try again`
Solution: Remove `resourceVersion`, `selfLink` and `uid`.


# Check prometheus service with kafka metrics

Run port forward
```shell
kubectl --namespace datacubepy port-forward $POD_NAME 9090
```

Go to `localhost:9090` and check the kafka-metrics are there

Create service so Grafana can connect to Prometheus
```shell
kubectl kubectl apply -f src/job/prometheus/headless-service-prometheus.yaml -n datacubepy
```

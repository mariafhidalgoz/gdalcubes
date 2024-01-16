
# Create namespace
```shell
kubectl create namespace datacubepy
```
```shell
kubens datacubepy
```

# Config zookeeper

1. Create zookeeper StatefulSet.
File `src/job/kubernetes/statefulset-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/statefulset-zookeeper.yaml -n datacubepy
```

1. Create zookeeper service (This open the port to use it from kafka brokers).
File `src/job/kubernetes/headless-service-zookeeper.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/headless-service-zookeeper.yaml -n datacubepy
```
1. Get the right url to connect kafka with zookeeper service.
Run another curl application to test this:
```shell
kubectl run curl --image=radial/busyboxplus:curl -i --tty --rm
```
Hit enter and run
```shell
nslookup zookeeper
```


# Config kafka

1. Get the serviceName from zookeeper StatefulSet
2. Create multi brokers kafka.
File `src/job/kubernetes/statefulset-multi-broker-kafka.yaml`
3. Update the `ZOOKEEPER_CONNECT` env variable with the value gotten in zookeeper configuration.

value: "<zookeeper pod name>.<zookeeper service name>.<namespace>.svc.cluster.local:2181"
value: "zookeeper-0.zookeeper.datacubepy.svc.cluster.loca:2181"

1. Update the `KAFKA_ADVERTISED_LISTENERS` env variable with the value `<kafka serviceName>.<namespace>.svc:9092`

INTERNAL://$(POD_NAME).<kafka serviceName>.<namespace>.svc:9092
INTERNAL://$(POD_NAME).kafka.datacubepy.svc:9092

1. Apply changes
NOTE: Remember create `jmx-config` and `jmx-javaagent` configmaps first, if they are not yet.
```shell
kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
```

1. Create kafka service (This open the port to use it from python producers and consumers).
File `src/job/kubernetes/headless-service-kafka.yaml`
2. Apply changes
```shell
kubectl apply -f src/job/kubernetes/headless-service-kafka.yaml -n datacubepy
```

1. (Optional) To access externally by using NodePort. Then `localhost:30003` can be used.
```shell
kubectl apply -f src/job/kubernetes/bootstrap-service-kafka.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-0-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-1-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-2-service.yaml -n datacubepy
```


# Check kafka consumer and producers locally

1. Install kafka application locally


1. Check topics
```shell
kafka-topics --list --bootstrap-server localhost:30003
```

```shell
kafka-topics.sh --create --partitions 1 --replication-factor 1 --topic my-topic-2 --bootstrap-server localhost:30003
```
1. Produce 
```shell
kafka-console-producer --topic my-topic --bootstrap-server localhost:30003
```

1. Consume
```shell
kafka-console-consumer --topic my-topic --bootstrap-server localhost:30003 --from-beginning
```

# Check kafka consumer and producers in a pod

`<serviceName>:9092` or `<kafka-pod>.<serviceName>.<namespace>.svc:9092` can be used as `bootstrap-server`
`kafka:9092` or `kafka-0.kafka.datacubepy:9092`

1. Enter to a pod
```shell
kubectl exec -it kafka-0 -- bash
```

1. Check topics
```shell
./bin/kafka-topics.sh --list --bootstrap-server kafka:9092
```
./bin/kafka-topics.sh --describe --bootstrap-server kafka:9092 --topic my-topic
./bin/kafka-topics.sh --describe --zookeeper zookeeper:2181 --topic my-topic

1. Produce
```shell
./bin/kafka-console-producer.sh --topic my-topic --bootstrap-server kafka-0.kafka.datacubepy.svc:9092
```

1. Consume
```shell
./bin/kafka-console-consumer.sh --topic my-topic --bootstrap-server kafka-2.kafka.datacubepy.svc:9092 --from-beginning
```


# Adding JMX metrics for Kafka metrics

Download `jmx_prometheus_javaagent-0.19.0.jar` file from `https://github.com/prometheus/jmx_exporter`

Create kafka metrics file by using `https://github.com/prometheus/jmx_exporter/blob/main/example_configs/kafka-0-8-2.yml`

Create configmap with the above files
```shell
kubectl create configmap jmx-config --from-file=src/job/kubernetes/jmx_exporter/jmx-prometheus-config.yaml -n datacubepy
kubectl create configmap jmx-javaagent --from-file=src/job/kubernetes/jmx_exporter/jmx_prometheus_javaagent-0.19.0.jar -n datacubepy
```

Update brokers
File: `src/job/kubernetes/statefulset-multi-broker-kafka.yaml`
- Add the env variable `KAFKA_OPTS`
```yaml
- name: KAFKA_OPTS
  value: "-javaagent:/jmx_javaagent/jmx_prometheus_javaagent-0.19.0.jar=8088:/jmx_config_metrics/jmx-prometheus-config.yaml"

```

- Add volumes for `jmx_config_metrics` and `jmx_javaagent`

Create service to open the pods connection
```shell
kubectl apply -f src/job/kubernetes/headless-service-kafka-jmx-metrics.yaml -n datacubepy
```

Restart kafka brokers
kubectl rollout restart statefulset <statefulset-name>
```shell
kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
kubectl rollout restart statefulset kafka
```

Check files `jmx-prometheus-config.yaml` and `jmx_prometheus_javaagent-0.19.0.jar` and in the kafka borker
```shell
kubectl exec -it kafka-0 -n datacubepy -- bash
ls /jmx_config_metrics/jmx-prometheus-config.yaml
ls /jmx_javaagent/jmx_prometheus_javaagent-0.19.0.jar
```


# Check metrics by using
This would be to run inside a pod
```shell
kubectl exec -it kafka-0 -n datacubepy -- bash
curl localhost:8088
```


# Debug pods

kubectl logs <pod name>
kubectl describe pod <pod name>
kubectl get events


# Clean namespace

kubectl delete all -n datacubepy --all
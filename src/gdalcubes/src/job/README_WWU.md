1. Login to WWU Kubernetes https://zivgitlab.uni-muenster.de/wwu-it/wwukube/login-script#building-from-source
```shell
wwukube login
```

1. set WWU context
```shell
kubectx wwukube-staging-ms1
```

1. Install zookeeper statefulset and service
```shell
kubectl apply -f src/job/kubernetes/statefulset-zookeeper.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/headless-service-zookeeper.yaml -n datacubepy
```
```shell
kubectl delete -f src/job/kubernetes/statefulset-zookeeper.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/headless-service-zookeeper.yaml -n datacubepy
```

1. Install kafka brokers and services
```shell
kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/headless-service-kafka.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/bootstrap-service-kafka.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-0-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-1-service.yaml -n datacubepy
kubectl apply -f src/job/kubernetes/kafka-2-service.yaml -n datacubepy
```
```shell
kubectl delete -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/headless-service-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/bootstrap-service-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-0-service.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-1-service.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-2-service.yaml -n datacubepy
```

kubectl delete namespace kafka
kubectl create namespace kafka
kubens kafka

kubectl apply -f src/job/kubernetes/statefulset-zookeeper.yaml
kubectl apply -f src/job/kubernetes/headless-service-zookeeper.yaml

kubectl apply -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml
kubectl apply -f src/job/kubernetes/headless-service-kafka.yaml
kubectl apply -f src/job/kubernetes/bootstrap-service-kafka.yaml
kubectl apply -f src/job/kubernetes/kafka-0-service.yaml
kubectl apply -f src/job/kubernetes/kafka-1-service.yaml
kubectl apply -f src/job/kubernetes/kafka-2-service.yaml

kubectl get ep
zookeeper-shell 10.1.0.140:2181

ZOOKEEPER_CONNECT
value: "<service name>.<namespace>.svc:2181"
value: "zookeeper.kafka.svc:2181"

KAFKA_ADVERTISED_LISTENERS
INTERNAL://$(POD_NAME).<service name>.<namespace>.svc:9092
INTERNAL://$(POD_NAME).kafka.kafka.svc:9092

kafka-topics --create --topic my-topic --replication-factor 3 --partitions 1 --bootstrap-server 10.1.0.144:9092
kafka-topics --create --topic my-topic --replication-factor 3 --partitions 1 --bootstrap-server localhost:31003
kafka-console-producer --topic my-topic --bootstrap-server localhost:30003
kafka-console-consumer --topic my-topic --bootstrap-server localhost:30003 --from-beginning

./bin/kafka-console-producer.sh --topic my-topic --bootstrap-server kafka-0.kafka.kafka.svc:9092
./bin/kafka-console-consumer.sh --topic my-topic --bootstrap-server kafka-0.kafka.kafka.svc:9092 --from-beginning
./bin/kafka-topics.sh --list --bootstrap-server kafka-0.kafka.kafka.svc:9092
./bin/kafka-topics.sh --list --bootstrap-server kafka:9092
kafka.kafka.svc.cluster.local:9092

kafka-topics --list --bootstrap-server localhost:30003

kubectl run send-chunks --rm --tty -i \
--image mafehiza/test15 \
--restart Never \
--command \
-- python3 -u ./producer.py

kubectl get all
gdalcubepy-kafka.datacubepy.svc.cluster.local
kafka.default.svc.cluster.local

kafka-topics --list --zookeeper localhost:2181
kafka-topics --list --bootstrap-server 10.1.0.73:9092

kafka-console-producer --topic my-topic --bootstrap-server localhost:9092
kafka-console-producer --topic my-topic --bootstrap-server kafka-bitnami.test-kafka.svc.cluster.local:9092

kubectl get endpoints -l app=kafka

kubectl port-forward kafka 9092:9092
kubectl port-forward service/gdalcubepy-kafka 9092:9092


kubectl delete -f src/job/kubernetes/statefulset-zookeeper.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/headless-service-zookeeper.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/statefulset-multi-broker-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/headless-service-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/bootstrap-service-kafka.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-0-service.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-1-service.yaml -n datacubepy
kubectl delete -f src/job/kubernetes/kafka-2-service.yaml -n datacubepy



Result:
```
    PRODUCER:
        kafka-console-producer.sh \
            --producer.config /tmp/client.properties \
            --broker-list gdalcubepy-kafka-controller-0.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-1.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-2.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server gdalcubepy-kafka.datacubepy.svc.cluster.local:9092 \
            --topic test \
            --from-beginning
```

1. List services
```shell
kubectl get service -n datacubepy
```

1. List pods
```shell
kubectl get pods -n datacubepy
```

1. Delete kafka client pod
```shell
kubectl delete pod gdalcubepy-kafka-client -n datacubepy
```

1. Get the kafka password (Instructions from result of install kafka service)
```shell
$(kubectl get secret gdalcubepy-kafka-user-passwords --namespace datacubepy -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)
```

1. Create the `client.properties` file and copy it to kafka client service (Instructions from result of install kafka service)
```shell
kubectl cp --namespace datacubepy src/job/kafka/wwu/client.properties gdalcubepy-kafka-client:/tmp/client.properties
```

1. Enter to the container
```shell
kubectl exec --tty -i gdalcubepy-kafka-client --namespace datacubepy -- bash
```
```shell
opt/bitnami/kafka/bin/kafka-topics.sh --version
```
```shell
opt/bitnami/kafka/bin/kafka-console-producer.sh \
--producer.config /tmp/client.properties \
--broker-list gdalcubepy-kafka-controller-0.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-1.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-2.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092 \
--topic test
```

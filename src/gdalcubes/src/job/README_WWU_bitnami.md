1. Login to WWU Kubernetes https://zivgitlab.uni-muenster.de/wwu-it/wwukube/login-script#building-from-source
```shell
wwukube login
```

1. set WWU context
```shell
kubectx wwukube-staging-ms1
```

1. Install kafka service
```shell
helm install gdalcubepy-kafka bitnami/kafka -n datacubepy \
--set persistence.enabled=false,zookeeper.persistence.enabled=false
```

Result:
```
NAME: gdalcubepy-kafka
LAST DEPLOYED: Tue Dec  5 15:08:36 2023
NAMESPACE: datacubepy
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 26.4.2
APP VERSION: 3.6.0

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    gdalcubepy-kafka.datacubepy.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    gdalcubepy-kafka-controller-0.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092
    gdalcubepy-kafka-controller-1.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092
    gdalcubepy-kafka-controller-2.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092

The CLIENT listener for Kafka client connections from within your cluster have been configured with the following security settings:
    - SASL authentication

To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="user1" \
    password="$(kubectl get secret gdalcubepy-kafka-user-passwords --namespace datacubepy -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run gdalcubepy-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.6.0-debian-11-r2 --namespace datacubepy --command -- sleep infinity
    kubectl cp --namespace datacubepy /path/to/client.properties gdalcubepy-kafka-client:/tmp/client.properties
    kubectl exec --tty -i gdalcubepy-kafka-client --namespace datacubepy -- bash

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
helm list -n datacubepy
```

1. Uninstall custom kafka service (This will delete the controller pods)
```shell
helm uninstall gdalcubepy-kafka -n datacubepy
```

1. Run kafka client service (check command from result of install kafka service)
```shell
kubectl apply -f src/job/kubernetes/resource-quota-mem-cpu.yaml -n datacubepy
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

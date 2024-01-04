1. Install, see config cluster, and version Kubernetes
```shell
brew install kubectl
brew install kubectx
cat ~/.kube/config
kubectl version
kubectl version --client --output=yaml
```

1. Start minikube
```shell
minikube start
```
```shell
minikube status
minikube version
```
```shell
minikube addons enable metrics-server
minikube dashboard
```
```shell
minikube stop
minikube delete
```

1. Set context
```shell
kubectx minikube
```

1. Set namespace
```shell
kubens datacubepy
```
```shell
kubectl delete namespace datacubepy
kubectl create namespace datacubepy
```

1. Get pods
```shell
kubectl get pods
```
Get pods from all namespace
```shell
minikube kubectl -- get pods -A
```

1. Install kafka service
```shell
helm install gdalcubepy-kafka bitnami/kafka -n datacubepy \
--set persistence.enabled=false,zookeeper.persistence.enabled=false
```

```shell
helm install gdalcubepy-kafka bitnami/kafka -n datacubepy \
--set persistence.enabled=false,zookeeper.persistence.enabled=false,controller.resources.limits.memory="128Mi",controller.resources.limits.cpu="500m",controller.resources.requests.memory="128Mi",controller.resources.requests.cpu="250m",controller.initContainerResources.limits.memory="128Mi",controller.initContainerResources.limits.cpu="500m"
```


Result:
```
NAME: gdalcubepy-kafka
LAST DEPLOYED: Wed Nov 29 18:09:18 2023
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
kubectl run gdalcubepy-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.6.0-debian-11-r2 --namespace datacubepy --command -- sleep infinity
```

1. Delete kafka client pod
```shell
kubectl delete pod gdalcubepy-kafka-client
```


1. Config `client.properties` file (Follow instructions from result of install kafka service: create and copy file)
```shell
kubectl cp --namespace datacubepy /path/to/client.properties gdalcubepy-kafka-client:/tmp/client.properties
```

1. kafka topics
Enter to the container
```shell
kubectl exec --tty -i gdalcubepy-kafka-client -- bash
```
```shell
opt/bitnami/kafka/bin/kafka-topics.sh
```
kafka-console-producer.sh \
--producer.config /tmp/client.properties \
--broker-list gdalcubepy-kafka-controller-0.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-1.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092,gdalcubepy-kafka-controller-2.gdalcubepy-kafka-controller-headless.datacubepy.svc.cluster.local:9092 \
--topic test


kafka-console-consumer.sh \
--consumer.config /tmp/client.properties \
--bootstrap-server gdalcubepy-kafka.datacubepy.svc.cluster.local:9092 \
--topic test \
--from-beginning
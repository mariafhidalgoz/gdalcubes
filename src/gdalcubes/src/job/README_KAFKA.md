Kafka

zookeeper host
local installation -> host.docker.internal.2181
kubernetes yaml file (statefulset + headless service) -> zookeeper.default.svc:2181

bootstrap
local installation -> localhost:9092


create topic container locally
kubectl exec -it kafka-0 -- bin/kafka-topics.sh --create --topic mytopic --partitions 1 --replication-factor 3 --bootstrap-server localhost:9092

describe topic
kubectl exec -it kafka-0 -- bin/kafka-topics.sh --describe --topic mytopic --bootstrap-server localhost:9092

producer
kubectl exec -it kafka-0 -- bin/kafka-console-producer.sh --topic mytopic --bootstrap-server localhost:9092

consumer
kubectl exec -it kafka-0 -- bin/kafka-console-consumer.sh --topic mytopic --bootstrap-server localhost:9092 --from-beginning


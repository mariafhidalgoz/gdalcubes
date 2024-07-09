[//]: # (https://pipekit.io/blog/argo-workflows-the-best-way-to-run-kubernetes-workflows)

1. install the Argo Workflows custom resources and controller
```shell
export ARGO_WORKFLOWS_VERSION=3.5.4
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v$ARGO_WORKFLOWS_VERSION/install.yaml
```

1. setting client authentication
```shell
kubectl patch deployment \
  argo-server \
  --namespace argo \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": [
  "server",
  "--auth-mode=server"
]}]'
```

1. you'll forward the deployment port to a port on your local server
```shell
kubectl -n argo port-forward deployment/argo-server 2746:2746
```

1. run workflow
```shell
argo submit -n argo --watch src/gdalcubes/src/job/kubernetes/argo/data-pipeline.yaml
```


[//]: # (https://argoproj.github.io/argo-events/quick_start/)

argo events

```shell
kubectl create namespace argo-events-2
```

1. config controller manager
```shell
kubectl apply -f src/gdalcubes/src/job/kubernetes/argo/argo-events/install.yaml
```

1. config events webhook
```shell
kubectl apply -f src/gdalcubes/src/job/kubernetes/argo/argo-events/install-validating-webhook.yaml
```

1. config eventbus (3 pods)
```shell
kubectl apply -n argo-events-2 -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/eventbus/native.yaml
```

**** custom process for webhook (check the process for other messages broker like redis)

1. create `event-source` for webhook
```shell
#kubectl apply -n argo-events-2 -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/event-sources/webhook.yaml
```

1. create a service account with RBAC settings to allow the sensor to trigger workflows
```shell
 # sensor rbac
kubectl apply -n argo-events-2 -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/sensor-rbac.yaml
 # workflow rbac
kubectl apply -n argo-events-2 -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/workflow-rbac.yaml
```

1. create `sensor` for webhook. (Once the sensor object is created, sensor controller will create corresponding pod and a service.)
```shell
kubectl apply -n argo-events-2 -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/sensors/webhook.yaml
```

1. Expose the event-source pod via Ingress, OpenShift Route or port forward to consume requests over HTTP.
```shell
kubectl -n argo-events-2 port-forward $(kubectl -n argo-events-2 get pod -l eventsource-name=webhook -o name) 12000:12000
```

1. Use either Curl or Postman to send a post request to the http://localhost:12000/example.
```shell
curl -d '{"message":"this is my first webhook"}' -H "Content-Type: application/json" -X POST http://localhost:12000/example
```

1. Verify that an Argo workflow was triggered.
```shell
kubectl -n argo-events-2 get workflows | grep "webhook"
```


[//]: # (https://argoproj.github.io/argo-events/eventsources/setup/redis/)

```shell
kubectl create namespace argo-events
```

1. Run redis pod and service
```shell
kubectl apply -f src/gdalcubes/src/job/kubernetes/redis/service/redis-pod.yaml -n argo-events
kubectl apply -f src/gdalcubes/src/job/kubernetes/redis/service/redis-service.yaml -n argo-events
```

1. Run redis
```shell
kubectl exec -it redis -n argo-events -- redis-cli
```

1. config controller manager
```shell
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
```

1. config events webhook
```shell
## Install with a validating admission controller
#kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install-validating-webhook.yaml
```

1. config `eventbus` (3 pods)
```shell
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/eventbus/native.yaml
```

1. Create the `event source` by running the following command.
```shell
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/event-sources/redis.yaml
```

1. create a service account with RBAC settings to allow the sensor to trigger workflows
```shell
 # sensor rbac
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/sensor-rbac.yaml
 # workflow rbac
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/workflow-rbac.yaml
```

1. Create the `sensor` by running the following command. (This has the workflow will be trigger)
```shell
#kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/sensors/redis.yaml
kubectl apply -n argo-events -f src/gdalcubes/src/job/kubernetes/argo/workflow-triggered-with-redis.yaml
```

1. Log into redis pod using kubectl.
```shell
kubectl -n argo-events exec -it <redis-pod-name> -c <redis-container-name> -- /bin/bash
kubectl exec -it redis -n argo-events -- redis-cli
```

1. Run redis-cli and publish a message on FOO channel.
```shell
PUBLISH FOO hello
```

1. Once a message is published, an argo workflow will be triggered. Run `argo list` to find the workflow
```shell
argo list
```



kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/event-sources/redis.yaml

kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/sensors/redis.yaml

kubectl -n argo-events exec -it <redis-pod-name> -c <redis-container-name> -- /bin/bash
kubectl exec -it redis-master -n argo -- redis-cli

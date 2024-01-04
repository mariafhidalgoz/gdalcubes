# Set up a secret to access to Docker Hub images from Kubernetes cluster

1. Create a Secret based on existing credentials
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials
```shell
kubectl create secret generic regcred \
--from-file=.dockerconfigjson=/Users/maria/.docker/config.json \ 
--type=kubernetes.io/dockerconfigjson
```

1. Inspecting the Secret regcred
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#inspecting-the-secret-regcred
```shell
kubectl get secret regcred --output=yaml
```
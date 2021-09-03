# sorry-gke

Currently on GKE, `event-exporter` and `stackdriver-metadata-agent` pods are preventing scaling down as they're using `hostPath` and not using `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"` annotation. Deployments of these pods are overwritten on every cluster upgrade so it's not a viable solution to set them manually. This controller patches Deployments to inject missing annotations to allow autoscaler a scaledown waiting a proper patch from GKE.

## Build

```sh
docker build -t guyguy333/sorry-gke .
```

## Install

```sh
kubectl apply -f deployment.yaml
```

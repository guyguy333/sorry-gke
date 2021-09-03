import asyncio
import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException

@kopf.on.update('apps/v1', 'deployments', labels={'k8s-app': 'event-exporter'})
@kopf.on.update('apps/v1', 'deployments', labels={'app': 'stackdriver-metadata-agent'})
async def inject_annotation(spec, name, **kwargs):
    lock = asyncio.Lock()
    async with lock:
        print(f"A deployment has been updated: {name}")
        try:
            api = kubernetes.client.AppsV1Api()
            current = api.read_namespaced_deployment(name=name, namespace="kube-system")
            if not "cluster-autoscaler.kubernetes.io/safe-to-evict" in current.spec.template.metadata.annotations:
                print("Annotation is missing. Patching...")
                current.spec.template.metadata.annotations['cluster-autoscaler.kubernetes.io/safe-to-evict'] = "true"
                res = api.patch_namespaced_deployment(name=name, namespace="kube-system", body=current)
                print("Deployment updated. status='%s'" % str(res))
                print(f"Annotation has been injected for deployment {name}")
        except ApiException as e:
            print("Exception when injecting annotation: %s\n" % e)

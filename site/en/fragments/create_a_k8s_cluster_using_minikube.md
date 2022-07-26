### Create a K8s cluster using minikube

We recommend installing Milvus on K8s with [minikube](https://minikube.sigs.k8s.io/docs/), a tool that allows you to run K8s locally.

<div class="alert note">
minikube can only be used in test environments. It is not recommended that you deploy Milvus distributed clusters in this way in production environments.
</div>

#### 1. Install minikube

See [install minikube](https://minikube.sigs.k8s.io/docs/start/) for more information.

#### 2. Start a K8s cluster using minikube

After installing minikube, run the following command to start a K8s cluster.

```
$ minikube start
```

#### 3. Check the K8s cluster status

Run `$ kubectl cluster-info` to check the status of the K8s cluster you just created. Ensure that you can access the K8s cluster via `kubectl`. If you have not installed `kubectl` locally, see [Use kubectl inside minikube](https://minikube.sigs.k8s.io/docs/handbook/kubectl/).

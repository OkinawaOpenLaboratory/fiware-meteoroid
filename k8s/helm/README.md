# Meteoroid

Meteoroid realizes integrating Function as a Service(FaaS) capabilities in FIWARE. It provides a management interface specialized for FaaS and FIWARE.

## Introduction

This chart bootstrap FIWARE and Meteoroid deployment on a [Kubernetes](http://kuberetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes 1.18+
- Helm 3.1.2+
- Dynamic Volume Provisioning Support

## Installing the Chart

You should specify Kubernetes node IP to `<Your API Host Name>` in `values.yaml`:

```bash
openwhisk:
  whisk:
    ingress:
      type: NodePort
      apiHostName: <Your API Host Name>
      apiHostPort: 31001
```

To install the chart with the release name `my-release`:

```bash
$ helm install my-release .
```

The command deploys FIWARE on the Kubernetes cluster in the default configration.
The [configration](#configration) section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configration

The following table lists the configrable parameters of the FIWARE chart and their default values.

Parameter                                  | Description                                     | Default
------------------------------------------ | ----------------------------------------------- | --------------
`orion.image.repository`                   | Image source repository name of FIWARE Orion    | `fiware/orion`
`orion.image.version`                      | FIWARE Orion release tag                        | `2.4.0`
`orion.image.pullPolicy`                   | Image pull policy                               | `IfNotPresent`
`orion.nodePort`                           | Node port number of FIWARE Orion                | `31026`
`orion.replicaCount`                       | Number of FIWARE Orion replicas                 | `1`
`mongodb.image.tag`                        | MongoDB release tag                             | `3.6-debian-9`
`mongodb.image.debug`                      | Enable debug of MongoDB                         | `true`
`mongo.usePassword`                        | Enable password authentication                  | `false`
`mongo.mongodbSystemLogVerbosity`          | Enable MongoDB system log verbosity             | `5`
`quantumleap.db.image.name`                | Image source repository name of Crate DB        | `crate`
`quantumleap.db.image.tag`                 | Crate DB release tag                            | `3.1.2`
`quantumleap.db.nodePort.admin`            | Node port number of Crate DB Admin              | `30200`
`quantumleap.db.nodePort.transport`        | Node port number of Crate DB Transport          | `30300`
`quantumleap.ql.image.name`                | Image source repository name of Quantum Leap    | `smartsdk/quantumleap`
`quantumleap.ql.image.tag`                 | Quantum Leap release tag                        | `0.7.4`
`quantumleap.ql.nodePort`                  | Node port number of Quantum Leap                | `30668`
`quantumleap.ql.db`                        | Host name of Crate DB                           | `crate`
`quantumleap.ql.replicaCount`              | Number of Quantum Leap replicas                 | `1`
`quantumleap.ui.image.name`                | Image source repository name of Quantum Leap UI | `grafana/grafana`
`quantumleap.ui.image.tag`                 | Quantum Leap UI release tag                     | `6.1.6`
`quantumleap.ui.nodePort`                  | Node port number of Quantum Leap UI             | `30333`
`meteoroid.image.name`                     | Image source repository name of Meteoroid       | `oolorg/meteoroid-core`
`meteoroid.image.tag`                      | Meteoroid release tag                           | `1.0.1`
`meteoroid.nodePort`                       | Node port number of Meteoroid                   | `30002`
`meteoroid.env.OPEN_WHISK_APIGATEWAY_PORT` | OpenWhisk API Gateway port                      | `80`
`openwhisk.whisk.ingress.type`             | Service type of OpenWhisk                       | `NodePort`
`openwhisk.whisk.ingress.apiHostName`      | OpenWhisk API host name                         | -
`openwhisk.whisk.ingress.apiHostPort`      | OpenWhisk API host port                         | `31001`
`openwhisk.invoker.containerFactory.impl`  | Invoker container factory (Docker or Kubernetes) | `kubernetes`
`openwhisk.invoker.containerFactory.kubernetes.isolateUserActions` | User action container network isolation | `false`
`openwhisk.nginx.httpsNodePort`            | Node port number of OpenWhisk Nginx HTTPS port  | `31001`
`openwhisk.providers.cloudant.enabled`     | Enable Cloudant provider                        | `false`
`openwhisk.providers.kafka.enabled`        | Enable Kafka provider                           | `true`
`openwhisk.metrics.prometheusEnabled`      | Enable system metrics using prometheus          | `true`
`openwhisk.metrics.userMetricsEnabled`     | Enable user metrics using prometheus            | `true`
`openwhisk.kafka.persistence.size`         | Kafka persistence size                          | `2Gi`
`cp-helm-charts.cp-kafka-rest.enabled`     | Enable Kafka REST Proxy                         | `false`
`pixy.image.name`                          | Image source repository name of Kafka Pixy      | `mailgun/kafka-pixy`
`pixy.image.tag`                           | Kafka Pixy release tag                          | `0.17.0`

For more information about OpenWhisk configuration please see [configurationChoices](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/configurationChoices.md).


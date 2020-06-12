.. _Introduction:

************
Introduction
************

Delivery toolchain is a the standalone entry point which offers a configuration of all parts of the application lifetime
such as CI/CD, orchestrator and monitoring and their interaction that is crucial to provide the successful delivery of the application.

- **Continuous Delivery** is an essential part of RADON. This means rapid, incremental changes to Serverless Applications. Doing so demands a specific focus on automation.

- The **orchestrator** is represented by xOpera orchestration tool which aims to be a lightweight orchestrator compliant with OASIS TOSCA
  The current compliance is with the TOSCA Simple Profile in YAML v1.3. Opera is by following TOSCA primarily a
  (TOSCA) cloud orchestrator which enables orchestration of automated tasks within cloud applications for different
  cloud providers such as Amazon Web Services(AWS), Microsoft Azure, Google Cloud Platform(GCP), OpenFaaS, OpenStack
  and so on. Apart from that this tool can be used and integrated to other infrastructures in order to orchestrate
  services or applications and therefore reduce human factor.

- The **RADON Monitoring tool** collects evidence from the runtime environment for supporting quality assurance on performance and security characteristic. It, thus, provides monitoring capabilities on different levels of abstraction:
  virtual machine, container, application and FaaS. The RADON Monitoring tool is based on `Prometheus <https://prometheus.io>`_, an open-source
  system monitoring and alerting toolkit. For the needs of RADON users, public available instances of a `Prometheus server <https://github.com/prometheus/prometheus>`_,
  a `Grafana visualization dashboard <https://grafana.com/grafana/>`_ and a Service Discovery service based on `Consul <https://www.consul.io/>`_ are offered.

  - RADON Prometheus server: http://3.127.254.144:9090/
  - RADON Grafana: `<http://3.127.254.144:3000/>`_
  - RADON Service Discovery: `<http://3.127.254.144:8500/>`_

.. _Installation:

************
Installation
************

This section explains the installation of monitoring tool.

Monitoring an AWS Lambda function
#################################

  - Prometheus Pushgateway

The Prometheus Pushgateway exists to allow ephemeral and batch jobs to expose their metrics to Prometheus.
Since these kinds of jobs may not exist long enough to be scraped, they can instead push their metrics
to a Pushgateway. The Pushgateway then exposes these metrics to Prometheus.

A service template in TOSCA for the push gateway, part of the RADON monitoring tool, is available at:
`<https://github.com/radon-h2020/radon-monitoring-tool/blob/master/service.yml>`_. You can try to deploy it with xOpera like::

  $ OPERA_SSH_USER=xxx opera deploy service.yml

It installs a push gateway instance and automatically advertises its endpoint
on the RADON service discovery agent. Then the RADON Prometheus server will auto discover the newly
registered/advertised push gateway endpoint and start scraping it to collect exposed metrics.
The exposed metrics are then available on the visualisation dashboard.


  - RADON Monitoring client

To monitor an AWS Lambda function import the RADON monitoring lib
(`<https://github.com/radon-h2020/radon-monitoring-tool/blob/master/lambda/python-runtime/monitoring_lib.py>`_) and simply annotate the
lambda_function:::lambda_handler, i.e::

  from monitoring_lib import monitor_cpu, monitor_ram

  @monitor_cpu
  @monitor_ram
  def lambda_handler(event, context):

The dependencies can be provided to AWS Lambda via layer like::

  $ pip install --target ./package/python prometheus_pushgateway
  $ pip install --target ./package/python psutil
  $ zip -r9 function.zip package/
  $ aws lambda publish-layer-version --layer-name monitoring_client --zip-file fileb://function.zip --compatible-runtimes ruby2.5

or packaged with the lambda code or simply reference a public available layer::

  arn:aws:lambda:eu-central-1:510790361559:layer:radon_monitoring_client:2

The RADON monitoring client needs to be registered to its corresponding push gateway component. This is achieved
by injecting an Environment variable to the AWS Lambda function with key: PUSH_GATEWAY_HOST.


Monitoring & extracting metrics from application logs
#####################################################

Extracting Prometheus metrics from application logs is supported in RADON using Google's `mtail <https://github.com/google/mtail>`_ tool.
mtail acts as a Prometheus exporter so it is fully compliant with the RADON Monitoring tool which is based on Prometheus toolkit.
A TOSCA service template for deploying the mtail component and transparently integrate it to the RADON central Prometheus server is available
at `<https://github.com/radon-h2020/radon-monitoring-tool/blob/master/service.yml>`_. It can be deployed with the RADON xOpera orchestrator on any server running a Docker runtime, as usual::

  $ OPERA_SSH_USER=xxx opera deploy service.yml

In terms of configuration needed, a user should specify the path of the log file to be monitored/analysed in the command of the corresponding docker compose file (--logs)::

  command:
    "-logtostderr --progs /progs/gauge.mtail --logs /logs/foo.log --poll_interval 250ms"

mtail continuously tails and parses the log file and on each log record it applies a RegEx rule to extract the monitoring metrics of interest. A sample mtail config file is available at:  `<https://github.com/radon-h2020/radon-monitoring-tool/blob/master/gauge.mtail>`_.
::

  gauge val_acc

  /validation accuracy (\d+)/ {
    # Parse log record and export validation accuracy value.
    val_acc = $1
  }

It filters log records containing the pattern: 'validation accuracy (\d+)' and exposes the value to the Prometheus and consequently to the Grafana for visualization of the monitored metrics.
Please refer to mtail's `Programming Guide <https://github.com/google/mtail/blob/master/docs/Programming-Guide.md>`_ for details.
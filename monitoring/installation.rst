.. _Installation:

************
Installation
************

This section explains the installation of monitoring tool.

Prometheus Pushgateway
######################

The Prometheus Pushgateway exists to allow ephemeral and batch jobs to expose their metrics to Prometheus.
Since these kinds of jobs may not exist long enough to be scraped, they can instead push their metrics
to a Pushgateway. The Pushgateway then exposes these metrics to Prometheus.

A service template in TOSCA for the push gateway, part of the RADON monitoring tool, is available at:
`<https://github.com/radon-h2020/radon-monitoring-tool/blob/master/service.yml>`_. You can try to deploy it with xOpera like::

  $ OPERA_SSH_USER=xxx opera deploy service.yml

It installs a push gateway instance and automatically advertises its endpoint
on the service discovery agent. Then the Prometheus server will auto discover the newly
registered/advertised push gateway endpoint and start scraping it to collect exposed metrics.
The exposed metrics are then available on the visualisation dashboard.


Monitoring client
#################

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

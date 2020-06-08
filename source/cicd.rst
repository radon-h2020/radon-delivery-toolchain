Continuous Delivery is an essential part of Radon. This means rapid, incremental changes to Serverless Applications. Doing so demands a specific focus on automation. 

 - For Continuous Integration, we want to be able to automate the necessary tollgates for quality validation and branch integration.
 - For Continuous Deployment, we want to automate the necessary release criterias and create a fail-safe environment.

Combined we achieve our ambition of reduced lead time and value to the end user.

Technically, this is achieved by utilizing the full framework of Radon. Within the framework you find all the necessary components for quality assurance, deployment, testing and monitoring. Including these tools in a CI/CD pipeline will assure automation and increase velocity.

::

    pipeline {
        agent any
        environment {
            AWS_ACCESS_KEY_ID     = credentials('aws-id')
            AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        }
        stages {
            stage('Defect prediction') {
                steps {
                    // https://radon-h2020.github.io/radon-defect-prediction-api/
                    sh docker run -p 5000:5000 radon-dp:latest
                    curl -X POST "http://localhost:5000/api/classification/classify" -H  "accept: */*" -H  "Content-Type: plain/text" -d "- host: all"
                }
            }

            stage('Deploy resources') {
                environment {
                    DEPLOY_FILE = '_definitions/radonlegacyblueprints__ImageResize.tosca'
                }
                steps {
                    sh 'unzip -o ImageResize.csar'
                    sh 'opera deploy $DEPLOY_FILE'
                }
            }
            stages {
            stage('Testing') {
                steps {
                    // https://continuous-testing-tool.readthedocs.io/en/latest/
                    sh docker run -t -i --name RadonCTT -p 18080:18080 -v /var/run/docker.sock:/var/run/docker.sock radonconsortium/radon-ctt:latest
                    curl -X POST "http://localhost:18080/RadonCTT/project" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"name\":\"SockShop\",\"repository_url\":\"https://github.com/radon-h2020/demo-ctt-sockshop.git\"}"
                    curl -X POST "http://localhost:18080/RadonCTT/deployment" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"testartifact_uuid\":\"87a2d052-93ce-43d2-b765-74b0cef9df92\"}"
                    curl -X POST "http://localhost:18080/RadonCTT/execution" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"deployment_uuid\":\"5f435990-8a1a-4741-a040-6db2fe552603\"}"

                }
            }
        }
    }
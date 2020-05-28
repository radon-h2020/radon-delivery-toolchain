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
            stage('Deploy resources') {
                environment {
                    DEPLOY_FILE = '_definitions/radonlegacyblueprints__ImageResize.tosca'
                }
                steps {
                    sh 'unzip -o ImageResize.csar'
                    sh 'opera deploy $DEPLOY_FILE'
                }
            }
        }
    }
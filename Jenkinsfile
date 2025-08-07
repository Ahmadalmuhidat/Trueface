pipeline {
  agent any

  parameters {
    choice(
      name: 'TARGET_DIR',
      choices: ['TrueFace-Admin', 'TrueFace-Cam', 'Trueface-Backend'],
      description: 'Select the folder to build from.'
    )
  }

  environment {
    DOCKER_IMAGE = "trueface-django"
    DOCKER_CONTAINER = "trueface-django"

    // Jenkins credentials (must be added via Manage Jenkins > Credentials)
    DB_HOST = credentials('mysql-db-host') // type: Secret Text
    DB_NAME=Trueface
    DB_USER = credentials('mysql-db-user') // type: Secret Text or Username
    DB_PASSWORD = credentials('mysql-db-password') // type: Secret Text
    JWT_TOKEN_SECRET = credentials('jwt-secret') // type: Secret Text
    SECRET = credentials('secret-env-key')  // type: Secret Text
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        echo "Checked out repository."
      }
    }

    stage('Build Docker Image') {
      steps {
        dir("${params.TARGET_DIR}") {
          script {
            echo "Building Docker image from ${params.TARGET_DIR}..."
            sh "docker build -t ${DOCKER_IMAGE}:latest ."
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          echo "Stopping and removing old container..."
          sh """
            docker stop ${DOCKER_CONTAINER} || true
            docker rm ${DOCKER_CONTAINER} || true
          """

          echo "Running new Docker container..."
          sh """
            docker run -d --name ${DOCKER_CONTAINER} -p 8000:8000 \
            -e DB_HOST=${DB_HOST} \
            -e DB_NAME=${DB_NAME} \
            -e DB_USER=${DB_USER} \
            -e DB_PASSWORD=${DB_PASSWORD} \
            -e JWT_TOKEN_SECRET=${JWT_TOKEN_SECRET} \
            -e SECRET=${SECRET} \
            ${DOCKER_IMAGE}:latest
          """
        }
      }
    }
  }

  post {
    success {
      echo 'Deployment completed successfully!'
    }
    failure {
      echo 'Deployment failed. Check logs for details.'
    }
  }
}

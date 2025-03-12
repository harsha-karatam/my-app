pipeline {
    agent any

    environment {
        CONTAINER_NAME = "flask-app"
        APP_PATH_IN_CONTAINER = "/app" // Adjust this if the app is in a different directory inside the container
        HOST_APP_PATH = "./app"       // Path to updated files on the host
        APP_PORT = "5003"             // Application port
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Update Application in Running Container') {
            steps {
                script {
                    echo "Copying updated application files into the container: ${CONTAINER_NAME}..."
                    sh '''
                        # Copy updated application files into the container
                        docker cp ${HOST_APP_PATH}/ ${CONTAINER_NAME}:${APP_PATH_IN_CONTAINER}/
                    '''
                    
                    echo "Stopping and restarting the container: ${CONTAINER_NAME}..."
                    sh '''
                        # Stop the container if it's running
                        docker stop ${CONTAINER_NAME} || true
                        
                        # Restart the container
                        docker start ${CONTAINER_NAME}
                    '''
                    
                    echo "Restarting application inside the container: ${CONTAINER_NAME}..."
                    sh '''
                        # Restart the application process if necessary
                        docker exec ${CONTAINER_NAME} pkill -f "python" || true
                        docker exec ${CONTAINER_NAME} python ${APP_PATH_IN_CONTAINER}/main.py &
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Application updated and container restarted successfully!'
        }
        failure {
            echo 'Update failed. Check the logs for details.'
        }
    }
}

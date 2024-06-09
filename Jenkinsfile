pipeline {
    agent any

    stages {

        stage('Setup') {
            steps {
                script {
                    sh "docker stop app_container || true"
                    sh "docker rm app_container || true"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
               
                    script {
                        
                        sh 'docker build -t app ./flask_image_fusion/'
                        
                    }
                
                
            }
        }

        stage('Run Docker Image') {
            steps {
                sh 'docker run -d -p 4000:80 --name app_container app'

            }
        }

        stage('Wait for Docker Container') {
            steps {
                
                script {
                    sleep 10
                }
            }
        }
    }

    post {
        always {
            
            cleanWs()
        }
    }
}
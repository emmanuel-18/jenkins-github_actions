pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Run') {
            steps {
                echo 'Webhook test working!'
            }
        }
    }
}
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat 'python --version'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Train + Compare Models') {
            steps {
                bat 'python train.py'
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'best_model.pkl, experiment_log.json', fingerprint: true
            }
        }
        
        stage ('Deploy Model API') {
            steps {
                bat 'pip install fastapi uvicorn'
                bat 'start /B uvicorn app:app --host 0.0.0.0 --port 8000'
            }
        }
    }
}
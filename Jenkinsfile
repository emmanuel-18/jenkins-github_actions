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

        stage('Deploy Model API') {
            steps {
                bat 'pip install fastapi uvicorn'

                bat 'start /B uvicorn app:app --host 0.0.0.0 --port 8000'

                bat 'ping 127.0.0.1 -n 6 > nul'
            }
        }

        stage('Test API') {
            steps {
                bat '''
                curl -X POST http://localhost:8000/predict ^
                -H "Content-Type: application/json" ^
                -d "{\\"features\\": [5.1, 3.5, 1.4, 0.2]}" > response.json

                type response.json
                '''
            }
        }

        stage('Validate API Output') {
            steps {
                bat '''
                python -c "import json; f=open('response.json'); data=json.load(f); f.close(); \
assert 'prediction' in data, 'API FAILED: missing prediction'; \
print('API TEST PASSED:', data)"
                '''
            }
        }
    }
}
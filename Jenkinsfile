pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('dependencies') {
            steps {
                sh """. ../venv/bin/activate 
                pip install --break-system-packages -r requirements.txt"""
            }
        }

        stage('Playwright Install') {
            steps {
                sh """. ../venv/bin/activate
                playwright install
                playwright install-deps"""
            }
        }

        
        stage('Test') {
            steps {
                sh """. ../venv/bin/activate
                pytest --junitxml=results.xml"""
            }
            post {
                always {
                    junit 'results.xml'
                    archiveArtifacts artifacts: 'results.xml', fingerprint: true
                }
            }
        }
    }
}
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
                pytest --junitxml=results-${BUILD_NUMBER}.xml"""
            }
            post {
                always {
                    junit "results-${BUILD_NUMBER}.xml"
                    archiveArtifacts artifacts: "results-${BUILD_NUMBER}.xml", fingerprint: true
                }
            }
        }
    }
}
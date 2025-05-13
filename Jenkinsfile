pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('env') {
            steps {
                sh '. ../venv/bin/activate'
            }
        }
        
        stage('dependencies') {
            steps {
                sh 'pip install --break-system-packages -r requirements.txt'
            }
        }

        stage('Playwright Install') {
            steps {
                sh 'playwright install'
            }
        }

        
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
    }
}
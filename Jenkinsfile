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
                '. ./venv/bin/activate'
            }
        }
        
        stage('Instalación dependencias') {
            steps {
                sh 'pip install --break-system-packages -r requirements.txt'
            }
        }
        
        stage('Pruebas') {
            steps {
                sh 'pytest'
            }
        }
    }
}
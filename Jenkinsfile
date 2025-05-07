pipeline {
    agent any

    stages {
        stages('Checkout' {
            steps {
                checkout scm
            }
        })
    }

    stage('Verificar Python') {
        steps {
            sh 'python3 --version || python --version'
        }
    }

    stage('Instalación dependencias') {
        steps {
            sh 'pip install -r requirements.txt'
        }
    }

    stage('Instalación Playwright') {
        steps {
            sh 'python install playwright'
        }
    }

    stage('Pruebas') {
        steps {
            sh 'pytest'
        }
    }
}
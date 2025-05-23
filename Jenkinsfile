pipeline {
    agent any

    parameters {
    string(name: 'COMMIT_SHA', defaultValue: '', description: 'SHA from the commit to use')
    }

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

                    publishGitHubChecks checkName: 'Automated-tests',
                                        commitSha: params.COMMIT_SHA,
                                        status: 'COMPLETED',
                                        conclusion: currentBuild.result == 'SUCCESS' ? 'SUCCESS' : 'FAILURE',
                                        testResultsFiles: 'results.xml'
                }
            }
        }
    }
}
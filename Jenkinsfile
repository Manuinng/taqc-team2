pipeline {
    agent any

    parameters {
    string(name: 'COMMIT_SHA', defaultValue: '', description: 'SHA del commit a reportar')
    }

    environment {
        GITHUB_APP = credentials('github-checks-app') 
        REPO = 'Manuinng/ecomus'                  
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
                    script {
                        def testFailed = false
                        def resultXml = readFile 'results.xml'
                        if (resultXml.contains('failures="0"') && resultXml.contains('errors="0"')) {
                            testFailed = false
                        } else {
                            testFailed = true
                        }

                        def conclusion = testFailed ? 'FAILURE' : 'SUCCESS'

                        publishChecks(
                            name: 'Automated-tests',
                            conclusion: conclusion,
                            title: 'Test Result',
                            summary: conclusion == 'SUCCESS' ? '✅ All the test pass.' : '❌ Some test failed.',
                            commit: params.COMMIT_SHA
                        )
                    }
                }
            }
        }
    }
}
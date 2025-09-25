pipeline {
    agent any

    stages {
        stage('Test') {
            withPythonEnv('python3') {
                sh 'pip install pytest'
                sh 'cd backend && pytest mytest.py'
            }
        }
    }
}

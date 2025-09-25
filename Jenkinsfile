pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'cd backend'
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest'
                sh 'python -m pytest'
            }
        }
    }
}

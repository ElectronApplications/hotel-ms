pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest'
                sh 'cd backend && python -m pytest'
            }
        }
    }
}

pipeline {
    agent any

    stages {
        stage('Prepare') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    cd backend
                    python -m pip install -r requirements.txt
                    python -m pip install pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . .venv/bin/activate
                cd backend
                python -m pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cp .env.jenkins .env
                    cp local_settings.py.jenkins local_settings.py
                    podman-compose up
                '''
            }
        }
    }
}

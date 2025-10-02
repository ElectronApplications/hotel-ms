pipeline {
    agent any

    stages {
        stage('Prepare') {
            steps {
                sh ```
                    python -m venv .venv
                    source .venv/bin/activate
                    python -m pip install -r requirements.txt
                    python -m pip install pytest
                ```
            }
        }

        stage('Test') {
            steps {
                sh 'cd backend && python -m pytest'
            }
        }

        stage('Deploy') {
            steps {
                sh ```
                    source .venv/bin/activate
                    cd backend
                    python manage.py migrate
                    python manage.py runserver 1267
                ```
            }
        }
    }
}

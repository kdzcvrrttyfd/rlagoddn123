pipeline {
    agent any

    environment {
        // Git 커밋 해시로 이미지 버전 생성
        VERSION = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        DOCKER_IMAGE = "gcr.io/<your-project-id>/rlagoddn123:${VERSION}"
    }

    stages {
        // 1. 소스 코드 클론
        stage('Checkout') {
            steps {
                git credentialsId: 'your-credentials-id', url: 'https://github.com/kdzcvrrttyfd/rlagoddn123.git'
            }
        }

        // 2. 의존성 설치
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        // 3. 테스트 실행
        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover'
            }
        }

        // 4. Docker 이미지 빌드 및 푸시
        stage('Build & Push Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE} .
                docker push ${DOCKER_IMAGE}
                """
            }
        }

        // 5. Kubernetes 매니페스트 파일 업데이트
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/<your-repo>/k8s-manifests.git'
                    sh """
                    sed -i 's|image: .*|image: ${DOCKER_IMAGE}|' deployment.yaml
                    git commit -am "Update image to ${VERSION}"
                    git push
                    """
                }
            }
        }
    }
}

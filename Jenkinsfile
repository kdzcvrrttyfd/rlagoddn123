pipeline {
    agent any

    environment {
        // Docker 이미지 태그에 사용할 Git 커밋 해시
        VERSION = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        DOCKER_IMAGE = "your-docker-repo/app:${VERSION}"
    }

    stages {
        // 1. 소스 코드 클론
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Docker 이미지 빌드
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        // 3. Kubernetes 매니페스트 파일 업데이트
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    // Kubernetes 매니페스트 파일의 이미지 태그 업데이트
                    git branch: 'main', url: 'https://github.com/your-repo/k8s-manifests.git'
                    sh """
                    sed -i 's|image: .*|image: ${DOCKER_IMAGE}|' deployment.yaml
                    """
                    sh 'git commit -am "Update image to ${VERSION}"'
                    sh 'git push'
                }
            }
        }

        // 4. GKE 클러스터에 배포
        stage('Deploy to GKE') {
            steps {
                script {
                    // Google Cloud 인증
                    withCredentials([file(credentialsId: 'gke-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh "gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}"
                        sh "gcloud container clusters get-credentials your-cluster-name --zone your-zone --project your-project-id"
                    }
                    
                    // kubectl을 사용하여 배포
                    sh 'kubectl apply -f deployment.yaml'
                }
            }
        }
    }
}



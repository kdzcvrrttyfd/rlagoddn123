pipeline {
    agent any

    environment {
        // GitHub 저장소 URL 및 도커 레지스트리 URL
        GITHUB_REPO = 'https://github.com/kdzcvrrttyfd/rlagoddn123.git'
        DOCKER_REGISTRY = 'your-docker-registry-url'
        DOCKER_IMAGE_NAME = 'your-docker-image-name'
        K8S_MANIFESTS_REPO = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git'
        K8S_MANIFEST_PATH = 'kubernetes/manifests'
        DOCKER_TAG = "${env.BUILD_ID}"

        // GKE 클러스터 정보
        GKE_PROJECT_ID = 'sidfjg'
        GKE_CLUSTER_NAME = 'kor-cluster'
        GKE_CLUSTER_ZONE = 'asia-northeast3' // 예: us-central1-a
    }

    stages {
        stage('Checkout GitHub Repos') {
            steps {
                script {
                    // GitHub 저장소에서 소스 코드 및 Kubernetes 매니페스트 파일을 체크아웃합니다.
                    checkout scm
                    // Kubernetes 매니페스트 저장소를 별도로 체크아웃
                    git branch: 'main', url: "${K8S_MANIFESTS_REPO}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Docker 이미지를 빌드하고 푸시합니다.
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG} .
                        docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                script {
                    // Kubernetes 매니페스트 파일에서 Docker 이미지 태그를 업데이트합니다.
                    sh """
                        sed -i 's|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:.*|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}|' ${K8S_MANIFEST_PATH}/deployment.yaml
                    """
                    // 변경된 매니페스트 파일을 GitHub 저장소에 푸시합니다.
                    sh """
                        git config --global user.email "youremail@example.com"
                        git config --global user.name "yourusername"
                        git add ${K8S_MANIFEST_PATH}/deployment.yaml
                        git commit -m "Update Docker image tag to ${DOCKER_TAG}"
                        git push origin main
                    """
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    // GKE 클러스터에 대한 인증을 설정합니다.
                    sh """
                        gcloud auth activate-service-account --key-file=/path/to/your/service-account-key.json
                        gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_CLUSTER_ZONE} --project ${GKE_PROJECT_ID}
                    """
                    // kubectl을 사용하여 Kubernetes 클러스터에 배포합니다.
                    sh """
                        kubectl apply -f ${K8S_MANIFEST_PATH}/deployment.yaml
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}

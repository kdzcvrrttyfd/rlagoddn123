pipeline {
    agent any

    environment {
        // GitHub 저장소 및 Docker 레지스트리 정보
        GITHUB_REPO = 'https://github.com/kdzcvrrttyfd/rlagoddn123.git'
        DOCKER_REGISTRY = 'docker.io/rlaekdh12345'
        DOCKER_IMAGE_NAME = 'qudwndh/shop'
        K8S_MANIFESTS_REPO = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git'
        K8S_MANIFEST_PATH = '~/3tier/was' // 수정된 경로
        DOCKER_TAG = "${env.BUILD_ID}"

        // GKE 클러스터 정보
        GKE_PROJECT_ID = 'sidfjg'
        GKE_CLUSTER_NAME = 'kor-cluster'
        GKE_CLUSTER_ZONE = 'asia-northeast3' // 예: asia-northeast3

        // Docker Hub 계정 정보
        DOCKER_USERNAME = 'rlaekdh12345'
        DOCKER_PASSWORD = 'rlagoddn123'
    }

    stages {
        stage('Checkout GitHub Repos') {
            steps {
                script {
                    // Jenkins 작업 공간으로 소스 코드 체크아웃
                    checkout scm
                    // Kubernetes 매니페스트 저장소 별도 체크아웃
                    dir('k8s-manifests') {
                        git branch: 'main', url: "${K8S_MANIFESTS_REPO}"
                    }
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    // Docker 레지스트리에 로그인
                    sh """
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Docker 이미지 빌드 및 레지스트리에 푸시
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
                    // Kubernetes 매니페스트 파일에서 Docker 이미지 태그 업데이트
                    dir('k8s-manifests') {
                        sh """
                            sed -i 's|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:.*|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}|' ${K8S_MANIFEST_PATH}/deployment.yaml
                        """
                        // 변경된 매니페스트 파일을 GitHub에 푸시
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
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    // GKE 인증 및 클러스터 컨텍스트 설정
                    sh """
                        gcloud auth activate-service-account --key-file=~/sidfjg-e6d6a9e59022.json
                        gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_CLUSTER_ZONE} --project ${GKE_PROJECT_ID}
                    """
                    // Kubernetes 클러스터에 새 매니페스트 배포
                    dir('k8s-manifests') {
                        sh """
                            kubectl apply -f ${K8S_MANIFEST_PATH}/deployment.yaml
                        """
                    }
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



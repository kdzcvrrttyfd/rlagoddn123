pipeline {
    agent any

    environment {
        // GitHub 저장소 및 Docker 레지스트리 정보
        GITHUB_REPO = 'https://github.com/kdzcvrrttyfd/rlagoddn123.git'
        DOCKER_REGISTRY = 'docker.io/rlaekdh12345'
        DOCKER_IMAGE_NAME = 'rlagoddn/shop'
        K8S_MANIFESTS_REPO = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git'
        K8S_MANIFEST_PATH = '3tier/was/flask-deployment.yaml'
        DOCKER_TAG = "${env.BUILD_ID}"

        // GKE 클러스터 정보
        GKE_PROJECT_ID = 'sdfasdf-429612'
        GKE_CLUSTER_NAME = 'kor-cluster'
        GKE_CLUSTER_ZONE = 'asia-northeast3'

        // Docker Hub 계정 정보
        DOCKER_USERNAME = 'rlaekdh12345'
        DOCKER_PASSWORD = 'rlagoddn123'
    }

    stages {
        stage('Checkout GitHub Repos') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: "${GITHUB_REPO}", credentialsId: 'github-creds']]])
                    dir('k8s-manifests') {
                        git branch: 'main', url: "${K8S_MANIFESTS_REPO}"
                    }
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    sh """
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
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
                    dir('k8s-manifests') {
                        sh """
                            sed -i 's|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:.*|image: ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}|' ${K8S_MANIFEST_PATH}
                            kubectl apply --dry-run=client -f ${K8S_MANIFEST_PATH} # 매니페스트 검증
                            git config --global user.email "rlaekdh12345@gmail.com"
                            git config --global user.name "kdzcvrrttyfd"
                            git add ${K8S_MANIFEST_PATH}
                            git commit -m "Update Docker image tag to ${DOCKER_TAG}"
                            git push https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/kdzcvrrttyfd/k8s-manifests.git main
                        """
                    }
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    sh """
                        gcloud auth activate-service-account --key-file=~/sdfasdf-429612-dd4349f4992b.json
                        gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_CLUSTER_ZONE} --project ${GKE_PROJECT_ID}
                        kubectl apply -f ${K8S_MANIFEST_PATH}
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





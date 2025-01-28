eline {
    agent any

    environment {
        dockerHubRegistry = 'rlaekdh12345/docker' // Docker Hub 레지스트리 경로
        dockerHubRegistryCredential = 'docker-hub' // Docker Hub 인증 ID
        githubCredential = 'github' // GitHub 인증 ID
        k8sRepoUrl = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git' // Kubernetes manifests Git URL
    }

    stages {
        // 1. Git repository 체크
        stage('Check Out Application Git Branch') {
            steps {
                checkout scm
            }
            post {
                failure {
                    echo 'Repository checkout failure'
                }
                success {
                    echo 'Repository checkout success'
                }
            }
        }

        // 2. Dockerfile 빌드
        stage('Docker Image Build') {
            steps {
                sh "docker build . -t ${dockerHubRegistry}:${currentBuild.number}"
                sh "docker build . -t ${dockerHubRegistry}:latest"
            }
            post {
                failure {
                    echo 'Docker image build failure!'
                }
                success {
                    echo 'Docker image build success!'
                }
            }
        }

        // 3. 빌드된 Docker 이미지 push
        stage('Docker Image Push') {
            steps {
                withDockerRegistry([credentialsId: dockerHubRegistryCredential, url: ""]) {
                    sh "docker push ${dockerHubRegistry}:${currentBuild.number}"
                    sh "docker push ${dockerHubRegistry}:latest"
                    sleep 10 // 업로드 대기
                }
            }
            post {
                failure {
                    echo 'Docker image push failure!'
                    sh "docker rmi ${dockerHubRegistry}:${currentBuild.number}"
                    sh "docker rmi ${dockerHubRegistry}:latest"
                }
                success {
                    echo 'Docker image push success!'
                    sh "docker rmi ${dockerHubRegistry}:${currentBuild.number}"
                    sh "docker rmi ${dockerHubRegistry}:latest"
                }
            }
        }

        // 4. Kubernetes manifests 업데이트
        stage('K8S Manifest Update') {
            steps {
                sh 'mkdir -p gitOpsRepo'
                dir("gitOpsRepo") {
                    git branch: "main",
                        credentialsId: githubCredential,
                        url: k8sRepoUrl
                    
                    sh "git config --global user.email 'rlaekdh12345@gmail.com'"
                    sh "git config --global user.name 'kdzcvrrttyfd'"

                    // deployment.yaml에서 docker 이미지 버전 업데이트
                    sh 'sed -i "s/docker:.*$/docker:${currentBuild.number}/" deployment.yaml'
                    sh "git add deployment.yaml"
                    sh "git commit -m '[UPDATE] k8s ${currentBuild.number} image versioning'"

                    withCredentials([gitUsernamePassword(credentialsId: githubCredential, gitToolName: 'git-tool')]) {
                        sh "git remote set-url origin ${k8sRepoUrl}"
                        sh "git push -u origin main"
                    }
                }
            }
            post {
                failure {
                    echo 'K8S Manifest Update failure!'
                }
                success {
                    echo 'K8S Manifest Update success!'
                }
            }
        }
    }
}














pipeline {
    agent any

    environment {
        dockerHubRegistry = 'rlaekdh12345/docker' // dockerHub에 repository 명
        dockerHubRegistryCredential = 'docker-hub' // Jenkins에서 생성한 dockerhub-credential-ID값
        githubCredential = 'github' // Jenkins에서 생성한 github-credential-ID값
        k8sRepoUrl = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git' // 수정된 Git 레포지토리 URL
    }

    stages {
        // 1. git repository 체크
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
                // Dockerfile을 이용하여 이미지를 빌드
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

        // 3. 빌드된 Docker 이미지 푸시
        stage('Docker Image Push') {
            steps {
                withDockerRegistry([credentialsId: dockerHubRegistryCredential, url: ""]) {
                    sh "docker push ${dockerHubRegistry}:${currentBuild.number}"
                    sh "docker push ${dockerHubRegistry}:latest"
                    sleep 10 // Wait for upload
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

        // 4. K8S 매니페스트 업데이트
        stage('K8S Manifest Update') {
            steps {
                sh "ls"
                sh 'mkdir -p gitOpsRepo'
                dir("gitOpsRepo") {
                    git branch: "main",
                        credentialsId: githubCredential,
                        url: k8sRepoUrl // 수정된 URL 사용
                    sh "git config --global user.email 'rlatkd1089@naver.com'" // 수정된 이메일
                    sh "git config --global user.name 'rlagoddn123'" // 수정된 사용자 이름
                    // 배포될 때마다 버전이 올라야 하므로, deployment.yaml에서 이미지 버전을 업데이트
                    sh "sed -i \\"s/docker:.*\\\\$/docker:${currentBuild.number}/\\" deployment.yaml"
                    sh "git add deployment.yaml"
                    sh "git commit -m '[UPDATE] k8s ${currentBuild.number} image versioning'"
                    withCredentials([gitUsernamePassword(credentialsId: githubCredential,
                                                         gitToolName: 'git-tool')]) {
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














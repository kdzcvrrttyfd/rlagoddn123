pipeline {
    agent any

    environment {
        dockerHubRegistry = 'rlaekdh12345/k8s'
        dockerHubRegistryCredential = 'docker-hub'
        githubCredential = 'github'
    }

    stages {
        stage('check out application git branch') {
            steps {
                checkout scm
            }
            post {
                failure {
                    echo 'repository checkout failure'
                }
                success {
                    echo 'repository checkout success'
                }
            }
        }
        stage('docker image build') {
            steps {
                bat "docker build . -t ${dockerHubRegistry}:${currentBuild.number}"
                bat "docker build . -t ${dockerHubRegistry}:latest"
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
        stage('Docker Image Push') {
            steps {
                withDockerRegistry([credentialsId: dockerHubRegistryCredential, url: ""]) {
                    bat "docker push ${dockerHubRegistry}:${currentBuild.number}"
                    bat "docker push ${dockerHubRegistry}:latest"
                    bat "timeout /t 10 >nul" /* Wait uploading */
                }
            }
            post {
                failure {
                    echo 'Docker Image Push failure!'
                    bat "docker rmi ${dockerHubRegistry}:${currentBuild.number}"
                    bat "docker rmi ${dockerHubRegistry}:latest"
                }
                success {
                    echo 'Docker image push success!'
                    bat "docker rmi ${dockerHubRegistry}:${currentBuild.number}"
                    bat "docker rmi ${dockerHubRegistry}:latest"
                }
            }
        }
        stage('K8S Manifest Update') {
            steps {
                bat "dir"
                bat 'mkdir gitOpsRepo'
                dir("gitOpsRepo") {
                    git branch: "main",
                        credentialsId: githubCredential,
                        url: '<https://github.com/skarltjr/kube-manifests.git>'
                    bat "powershell -Command \"(Get-Content deployment.yaml) -replace 'k8s:.*\\$', 'k8s:${currentBuild.number}' | Set-Content deployment.yaml\""
                    bat "git add deployment.yaml"
                    bat "git commit -m \"[UPDATE] k8s ${currentBuild.number} image versioning\""
                    withCredentials([gitUsernamePassword(credentialsId: githubCredential,
                                                         gitToolName: 'git-tool')]) {
                        bat "git remote set-url origin <https://github.com/skarltjr/kube-manifests>"
                        bat "git push -u origin main"
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










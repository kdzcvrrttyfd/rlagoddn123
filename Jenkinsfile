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
        stage('Docker Image Push') {
            steps {
                withDockerRegistry([credentialsId: dockerHubRegistryCredential, url: ""]) {
                    sh "docker push ${dockerHubRegistry}:${currentBuild.number}"
                    sh "docker push ${dockerHubRegistry}:latest"
                    sleep 10 /* Wait uploading */
                }
            }
            post {
                failure {
                    echo 'Docker Image Push failure!'
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
        stage('K8S Manifest Update') {
            steps {
                sh "ls"
                sh 'mkdir -p gitOpsRepo'
                dir("gitOpsRepo") {
                    git branch: "main",
                        credentialsId: githubCredential,
                        url: '<https://github.com/skarltjr/kube-manifests.git>'
                    sh "sed -i 's/k8s:.*\\$/k8s:${currentBuild.number}/' deployment.yaml"
                    sh "git add deployment.yaml"
                    sh "git commit -m '[UPDATE] k8s ${currentBuild.number} image versioning'"
                    withCredentials([gitUsernamePassword(credentialsId: githubCredential,
                                                         gitToolName: 'git-tool')]) {
                        sh "git remote set-url origin <https://github.com/skarltjr/kube-manifests>"
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








pipeline {
    agent any

    environment {
        dockerHubRegistry = 'rlaekdh12345/docker'
        dockerHubRegistryCredential = 'docker-hub'
        githubCredential = 'github'
        k8sRepoUrl = 'https://github.com/kdzcvrrttyfd/k8s-manifests.git'
        BUILD_NUMBER = "${currentBuild.number}"
    }

    stages {
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

        stage('Docker Image Build') {
            steps {
                sh "docker build . -t ${dockerHubRegistry}:${BUILD_NUMBER}"
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
                    sh "docker push ${dockerHubRegistry}:${BUILD_NUMBER}"
                    sh "docker push ${dockerHubRegistry}:latest"
                    sleep 10
                }
            }
            post {
                failure {
                    echo 'Docker image push failure!'
                    sh "docker rmi ${dockerHubRegistry}:${BUILD_NUMBER}"
                    sh "docker rmi ${dockerHubRegistry}:latest"
                }
                success {
                    echo 'Docker image push success!'
                    sh "docker rmi ${dockerHubRegistry}:${BUILD_NUMBER}"
                    sh "docker rmi ${dockerHubRegistry}:latest"
                }
            }
        }

        stage('K8S Manifest Update') {
            steps {
                sh 'mkdir -p gitOpsRepo'
                dir("gitOpsRepo") {
                    git branch: "main",
                        credentialsId: githubCredential,
                        url: k8sRepoUrl

                    sh '''
                    #!/bin/bash
                    git config --global user.email 'rlaekdh12345@gmail.com'
                    git config --global user.name 'kdzcvrrttyfd'
                    sed -i "s/docker:.*$/docker:${BUILD_NUMBER}/" deployment.yaml
                    git add deployment.yaml
                    git commit -m '[UPDATE] k8s ${BUILD_NUMBER} image versioning'
                    '''

                    withCredentials([usernamePassword(credentialsId: githubCredential, usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh '''
                        #!/bin/bash
                        git remote set-url origin https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/kdzcvrrttyfd/k8s-manifests.git
                        git push -u origin main
                        '''
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
















pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'mi-app-python'
        IMAGE_TAG = "v${1}"
    }
    
   
        stage('Construir Imagen Docker') {
            steps {
                script {
                    echo "Construyendo la imagen Docker..."

                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                    
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Ejecutar Contenedor') {
            steps {
                script {
                    echo "Ejecutando el script de Python..."

                    sh "docker run --rm ${IMAGE_NAME}:latest"
                }
            }
        }
    }
    
    post {
        always {
            echo "Limpieza final de recursos..."

            sh "docker image prune -f"
        }
        success {
            echo "✅ ¡El pipeline se ejecutó con éxito y tu script corrió sin errores!"
        }
        failure {
            echo "❌ El pipeline falló. Revisa los logs de los contenedores o la construcción."
        }
    }
}
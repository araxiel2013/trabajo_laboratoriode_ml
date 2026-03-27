pipeline {
    agent {
        docker { 
            image 'python:3.9-slim' 
        }
    }

    stages {
        stage('1. Checkout del repositorio') {
            steps {
                checkout scm
            }
        }

        stage('2. Instalación de dependencias') {
            steps {
                echo "Instalando librerías..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('3. Pruebas básicas del dataset') {
            steps {
                echo "Verificando el dataset..."
                sh '''
                python -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('sdss_sample.csv')
    print('Dataset cargado. Filas:', len(df))
except Exception as e:
    print('Error leyendo el dataset:', e)
    sys.exit(1)
"
                '''
            }
        }

        stage('4. Ejecución del script principal') {
            steps {
                echo "Ejecutando main.py..."
                sh 'python main.py'
            }
        }

        stage('5. Almacenamiento de artefactos') {
            steps {
                echo "Guardando resultados..."
                archiveArtifacts artifacts: '**/*.png, **/*.csv, **/*.txt', allowEmptyArchive: true
            }
        }
    }
}
# flaws-aws-automation
Este script automatiza el análisis, la explotación y encadena las vulnerabilidades de los 3 primeros niveles de la plataforma de aprendizaje **flaws.cloud**. Permite auditar configuraciones incorrectas comunes en entornos AWS de manera secuencial y didáctica.

## Niveles Automatizados

* **Nivel 1 (S3 Abierto al Público)**: Descubrimiento de buckets expuestos mediante peticiones HTTP directas.
* **Nivel 2 (Permisos S3 para Usuarios Autenticados)**: Listado y extracción de archivos utilizando cualquier cuenta de AWS válida.
* **Nivel 3 (Fuga de Credenciales e Historial Git)**: Clonación y análisis automatizado de repositorios expuestos en busca de Access Keys en el historial.

---

## Requisitos Previos

Antes de ejecutar el script, asegúrese de contar con lo siguiente en su máquina:

* **Python 3.10+** instalado.
* Una **cuenta de AWS** activa (para las credenciales del Nivel 2).

---

## Instalación y Configuración
### 1. Configurar el Entorno Virtual
Las pruebas se realizaron dede una máquina kali

Cree y active un entorno aislado para instalar las dependencias requeridas

* **Linux**:
  ```bash
  sudo apt install -y python3-virtualenv
  virtualenv venv
  source venv/bin/activate
  ```

### 2. Instalar Dependencias
Instale los paquetes necesarios dentro del entorno activo usando `pip`:

```bash
pip install -r requirements.txt
```

```bash
sudo apt install dnsutils
```

```bash
sudo apt install git
```

### 3. Configurar las Credenciales de AWS
Para que el script pueda interactuar con AWS (necesario a partir del Nivel 2), configure un usuario IAM con el permiso mínimo recomendado (`AmazonS3ReadOnlyAccess`) dentro de la consola oficial de aws y genere las Access key ID y Secret Access Key:

```bash
aws configure
```
modifique el archivo ~/.aws/credentials y ~/.aws/configure
cambie el nombre "default" por el nombre de perfil de la cuenta IAM

verifique con el siguiente comando:

```bash
aws sts get-caller-identity 
```

---

## Uso del Script

Una vez activado el entorno virtual y configurado el CLI, ejecute:

```bash
python flaws_chaining.py
```

El script mostrará en la terminal el progreso de cada nivel.



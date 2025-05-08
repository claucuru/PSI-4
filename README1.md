## COMANDOS

### **GitHub**
Con el archivo de gitinit.sh hacemos:
```Bash
bash gitinit.sh --config --keygen --port 443
```
Copiamos la clave como se nos indica y  vamos a:
1. Ajustes
3. SSH KEYS
4. Añadimos la nueva clave copiándola en el recuadro grande
5. Vamos al repositorio
6. Pulsamos en botón code
7. Damos a clave SSH
8. Copiamos dirección
9. Hacemos:
```
git clone <<direccion_copiada>>
```

### **Entorno virtual**
Crear el entorno
``` Bash
 python -m venv p_env
```

Entrar en el entorno
``` Bash
source p_env/bin/activate
```

Instalar requirements.txt una vez en el entorno (está en chesstournament)
``` Bash
pip install -r requirements
```
### **Vue**
Instalar el vue en el ordenador dentro del chesstournament-client
``` Bash
npm install vue@3.5.13
```
``` Bash
npm install
```
Dentro de la carpeta chesstournament-client
``` Bash
npm run dev
```

### **Cypress**

Abrir el cypress
```
npx cypress open
```

## **Activar postgres y BBDD**
Hacer:

sudo systemctl restart postgresql

1. Cambiar todo 8000 por 8001
2. Cambiar urls de python y manage.py en el json
3. Hacer make clear_db
4. Hacer python3 manage.py makemigrations chess_models
5. Hacer python manage.py migrate
6. Hacer make create_super_user

## **Entrar base de datos**
psql -U alumnodb -d chess -h localhost


# **Plataformas**
![ringa-tech](https://i.ytimg.com/vi/_BjL6W71mWY/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLC_f9QnPnhjeRFvzGYkR2cuDj7c5w)

## **Información general**
Este repositorio contiene el código para el juego de Plataformas controlado por la boca cara usando Facemesh, como fue creado en mi canal de Youtube:
[Ringa-Tech](https://youtu.be/_BjL6W71mWY)


---
## **Importante**
El juego puede controlarse con la barra espaciadora, o abriendo/cerrando la boca.
El tema de abrir y cerrar la boca no es perfecto, depende del angulo en el que tienes la cara vs la camara, entre otras cosas. Abre y cierra bien la boca para que lo detecte, y si batallas, puedes ayudarme a mejorarlo!

---

## **Información Adicional:**

Este juego no puede ser ejecutado en terminales de subsistemas Linux. Cómo WSL, WSL2, Termux, entre otros. Debido a que hay problemas con los triggers. 
Se puede ejecutar pero es una tarea demasiado complicada. Te comparto está información de [Stackoverflow](https://stackoverflow.com/questions/65939167/problem-using-opencv-in-wsl-when-opening-windows) en caso de que lo quieras intentar.

---
## **Configuración inicial**
El proyecto lo hice con Python 3.7.9.
Pero mediaPipe acepta versiones desde 3.6, hasta 3.10.

<details><summary><b>Instalar en WINDOWS:</b></summary>

### ***Sigue los siguentes pasos:***

Revisar versión de Python:
```
python --version
```
Crear un ambiente virtual:
```
python3 -m virtualenv venv
```
Activar ambiente virtual:
```
.\venv\Scripts\activate
```
Actualizar pip:
```
python.exe -m pip --upgrade pip
```
Para instalar las dependencias es necesario ejecutar
```
pip install -r requirements.txt
```
</details>

---
<details><summary><b>Instalar en LINUX:</b></summary>

### ***Sigue los siguentes pasos:***

Revisar versión de Python:
```
python --version
```
Crear un ambiente virtual:
```
python3 -m venv venv
```
Activar ambiente virtual:
```
source venv/bin/activate
```
Actualizar pip:
```
python -m pip --upgrade pip
```
Para instalar las dependencias es necesario ejecutar
```
pip install -r requirements.txt
```

</details>


---
## **Descarga de imágenes**
Por motivos de Copyright, no puedo incluir las imágenes que usé en el juego aquí.
Pero puedes descargarlas de manera gratuita! Tal cual como se muestra en el video.

Te dejo aquí las instrucciones:

- Descargar el paquete de personajes y descomprimir la carpeta '2 Punk' en la carpeta 'sprites':
	- [Paquete de personajes](https://bit.ly/3vxIk3W)
 - Descargar el paquete de fondos y descomprimir la carpeta '1 Backgrounds' en la carpeta 'sprites':
	- [Paquete de fondos](https://bit.ly/3i9X0mS)
 - Descargar el paquete de pisos, señalamientos, etc y descomprimir las carpetas '1 Tiles' y '4 Animated objects' en la carpeta 'sprites':
	- [Paquete de pisos etc](https://bit.ly/3GdSn2W)
 - Descomprimir el paquete de enemigos de zona verde. En 'sprites' crear una carpeta llamada 'City Enemies' y dentro descomprimir la carpeta '5':
	- [Paquete de enemigos](https://bit.ly/3WXAZGt)

 Al final debes quedar con la siguiente estructura:

 - sprites
	- 1 Backgrounds
	- 1 Tiles
	- 2 Punk
	- 4 Animated objects
	- City Enemies
		- 5

## **Ejecutar el juego**

El siguiente comando para ejecutar el juego:

**WINDOWS**
```
python .\app.py
```
**LINUX**
```
python ./app.py
```

Si no te funciona, prueba usando "python3" o "py" en lugar de "python" en el comando anterior.

---
## **¿Problemas?**

En ese caso por favor levanta un [**issue** aquí en Github](https://github.com/ringa-tech/juego-python-ia-plataforma/issues), con el mayor detalle que puedas (versión de python, de paquetes, mensaje completo de error, etc).

Si eres ninja y lo solucionas, ¡levanta un [Pull Request!](https://github.com/ringa-tech/juego-python-ia-plataforma/pulls)

![logo-Ringa-tech](https://www.ringa-tech.com/LogotipoV2-Simple.png)

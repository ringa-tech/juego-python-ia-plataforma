# Plataformas

## Información general
Este repositorio contiene el código para el juego de Plataformas controlado por la boca cara usando Facemesh, como fue creado en mi canal de Youtube:
https://youtu.be/_BjL6W71mWY

## Importante
El juego puede controlarse con la barra espaciadora, o abriendo/cerrando la boca.
El tema de abrir y cerrar la boca no es perfecto, depende del angulo en el que tienes la cara vs la camara, entre otras cosas. Abre y cierra bien la boca para que lo detecte, y si batallas, puedes ayudarme a mejorarlo!

## Configuración inicial
El proyecto lo hice con Python 3.7.9
Para instalar las dependencias es necesario ejecutar
```
pip install -r requirements.txt
```

## Descarga de imágenes
Por motivos de Copyright, no puedo incluir las imágenes que usé en el juego aquí.
Pero puedes descargarlas de manera gratuita! Tal cual como se muestra en el video.

Te dejo aquí las instrucciones:

 - Descargar el paquete de personajes y descomprimir la carpeta '2 Punk' en la carpeta 'sprites':
	1.1. [Paquete de personajes](https://bit.ly/3vxIk3W)
 - Descargar el paquete de fondos y descomprimir la carpeta '1 Backgrounds' en la carpeta 'sprites':
	2.1. [Paquete de fondos](https://bit.ly/3i9X0mS)
 - Descargar el paquete de pisos, señalamientos, etc y descomprimir las carpetas '1 Tiles' y '4 Animated objects' en la carpeta 'sprites':
	3.1. [Paquete de pisos etc](https://bit.ly/3GdSn2W)
 - Descomprimir el paquete de enemigos de zona verde. En 'sprites' crear una carpeta llamada 'City Enemies' y dentro descomprimir la carpeta '5':
	4.1. [Paquete de enemigos](https://bit.ly/3WXAZGt)

 Al final debes quedar con la siguiente estructura:

 - sprites
	- 1 Backgrounds
	- 1 Tiles
	- 2 Punk
	- 4 Animated objects
	- City Enemies
		- 5

## Ejecutar el juego

Para ejecutar el juego, ejecutar

```
python .\app.py
```
Si no te funciona, prueba usando "python3" o "py" en lugar de "python" en el comando anterior.
## ¿Problemas?

Solo he probado el juego en mi equipo así que seguramente puedes encontrar problemas.

En ese caso por favor levanta un issue aquí en Github, con el mayor detalle que puedas (versión de python, de paquetes, mensaje completo de error, etc).

Si eres ninja y lo solucionas, ¡levanta un Pull Request!
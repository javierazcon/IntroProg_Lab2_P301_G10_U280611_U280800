# IntroProg_Lab2_P301_G10_U280611_U280800

## Trabajo realizado:
Esta nueva práctica 2 nos pide que hagamos un juego de ping-pong configurando las funciones que usa al ejecutarse, por lo tanto, primero tenemos que entender como quiere el programa que funcione, y por eso nos hemos mirado la guía del programa y así poder hacer unas funciones óptimas. 

Nos hemos repartido el trabajo del programa entre los 2 para ayudarnos y entender bien el programa, el cual ha ido de forma progresiva, empezando por funciones básicas como “ask_yes_no”, “read_color”, “read_int_in_range” las cuales las hemos hecho conjuntamente, para entender los dos las bases que usarían el resto de funciones requeridas durante el código.

Después, Javier ha hecho la función “get_config” y “read_color”, y Eric con colaboración de Javier ha realizado el resto de funciones.

## Funcionamento del programa:
El programa realizado se organiza prácticamente con main(), el cual grita los valores de las funciones creadas, o sea los valores que hemos devuelto a cada una de las funciones con return.

Antes que nada el que pide el programa son las funciones de configuración, o sea “get_config” y “change_colors” las cuales con la función “ask_yes_no” preguntan al usuario si quieren hacer cambios a las variables predeterminadas, y con “read_int_in_range” y “read_color” leen los valores introducidos por el usuario en cada una de las variables, por así poder devolverlas al código principal y ejecutarlas.

Seguidamente de esto, el que hace el programa es abrir la ventana ya preconfigurada y hace la primera llamada con la función “reset_ball”. Por lo tanto, empieza un bucle en el cual constantemente se calculan los movimientos de las palas con “move_paddle”, los movimientos de la bola con “move_ball”, y finalmente las colisiones con “collide_ball_walls” y “collide_ball_paddle”, hasta que uno de los 2 lados puntúe y, por lo tanto, vuelva a empezar con “reset_ball”.

En el código el que hacemos es devolver siempre valores, y por eso no cambiamos las variables globales, sino que estos valores devueltos son captados a main() y les usa constantemente durante el juego, como por ejemplo en el movimiento de la pala, donde “move_paddle” calcula la posición de la pala, la devuelve a main() y la guarda la variable “new_y” devuelta en “p1_y” y “p2_y”.

## Decisiones clave de implementación:
### Colisión entre la bola y la pala: 
Primero de todo, tratamos la bola como si fuese un rectángulo, así sería más sencillo saber si un rectángulo y un cuadrado se tocan.

Para conseguirlo, primero calculamos los 4 bordes que forman el perímetro de los rectángulos. Estos se tocan cuando se superponen tanto como el lado horizontal como el vertical al mismo tiempo, esto se hace para exceptuar casos en los que la pala y la bola se encuentran a la misma altura pero en el centro de la pantalla, en donde no debe rebotar porque no está en contacto con la pala.

Ahora bien, para lograr esto debemos limitar la condición de choque a la siguiente: que la bola no esté entera a la izquierda, derecha, arriba o abajo de la pala. Esto lo hacemos mediante comparaciones simultáneas comparando el borde de la bola con el de la pala. Además, así detectamos también cuando la bola toca con la esquina de la pala.

No tan solo eso, sino que cuando la bola choca no basta tan solo con cambiarle la dirección, como superponemos la pala con la bola hay píxeles que se quedan con la bola que al detectar todo el rato el contacto haría que cambiase de sentido todo el rato la bola.
Para arreglarlo, hacemos que cuando entre en contacto la bola con la pala, se mueva un poco de la pala para evitar esos píxeles que se quedan y la cambiamos de dirección horizontal. Para saber de dónde se tiene que despegar la bola primero comprobamos de donde venía.

### Validación de datos del menú:
Cómo no queríamos que el programa se cerrará debido a que el usuario no introduce datos correctos, el programa persiste hasta conseguir la configuración que quiera el usuario.

Podemos encontrar dos casos de error (por datos erróneos):
Que no sea un número: en casos en donde el usuario pone una palabra, una letra o algo que no sea un número y, en vez de que pete el programa, le hacemos un print sobre que el valor no es correcto y que debe introducir uno correcto, introduciendolo en la caja del try/except para evitar que se rompa el programa.
Que sea un número fuera del rango permitido: casos donde el usuario pone cifras descomunales, como puede ser 500. El programa funciona hasta un punto, en donde detecta que se queda corto o sobrepasa los límites impuestos y volverá a preguntar al usuario un valor.

Para que el usuario sea consciente de entre qué dos números es el rango permitido se le muestra el rango. Este rango lo hemos elegido para que siempre se incluya el valor predeterminado que da el programa, para que se pueda jugar con la configuración inicial.

En las preguntas de sí o no, las respuestas se convierten en minúscula y les quitamos los espacios, admitiendo respuestas cómo: “Y”, “yes”, “NO”, entre otras.

### Funciones opcionales:
El saque aleatorio: el docstring provoca una pequeña variación de la velocidad vertical. Al elegir la al azar la dirección y la inclinación de la bola, esto la convierte en saques más variados, con valores entre 1 y un poco más de la velocidad por defecto para evitar que siempre salga en horizontal.

## Problemas y soluciones: 
### 1er problema, modificación de constantes dentro de una función: 
- En la primera versión del get_config() guardábamos los valores nuevos a PADDLE_H, etc. Cuando respondíamos “no”, el programa daba error. Nos dimos cuenta de que cuando decíamos el “no”, como llamábamos a la variable dentro de la función ya la convertía en una local y que al decir el “no” ya no las volvía a encontrar en todo el código.
### 2do problema, validación de números: 
- Primero, comparábamos la respuesta del usuario sin pasarla por el try y cuando el usuario ponía un texto el programa se cerraba directamente con un typeerror, entonces decidimos comprobar los int con un try y el except valueerror para estos casos.
### 3er problema, errores relacionados con el main(): 
- Tuvimos algunos errores del tipo “cannot unpack”. Esto era debido a algunas funciones en donde o devolvíamos un solo valor en vez de dos, como en move_ball() o que en reset_ball() el return quedaba dentro de un if, así que la bola en el caso de salir a la izquierda el código daba un none en el main().
### 4to problema, detección de colisión: 
- La primera versión detectaba si coincidía un solo lado de la pala y la bola, haciendo así que rebotara con tan solo coincidir un lado hasta en el centro de la pantalla. Para esto, lo resolvimos haciendo que se solapen 2 lados a la vez, comparando el borde de la bola con el opuesto de la pala.
### 5to problema, la pala se salía de la pantalla: 
- Limitábamos la posición con la altura de la pantalla, donde no tuvimos en cuenta que y era el borde superior de la pala. Ahora bien, lo corregimos usando como límite la altura de la pantalla menos la altura de la pala.

## Test del codigo:
Lo que hemos hecho para poder testear el código mientras lo escribíamos es hacer diferentes prints probando las diferentes funciones para ver que es el que devolvían, como por ejemplo haciendo prueba del “read_int_in_range(“prueba”,1,10). Después, para ver en qué casos podría dar error, hemos ido probando dando valores incorrectos para ver cuando se rompe el programa y como lo podemos solucionar.

## Declaración del uso de IA:
La inteligencia artificial utilizada en esta práctica ha estado principalmente Claude, para entender conceptos y funcionamiento de algunos parámetros dentro de main(), interpretar mensajes de errores del código, revisión de cada versión hecha y organización para hacer el informe.

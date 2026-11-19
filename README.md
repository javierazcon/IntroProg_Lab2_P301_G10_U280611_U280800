# IntroProg_Lab2_P301_G10_U280611_U280800

## Treball fet:
Aquesta nova pràctica 2 ens demana que fem un joc de ping-pong configurant les funcions que fa servir en executar-se, per tant, primer hem d’entendre com vol el programa que funcioni, i per això ens hem mirat la guia del programa i així poder fer unes funcions òptimes. 

Ens hem repartit el treball del programa entre els 2 per ajudar-nos i entendre bé el programa, el qual ha anat de forma progressiva, començant per funcions bàsiques com “ask_yes_no”,  “read_color”, “read_int_in_range” les quals les hem fet conjuntament, per entendre tots dos les bases que farien servir la resta de funcions requeridas durant el codi.

Després, en Javier ha fet la funció “get_config” i “read_color”, i l’Eric amb colaboració d’en Javier ha realitzat la resta de funcions.

## Funcionament del programa:
El programa realitzat s’organitza pràcticament amb main(), el qual crida els valors de les funcions creades, o sigui els valors que hem retornat a cadascuna de les funcions amb return.

Primer de tot el que demana el programa són les funcions de configuració, o sigui “get_config” i “change_colors” les quals amb la funció “ask_yes_no” pregunten a l’usuari si volen fer canvis a les variables predeterminades, i amb “read_int_in_range” i “read_color” llegeixen els valors introduïts per l’usuari en cadascuna de les variables, per així poder retornar-les al codi principal i executar-les.

Seguidament d’això, el que fa el programa és obrir la finestra ja preconfigurada i fa el primer llençament amb la funció “reset_ball”. Per tant, comença un bucle en el qual constantment es calculen els moviments de les pales amb “move_paddle”, els moviments de la bola amb “move_ball”, i finalment les col·lisions amb “collide_ball_walls” i “collide_ball_paddle”, fins que un dels 2 costats puntuï i, per tant, torni a començar amb “reset_ball”.

En el codi el que fem és retornar sempre valors, i per això no canviem les variables globals, sinó que aquests valors retornats són captats a main() i els fa servir constantment durant el joc, com per exemple en el moviment de la pala, on “move_paddle” calcula la posició de la pala, la retorna a main() i la guarda la variable “new_y” retornada en “p1_y” i “p2_y”.

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

## Test del codi:
El que hem fer per poder testejar el codi mentre ho escrivíem és fer diferents prints provant les diferents funcions per veure que és el que retornaven, com per exemple fent prova del “read_int_in_range(“prova”,1,10). Després, per veure en quins casos podria donar error, hem anat provant donant valors incorrectes per veure quan es trenca el programa i com ho podem solucionar.

## Declaració d’ús d’IA:
La intel·ligència artificial utilitzada en aquesta pràctica ha estat principalment Claude, per entendre conceptes i funcionament d’alguns paràmetres dins de main(),  interpretar missatges d’errors del codi, revisió de cada versió feta i organització per fer l’informe.

## Proyecto sobre Sistemas Recomendadores Basados en Contenido 
### Técnicas Avanzadas de Análisis de Datos
### Pablo Bethencourt Díaz
### Máster en Ciberseguridad e Inteligencia de Datos. Universidad de La Laguna
<hr>
<b> Índice: </b>
<ol>
  <li>Presentación del programa</li>
  <li>Ejecución del programa</li>
  <li>Lectura de los documentos</li>
  <li>Implementación mediante Sklearn</li>
  <li>Implementación </li>
  <li>Visualización de los resultados</li>
</ol>

#### 1. Presentación del programa
El software desarrollado para el proyecto es una aplicación de consola que recibe un fichero de texto plano, donde cada línea representa un documento, y devuelve los resultados obtenidos al aplicar TF-IDF. La aplicación de TF-IDF se lleva a cabo siguiendo dos procedimientos distintos: el implementado por la librería sklearn, y el visto en las transparencias de clase.

Además, también se calcula la similaridad del coseno para cada par de documentos, presentando los resultados en una tabla-matríz con la relación de cada uno de ellos.

#### 2. Ejecución del programa
El programa ha de ser ejecutado de la siguiente forma: 
<p><code>python recomender.py <i>documento.txt</i> </code></p>

En caso de no pasar ningún argumento, el programa lanzará un error con las instrucciones de uso. Únicamente tiene en cuenta el primer argumento, cualquier número de argumentos que se pasen después de este serán ignorados.

#### 3. Lectura de los documentos
Como ya se ha mencionado, cada línea representa un documento distinto, por lo que el fichero pasado como argumento se lee línea a línea:

![image](https://user-images.githubusercontent.com/43812499/156207318-405d245c-e810-4bd8-ac08-7029492b52ee.png)
Cada línea se procesa para:
- Eliminar los símbolos de puntuación y las comillas. 
- Convertir todas las palabras a minúscula. Esta función (al igual que la anterior) ya la realiza automáticamente sklearn en los métodos <code>TfidfVectorizer()</code> y <code>CountVectorizer()</code>, pero es necesario realizarlo manualmente para la implementación mediante las transparencias de la asignatura.
- Mediante una expresión regular, se eliminan los índices de cada documento.
- Cada uno de los documentos preprocesados se guardan en una nueva lista. Esta lista es la que se pasa a los métodos para aplicarles TF-IDF.

Para guardar los resultados, primero se crea un diccionario cuya clave es el identificador del documento (por ejemplo: doc_2) y cuyo valor es un nuevo diccionario con cada palabra del documento como clave y como valor una lista con cada uno de los indicadores para esa palabra. Vemos el esquema:

<code>{doc_1: { palabra_1: [<i>Índice</i>,<i>TF</i>, <i>IDF</i>, <i>TF-IDF</i>], palabra_2: [<i>Índice</i>,<i>TF</i>, <i>IDF</i>, <i>TF-IDF</i>]...},
{doc_2: ...}, {doc_3: ...}</code>

Cada conjunto de diccionarios se guarda en dos listas diferentes: una lista para cada resultado de cada implementación. El código para obtener esta estructura es el siguiente:

![image](https://user-images.githubusercontent.com/43812499/156210873-c18e11bf-8ef3-4436-a076-b5446fb486ee.png)

#### 4. Implementación mediante Sklearn
<ul>
  <li>Se obtiene el valor de la <b>frecuencia de término</b> mediante el método <i>CountVectorizer()</i></li>
  <li>Los valores de la <b>frecuencia inversa de documento</b> y del peso combinado de las dos medidas (<b>TF-IDF</b>) para cada palabra en cada documento, se obtiene con el método <i>TfidfVectorizer()</i></li>
  <li>Los resultados de <b>TF-IDF</b> se encuentran normalizados. En el informe se explica la operación que aplica el método en la normalización de los resultados.</li>
</ul>

![image](https://user-images.githubusercontent.com/43812499/156626265-8e55da7b-2b47-4503-99b8-e071863eed88.png)

Los resultados se vuelcan en la estructura descrita anteriormente y se llama a la función que permite calcular la <b>similitud del coseno</b> para cada documento.

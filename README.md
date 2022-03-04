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
  <li>Implementación de clase</li>
  <li>Ejemplo de uso</li>
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
  <li>Los valores de la <b>frecuencia inversa de documento</b> y del peso combinado de las dos medidas (<b>TF-IDF</b>) para cada palabra en cada término, se obtienen con el método <i>TfidfVectorizer()</i></li>
  <li>Los resultados de <b>TF-IDF</b> se encuentran normalizados. En el informe se muestra la operación que aplica el método en la normalización de los resultados.</li>
</ul>

![image](https://user-images.githubusercontent.com/43812499/156626265-8e55da7b-2b47-4503-99b8-e071863eed88.png)

Los resultados se vuelcan en la estructura descrita anteriormente y se llama a la función que permite calcular la <b>similitud del coseno</b> para cada documento.

![image](https://user-images.githubusercontent.com/43812499/156628001-c36175dd-8650-44b5-b1aa-2d59c1bdd72c.png)

Los resultados se guardan en un <i>dataframe</i> con los valores para cada par de documentos.

#### 5. Implementación de clase
<ul>
  <li>Se emplea nuevamente el método Countvectorizer() para hallar el número total de palabras en cada documento. Los resultados se añaden a un dataframe. Se define un valor “N” que representa el número total de documentos en la colección.</li>
<li>Se itera sobre cada uno de los documentos, y sobre cada término en cada documento.</li>
<li>Se halla el valor normalizado de la frecuencia de término mediante los valores del dataframe generado en el punto 1.</li>
</li>Se calcula el número de documentos en los que aparece el término  que se está iterando (ni) para determinar el valor del logaritmo del valor de “N” entre ni. El valor resultante representa la frecuencia inversa del documento para cada término.</li>
<li>Se multiplica directamente el valor de la frecuencia de término por la frecuencia inversa del documento y se obtiene el valor final del TF-IDF.</li>
<li>Todos estos valores se añaden a la estructura definida para la representación de los resultados.</li>
<li>Los valores del TF-IDF  se añaden a un nuevo dataframe para calcular posteriormente la similitud del coseno.</li>
<li>La similitud del coseno se obtiene aplicando el método cosine_similarity, de la misma forma en la que se calculó para la implementación mediante Sklearn.</li> 
</ul>
El código en el programa correspondiente a esta parte es el siguiente:

![image](https://user-images.githubusercontent.com/43812499/156837370-dcf3ae29-29f9-4b5e-a74b-700c7016b960.png)


#### 6. Ejemplo de uso
Se ejecuta el software con el documento de ejemplo definido en el enunciado del proyecto:

![image](https://user-images.githubusercontent.com/43812499/156635019-b2a04668-442b-4e41-88b9-3335ec0ec038.png)

El programa realizará todos los cálculos y mostrará un menú para visualizar los resultados obtenidos:

![image](https://user-images.githubusercontent.com/43812499/156836539-7d4d1c2d-3e57-4f64-b090-b3bf869557a9.png)

Las dos primeras opciones mostrarán los resultados obtenidos directamente en la terminal, la tercera opción guardará todos los resultados en un fichero. En la salida se listan todos los documentos: para cada documento se imprime una tabla con los resultados obtenidos para cada término, mostrando los índices en los que aparece el término, el valor de su frecuencia, el valor de la frecuencia inversa del documento y el valor del producto de estos dos (el valor normalizado en el caso de Sklearn). 

Justo debajo aparecerá una nueva tabla con la relación de los resultados de la similitud del coseno entre cada par de documentos. Un ejemplo de salida en consola puede ser el siguiente:

![image](https://user-images.githubusercontent.com/43812499/156836731-f48cb397-3d6e-47f6-a408-dd2faeae4aad.png)

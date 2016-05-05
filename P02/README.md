# Códigos de residuos cuadráticos

Se consideran dos códigos cíclicos *Cq*, *Cn*, ideales de

![alt text](https://github.com/Dr-Tredok/CodeTheory-2016-2/tree/master/P02/eqn/r.png "Reducción del campo")

donde

*x⁷ - 1 = (x - 1) (x³ + x + 1) (x³ + x² + 1)*

Definimos a los códigos como:

*Cq = < x³ + x + 1 > = < g(x) > = [7, 4] -* código

*Cn = < x³ + x² + 1> = < f(x) > = [7, 4] -* código

denominanados *códigos de residuos cuadráticos* **(QR)**. Además, ya que *7 ≡ -1 mod 8* entonces Cq y Cn son equivalentes; por otra parte, ambos códigos son equivalentes a un código Hamming [7, 4]. (Códigos perfectos)

## Algoritmos

Dado el código  C = *< g(x) >* y el polinomio del mensaje *m(x)* se usa la codificación sistemática.

### Codificación

Sea el polinomio asociado al mensaje:

![alttext](https://github.com/Dr-Tredok/CodeTheory-2016-2/tree/master/P02/eqn/mword.png "Mensaje a codificar")

es decir, palabras de longitud 4.

El algoritmo para la codificación es:

1. *a(x) = x³ m(x)* de grado 6.
2. *a(x) = q(x) g(x) + p(x)* donde *p(x)* es de grado a lo más 5
3. *c(x) = a(x) - p(x)*

podemos ver que el polinomio codificado es:

 ![alttext](https://github.com/Dr-Tredok/CodeTheory-2016-2/tree/master/P02/eqn/cword.png "Palabra en el código")

es decir, el mensaje está contenido en las últimas entradas.

### Decodificación

Dado el mensaje recibido *r(x)* se sigue el algoritmo:

1. *r(x) = q(x) g(x) + s(x)* donde *s(x)* es el síndrome de *r(x)*
2. Si *s(x)* = 0 entonces *r(x)* forma parte del código y se devuelven las últimas entradas.
3. Se obtiene *e(x) = p(x) g(x) + s(x)* el  polinomio de error y se corrige el polinomio: *r(x) = c(x) + e(x)*.
4. Dado *c(x)* se obtienen las últimas entradas.

## Implementación

Se usa la implementación de polinomios definida en *src/polybomial*.

Ya que las palabras en el código son de longitud 7, basta un byte para su representación. Aprovechando esta cualidad, un hash de un polinomio es el entero que representan sus coeficientes.

Al leer el archivo, por cada byte se obtienen dos conjuntos de 4 bits (mitad del bytestring) y se considera un mensaje a codificar. Para escribir el archivo codificado, se regresa la palabra de longitud 7 y se almacena como un byte completo (0 en el byte más significativo).

Para decodificar se leen dos bytes para obtener el byte asociado correspondiente.

### Uso

python3 main.py [option] [code] [file]

donde
  1. option: --encode para codificar [file], --decode para decodificarlo
  2. code: --cq para usar el código *Cq*, en otro caso, --cn
  3. file: el archivo a procesar

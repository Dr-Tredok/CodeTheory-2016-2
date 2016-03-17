"""
    Instrucciones

    Práctica 1. Calculadora de campos finitos.

    Para construir Fq con q = p^n se toma a Zp como base y un polinomio irreducible de grado n.
    En la interfaz:
        Se pide p=, n=, f=.
        El polinomio f se espera como una secuencia de números, separados por espacio:
            1 0 4 4 2 0 = x⁵ + 4x³ + 4x² + 2x
        Para generar... pues click al botón 'Generar'
        La lista de polinomios en el campo, aparece al centro.

    Implementación:
        Polinomios donde p=2: src.PolynomialZ2
        Demás polinomios: src.Polynomial
    Nota divertida:
        src.PolynomialZ2 tiene un atributo SIZE que indica el número de bits en que se agrupan los coeficientes.
        Se pueden probar usando por ejemplo, SIZE = 8. (SIZE = 32 equivale a un entero y no creo que sean tan ociosos como para poner uno mayor...)

    Operaciones:
        Se piden dos polinomios (cajas inferiores), en el mismo formato que el polinomio irreducible.
        La operación es ese botón del centro, al darle click cambia la operación y ésta se ejecuta hasta clickear el botón de '='

        + = suma de polinomios
        * = producto de polinomios
        ia = inverso aditivo del primer polinomio
        im = inverso multiplicativo
        ** = ¿qué potencia de alpha es?

        O si se prefiere, en la última entrada de texto, se pide una potencia de alpha y se devuelve inverso aditivo y multiplicativo (en ese orden aparecen)

    Se omite la notación pues se regresan salidas en formato polinomial, pero siempre están listados junto a su potencia respectiva.

    Implementación:
        Las clases que realmente hacen cosas están en la carpeta src. Lo demás son módulos que unen las piezas.

    Ejecución:
        Se ejecuta
            python3 campo-finito.py
        Se necesita instalar kivy para la GUI
            https://kivy.org/#home
        Espacio para probar individualmente:
            python3 playground.py

"""

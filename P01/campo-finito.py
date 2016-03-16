from src.field import FqField
from view.main import MainApp

campoFinito = None

def generate_field(p, n, f):
    global campoFinito

    try:
        prime = int(p)
        expnt = int(n)
        if n == 0:
            raise Exception("n >= 1")
        if p == 0:
            raise Exception("p >= 2")
        print("Trusting p is a prime number")
        campoFinito = FqField(prime, expnt, f)
        return campoFinito.list_elements()
    except ValueError:
        print("Ingresa valores numéricos")
    except Exception as e:
        print(e.args)
    return []

# operations = ["+", "*", "ia", "im", "**"]
def op_polynomial(poly1, poly2, n):
    global campoFinito

    try:
        a = campoFinito.reduce(poly1)
        b = campoFinito.reduce(poly2)
        
        if n == 0:
            return campoFinito.sum(a, b)
        elif n == 1:
            return campoFinito.product(a, b)
        elif n == 2:
            return campoFinito.get_isum(a)
        elif n == 3:
            return campoFinito.get_iproduct(a)
        elif n == 4:
            return campoFinito.get_apower(a)
        else:
            raise Exception("Unsupported operation")
    except Exception as e:
        print(e.args)
    return None

MainApp(generate_field, op_polynomial).run()

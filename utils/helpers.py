#funcion para centrar la ventanas del inicion de session y sistema principal.
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

#funcion para validar que solo se ingresen numeros en los entry
def solo_numeros(char):
    return char.isdigit() or char == ""

#funcion para validar que solo se ingresen numeros en los entry con limite de caracteres
def solo_numeros_con_limite(char, valor_actual, limite):
    if not char.isdigit() and char != "":
        return False
    return len(valor_actual) <= int(limite)

#funcion para validar que solo se ingresen letras en los entry
def solo_letras(char):
    return char.isalpha() or char.isspace() or char == ""
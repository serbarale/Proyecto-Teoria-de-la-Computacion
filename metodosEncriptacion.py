from cryptography.fernet import Fernet
print("----------MENU----------")
print("1.Método Cesar")
print("2.Método Vigenere")
print("3.Método Simetrico")
print("4.Método Bacon")
print(
    "Se le solicita escrbir el método de cifrado tal como esta en el menú, caso contrario el programa no lo reconocera")
metodo = input("Elige el método a utilizar: ")

# ============================================================================================================

if metodo == "Método Cesar":
    # cifrado cesar
    abc = "abcdefghijklmnopqrstuvwxyz"


    def cifrar(cadena, clave):
        text_cifrado = " "

        for letra in cadena:
            suma = abc.find(letra) + clave
            modulo = int(suma) % len(abc)
            text_cifrado = text_cifrado + str(abc[modulo])
        return text_cifrado


    def decifrar(cadena, clave):
        text_cifrado = " "

        for letra in cadena:
            suma = abc.find(letra) - clave
            modulo = int(suma) % len(abc)
            text_cifrado = text_cifrado + str(abc[modulo])
        return text_cifrado


    def main():
        print("-----Opciones-----")
        print("1.cifrar mensaje")
        print("2.descifrar mensaje")
        opcion = input("Escriba la opcion que desee: ")
        if opcion == "cifrar mensaje":
            c = str(input("Cadena a cifrar: ")).lower()
            n = int(input("clave numerica: "))
            print(cifrar(c, n))
        elif opcion == "descifrar mensaje":
            cc = str(input("Cadena a decifrar: ")).lower()
            cn = int(input("clave numerica: "))
            print(decifrar(cc, cn))
        else:
            print("Opcion no reconocida / no digitada correctamente")


    if __name__ == "__main__":
        main()

# ============================================================================================================

elif metodo == "Método Vigenere":
    # cifrado vigenere
    abc = "abcdefghijklmnopqrstuvwxyz"


    def cifrar(cadena, clave):
        text_cifrar = ""

        i = 0
        for letra in cadena:
            suma = abc.find(letra) + abc.find(clave[i % len(clave)])
            modulo = int(suma) % len(abc)
            text_cifrar = text_cifrar + str(abc[modulo])
            i = i + 1
        return text_cifrar


    def descifrar(cadena, clave):
        text_cifrar = ""

        i = 0
        for letra in cadena:
            suma = abc.find(letra) - abc.find(clave[i % len(clave)])
            modulo = int(suma) % len(abc)
            text_cifrar = text_cifrar + str(abc[modulo])
            i = i + 1
        return text_cifrar


    def main():
        print("-----Opciones-----")
        print("1.cifrar mensaje")
        print("2.descifrar mensaje")
        opcion = input("Escriba la opcion que desee: ")
        if opcion == "cifrar mensaje":
            c = str(input("cadena a cifrar:")).lower()
            clave = str(input("clave: ")).lower()
            print(cifrar(c, clave))
        elif opcion == "descifrar mensaje":
            c = str(input("cadena a descifrar:")).lower()
            clave = str(input("clave: ")).lower()
            print(descifrar(c, clave))
        else:
            print("Opcion no reconocida / no digitada correctamente")


    if __name__ == "__main__":
        main()

# ============================================================================================================

elif metodo == "Método Simetrico":


    def main():
        key = Fernet.generate_key()
        fernet = Fernet(key)

        print(f"Tu clave privada es: {key.decode('utf-8')}")

        clave_criptar = input("Ingresa la clave para encriptar: ").encode('utf-8')

        if clave_criptar == key:
            mensaje = input("Ingrese el mensaje a encriptar: ").encode('utf-8')
            mensaje_encriptado = fernet.encrypt(mensaje)
            print("Mensaje encriptado: ", mensaje_encriptado)
        else:
            print("Clave incorrecta. No puedes encriptar el mensaje.")

        clave_desencriptar = input("Ingresa la clave para desencriptar: ").encode('utf-8')
        if clave_desencriptar == key:
            mensaje_desencriptado = fernet.decrypt(mensaje_encriptado)
            print("Mensaje desencriptado: ", mensaje_desencriptado.decode('utf-8'))
        else:
            print("Clave incorrecta. No puedes desencriptar el mensaje.")

    if __name__ == "__main__":
        main()


# ============================================================================================================

elif metodo == "Método Bacon":
    print("metodo en proceso")

# ============================================================================================================

else:
    print("metodo no reconocido / digitado incorrectamente")
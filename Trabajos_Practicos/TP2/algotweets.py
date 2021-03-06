import sys
import csv
import random
import time
import datetime


def random_choice(d):
    clave_random = random.choices(list(d), weights=d.values())
    clave = clave_random[0]
    return clave


def mostrar_favoritos(cantidad):
    lista_fav = []
    contador = 0
    if cantidad > 0:
        with open('favoritos.csv', 'r', encoding='utf-8') as f:
            favoritos_csv = reversed(list(csv.reader(f, delimiter=',')))
            for tweet in favoritos_csv:
                if contador < cantidad:
                    lista_fav.append(str(tweet[1]).rstrip(','))
                    contador += 1
                else:
                    break
        print(f"\nUltimos {cantidad} favoritos: \n")
        for i in range(len(lista_fav)):
            print(f"- {lista_fav[i]} \n")
    elif cantidad == 0:
        with open('favoritos.csv', 'r', encoding='utf-8') as f:
            favoritos_csv = reversed(list(csv.reader(f, delimiter=',')))
            for tweet in favoritos_csv:
                lista_fav.append(tweet[1])

        print(f"\nLista de favoritos ordenados por mas reciente: \n")
        for i in range(len(lista_fav)):
            print(f"- {lista_fav[i]} \n")


def mostrar_trending(cantidad):
    """
    Recibe como parametro la cantidad de #hashtags con mayor aparicion que el usuario desea visualizar y los
    muestra en pantalla
    :param cantidad: numero entero (controlado antes de entrar). Cero para imprimir todos
    :return:Imprime los $cantidad de hashtags mas utilizados,si $cantidad > len(tweets) o $cantidad = 0 : imprime todos
    """
    tt = {}
    lista_hashtags = []

    # armo una lista de hashtags
    with open('tweets.csv', encoding="utf8", ) as f:
        tweets_csv = csv.reader(f, delimiter='\t')

        for tweet in tweets_csv:
            palabras = tweet[1].split()

            for i in range(len(palabras)):
                if palabras[i].startswith('#'):
                    lista_hashtags.append(palabras[i])

    for i in range(len(lista_hashtags)):
        if lista_hashtags[i] in tt.keys():
            tt[lista_hashtags[i]] += 1
        else:
            tt[lista_hashtags[i]] = 1

    # [:cantidad] con esto le pongo limite a la lista pero no me queda presentable para imprimir
    lista_hashtags_ordenada = list(sorted(tt, key=tt.get, reverse=True))
    # print(len(lista_hashtags_ordenada))

    print(f"\nEste es el top {cantidad} de #hashtags: \n")
    if cantidad > len(lista_hashtags_ordenada):
        for i in range(len(lista_hashtags_ordenada)):
            print(' ' + lista_hashtags_ordenada[i] + '\n')
    else:
        for i in range(cantidad):
            print(' ' + lista_hashtags_ordenada[i] + '\n')
    print('\n')


def generar_tweet(usuarios):
    """
    Genera un tweet en base a tweets anteriores de los usuarios indicados por consola
    :param usuarios: lista de los usuarios en base a los cuales se genera el tweet
    :return: se imprime el tweet generado y se pregunta si se lo quiere agregar a favoritos
    """
    # Diccionario de tweets {<usuario>: [tweets]}
    dic_tws = {}

    # Diccionario de palabras iniciales {<palabra> : cantidad de apariciones (al inicio)}
    dic_p_inicial = {}

    # Diccionario de palabras iniciales {<palabra> : cantidad de apariciones (al inicio)}
    dic_p_final = {}

    # Diccionario de proximas palabras {<palabra> : {<palabra_sgte> : apariciones }}
    dic_p_prox = {}

    tweet_generado = ''
    aux = {}
    usuarios_totales = []
    # Para hacerlo un poco mas realista, nadie escribe ni menos de 40 ni siempre los 280 caracteres
    longitud_tw = random.randrange(40, 280)
    hora_actual = str(datetime.datetime.now())

    try:
        # ----------------- POR SI LA LISTA VIENE VACIA ------------------------
        with open('tweets.csv', encoding="utf8", ) as f:
            tweets_csv = csv.reader(f, delimiter='\t')
            for linea in tweets_csv:
                aux[linea[0]] = 1

        for usuario in aux.keys():
            usuarios_totales.append(usuario)

        if len(usuarios) == 0:
            usuarios = usuarios_totales
        # ------------------- ES MEDIO REBUSCADO --------------------------------

        for usuario in usuarios:

            dic_tws_usuario = {}

            with open('tweets.csv', encoding="utf8", ) as f:
                tweets_csv = csv.reader(f, delimiter='\t')

                for tweet in tweets_csv:
                    if tweet[0] == usuario:
                        if usuario in dic_tws_usuario.keys():
                            dic_tws_usuario[usuario].append(tweet[1])
                            continue
                        else:
                            dic_tws_usuario[usuario] = [tweet[1]]

            dic_tws.update(dic_tws_usuario)

        for usuario in dic_tws.keys():
            for tweet in dic_tws[usuario]:
                lista = tweet.split()
                # print(lista)
                # Armo el diccionario con las palabras iniciales y sus apariciones
                if lista[0] in dic_p_inicial.keys():
                    dic_p_inicial[lista[0]] += 1
                    # print(f"LOGG - se sumo 1 a {lista[0]} en dic inicial")
                else:
                    dic_p_inicial[lista[0]] = 1
                    # print(f"LOGG - se creo {lista[0]} en dic inicial")

                # Armo los dos diccionarios restantes
                for i in range(len(lista)):
                    # print(f"LOGG - entro al for de la lista")

                    if i + 1 < len(lista):
                        if lista[i] in dic_p_prox.keys():
                            if lista[i + 1] in dic_p_prox[lista[i]].keys():
                                dic_p_prox[lista[i]][lista[i + 1]] += 1
                                # print(f"LOGG -se sumo uno a {lista[i + 1]} en {lista[i]} dic prox")
                            else:
                                dic_p_prox[lista[i]][lista[i + 1]] = 1
                                # print(f"LOGG - se guardo {lista[i+1]} en {lista[i]} dic prox")
                        else:
                            dic_p_prox[lista[i]] = {lista[i + 1]: 1}
                            # print(f"LOGG - se guardo [{lista[i + 1]}  {lista[i]}] en dic prox")

                    else:
                        if lista[i] in dic_p_final.keys():
                            dic_p_final[lista[i]] += 1
                        else:
                            dic_p_final[lista[i]] = 1

        # para chequear lo que me esta armando
        with open('primeras.txt', 'w', encoding='utf-8') as f:
            for clave in dic_p_inicial.keys():
                f.write(clave + ':' + str(dic_p_inicial[clave]) + '\n')

        with open('proxima.txt', 'w', encoding='utf-8') as f:
            for clave in dic_p_prox.keys():
                f.write(f"{clave}:\t{dic_p_prox[clave]}\n")

        usuarios_printable = ''

        for idx in range(len(usuarios)):
            usuarios_printable += usuarios[idx] + ' - '

        print(f"\nGenerando tweet a partir de : {usuarios_printable}...\n")

        # Solo para que genere intriga
        time.sleep(1)

        # Aca empieza el chiste de la función
        primer_palabra = random_choice(dic_p_inicial)
        tweet_generado += primer_palabra
        proxima_palabra = random_choice(dic_p_prox[primer_palabra])
        # print(f"DEBUGG - Proxima palabra : {proxima_palabra}")

        tweet_generado += ' ' + proxima_palabra

        while len(tweet_generado) < longitud_tw:
            # print('entro al while..')
            if proxima_palabra in dic_p_prox.keys():
                proxima_palabra = random_choice(dic_p_prox[proxima_palabra])
                tweet_generado += ' ' + proxima_palabra
            else:
                break

        # No era necesario, pero a veces terminaba sin nada
        tweet_generado += '.'
        print(tweet_generado)
        guardar = input('\nDesea guardar el tweet como favorito? [s/n] ')

        if guardar == 's':
            with open('favoritos.csv', 'a', encoding='utf-8') as f:
                # favoritos_csv = csv.writer(f)
                f.write(hora_actual + ',' + tweet_generado + '\n')
            print(f"\nTweet guardado con éxito.!")
        elif guardar == 'n':
            print(f"\nHasta luego..")
        else:
            raise Exception

    except IndexError:
        print(f"[ATENCIÓN]El usuario ingresado no se encuentra en la lista...")
    except:
        print(f"[ATENCIÓN]Entrada invalida")


# ejecucion
try:
    if sys.argv[1] == 'trending':
        try:
            if int(sys.argv[2]) < 0:
                raise Exception
            mostrar_trending(int(sys.argv[2]))
        except IndexError:
            print(f"[ATENCIÓN]Para utilizar la función trending es obligatorio indicar la cantidad de hashtags")
        except ValueError:
            print(f"[ATENCIÓN]Se debe ingresar un numero entero.")
        except:
            print(f"[ATENCIÓN]A que jugas? El numero entero ingresado debe ser positivo u.u ")

    elif sys.argv[1] == 'generar':
        lista_usuarios = []
        for i in range(2, len(sys.argv)):
            lista_usuarios.append(sys.argv[i])

        generar_tweet(lista_usuarios)

    elif sys.argv[1] == 'favoritos':
        try:
            if len(sys.argv) == 2:
                mostrar_favoritos(0)
            elif int(sys.argv[2]) < 0:
                raise Exception
            else:
                mostrar_favoritos(int(sys.argv[2]))
        # except IndexError:
        #     print(f"Para utilizar la función favoritos es obligatorio indicar la cantidad de hashtags")
        except ValueError:
            print(f"[ATENCIÓN]Se debe ingresar un numero entero.")
        except:
            print(f"[ATENCIÓN]A que jugas? El numero entero ingresado debe ser positivo u.u ")

    else:
        raise Exception
except IndexError:
    print(f"\n[ATENCIÓN]")
    print(f"\nDebe introducir alguna de las siguientes funciones: \n"
          f"\t* trending <cantidad de hashtags>\n"
          f"\t* generar <usuario1> <usuarioN> - De no ingresar usuario se genera tweet en base a toda la db\n"
          f"\t* favoritos <cantidad de tweets>\n")


# generar_tweet(['_ErnestoSabato', 'erescurioso'])



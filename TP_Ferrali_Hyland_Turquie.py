#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 02:16:22 2025

@author: giuliferrali
"""

import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import numpy as np
from tabulate import tabulate

def lista_cero():
    return [0, 0]
# Clase para representar una transacción
class Transaccion:
    def __init__(self, tipo, fecha, categoria, monto, metodo, descripcion):
        self.tipo = tipo
        self.fecha = fecha
        self.categoria = categoria
        self.monto = monto
        self.metodo = metodo
        self.descripcion = descripcion

# Clase para manejar todas las transacciones
class RegistroGastos:
    def __init__(self):
        self.transacciones = []

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)

    def modificar_transaccion(self, indice, nueva_transaccion):
        if 0 <= indice < len(self.transacciones):
            self.transacciones[indice] = nueva_transaccion

    def eliminar_transaccion(self, indice):
        if 0 <= indice < len(self.transacciones):
            self.transacciones.pop(indice)

    def resumen_por_mes(self):
        resumen = defaultdict(lista_cero)
        for t in self.transacciones:
            mes = t.fecha[:7]  # 'YYYY-MM'
            resumen[mes][0] += t.monto
            resumen[mes][1] += 1
        return {mes: (suma, suma / cantidad) for mes, (suma, cantidad) in resumen.items() if cantidad > 0}

    def max_min_gasto(self):
        gastos = [t.monto for t in self.transacciones]
        if gastos:
            return max(gastos), min(gastos)
        return None, None

# Funciones para cargar y guardar datos

def carga_datos(archivo):
    registro = RegistroGastos()
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile)
        next(lector)  # Saltear encabezado
        for row in lector:
            try:
                tipo, fecha, categoria, monto, metodo, descripcion = row
                monto = float(monto)
                registro.agregar_transaccion(Transaccion(tipo, fecha, categoria, monto, metodo, descripcion))
            except ValueError:
                print(f"Fila ignorada por error de datos: {row}")
    return registro

def actualizar_datos(archivo, registro):
    with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
        escritor = csv.writer(csvfile)
        escritor.writerow(['tipo','fecha','categoria','monto','metodo','descripcion'])
        for t in registro.transacciones:
            escritor.writerow([t.tipo, t.fecha, t.categoria, f"{t.monto:.2f}", t.metodo, t.descripcion])

# Función para cargar una transacción desde entrada usuario
def cargar_transaccion():
    tipo = "gasto" #siempre es gasto

    # Validación de fecha
    while True:
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            break
        except ValueError:
            print("Fecha inválida. Ingrese nuevamente en formato YYYY-MM-DD.")

    categoria = input("Categoría: ").strip()
    monto = float(input("Monto: "))
    metodo = input("Método: ").strip()
    descripcion = input("Descripción: ").strip()
    print("Gasto agregado con exito!")
    return Transaccion(tipo, fecha, categoria, monto, metodo, descripcion)

def editar_transaccion(transaccion_actual):
    print("Presione Enter para dejar el valor actual sin cambios.")

    while True:
        fecha = input(f"Fecha (YYYY-MM-DD) [Actual: {transaccion_actual.fecha}]: ").strip()
        if fecha == "":
            fecha = transaccion_actual.fecha
            break
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            break
        except ValueError:
            print("Fecha inválida. Debe tener el formato YYYY-MM-DD.")

    categoria = input(f"Categoría (Salud, ocio, comida, transporte, servicios, otros) [Actual: {transaccion_actual.categoria}]: ").strip()
    if categoria == "":
        categoria = transaccion_actual.categoria

    while True:
        monto_input = input(f"Monto [Actual: {transaccion_actual.monto}]: ").strip()
        if monto_input == "":
            monto = transaccion_actual.monto
            break
        try:
            monto = float(monto_input)
            break
        except ValueError:
            print("Monto inválido.")

    metodo = input(f"Método (credito, debito, transferencia, efectivo) [Actual: {transaccion_actual.metodo}]: ").strip()
    if metodo == "":
        metodo = transaccion_actual.metodo

    descripcion = input(f"Descripción [Actual: {transaccion_actual.descripcion}]: ").strip()
    if descripcion == "":
        descripcion = transaccion_actual.descripcion

    return Transaccion("gasto", fecha, categoria, monto, metodo, descripcion)


# Funciones para graficar

def grafico_torta_categoria(registro):
    categorias = defaultdict(float)
    for t in registro.transacciones:
        categorias[t.categoria] += t.monto
    if not categorias:
        print("No hay datos para graficar.")
        return
    etiquetas = list(categorias.keys())
    valores = list(categorias.values())
    plt.figure(figsize=(7,7))
    plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=['#F48FB1', '#FFCC80', '#FFF176', '#A5D6A7', '#90CAF9', '#CE93D8'] )
    plt.title("Gastos por categoría")
    plt.show()

def grafico_barras_anios(registro):
    gastos_por_anio = defaultdict(float)
    for t in registro.transacciones:
        anio = t.fecha[:4]
        gastos_por_anio[anio] += t.monto
    if not gastos_por_anio:
        print("No hay datos para graficar.")
        return
    anios = sorted(gastos_por_anio.keys())
    valores = [gastos_por_anio[anio] for anio in anios]
    
    # Definir colores para cada barra (repetir si hay más años que colores)
    colores = ['#F8BBD0', '#F48FB1', '#F06292', '#EC407A', '#E91E63']
    colores_asignados = [colores[i % len(colores)] for i in range(len(anios))]

    plt.bar(anios, valores, color=colores_asignados)
    plt.xlabel("Año")
    plt.ylabel("Gastos")
    plt.title("Gastos por año")
    plt.show()


def histograma_montos(registro):
    montos = [t.monto for t in registro.transacciones]
    if not montos:
        print("No hay datos para graficar.")
        return
    plt.hist(montos, bins=10, edgecolor='black', color = "#40E0D0")
    plt.xlabel("Monto")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de montos de gastos")
    plt.show()

def diccionario_float():
    return defaultdict(float)

def grafico_barras_categoria_anio(registro): 
    data = defaultdict(diccionario_float)

    for t in registro.transacciones:
        anio = t.fecha[:4]
        data[t.categoria][anio] += t.monto
    categorias = list(data.keys())
    anios = sorted({anio for cat in data.values() for anio in cat.keys()})
    x = np.arange(len(anios))
    width = 0.1
    plt.figure(figsize=(10,6))

    # Definir colores para las categorías (se repiten si hay más categorías que colores)
    colores = ['#F48FB1', '#FFCC80', '#FFF176', '#A5D6A7','#90CAF9', '#CE93D8', '#F8BBD0', '#F06292','#E91E63', '#80CBC4']
    colores_asignados = [colores[i % len(colores)] for i in range(len(categorias))]

    for i, categoria in enumerate(categorias):
        valores = [data[categoria].get(anio, 0) for anio in anios]
        plt.bar(x + i*width, valores, width=width, label=categoria, color=colores_asignados[i])

    plt.xlabel("Año")
    plt.ylabel("Gastos")
    plt.title("Gastos por categorías y años")
    plt.xticks(x + width*(len(categorias)-1)/2, anios)
    plt.legend()
    plt.show()


def diccionario_lista():
    return defaultdict(list) 


# Menú principal
def menu():
    archivo = "tpgastos.csv"
    registro = carga_datos(archivo)

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ingresar/ Modificar gastos")
        print("2. Analizar gastos")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                print("\n1. Agregar gasto")
                print("2. Modificar gasto")
                print("3. Eliminar gasto")
                print("4. Promedio gastos por mes (tabla)")
                print("5. Máximo y mínimo gasto")
                print("6. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    t = cargar_transaccion()
                    registro.agregar_transaccion(t)
                    actualizar_datos(archivo, registro) 
                
                
                elif subop == "2": 
                    if not registro.transacciones: 
                        print("No hay transacciones registradas.") 
                    else: 
                        nombres_meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"} 
                        años = sorted(set(datetime.strptime(t.fecha, "%Y-%m-%d").year for t in registro.transacciones)) 
                        print("Años disponibles:") 
                        for i, año in enumerate(años): 
                            print(f"{i}: {año}") 
                       
                        while True: 
                            try: 
                                i_año = int(input("Seleccione el año: ")) 
                                if 0 <= i_año < len(años): 
                                    año_seleccionado = años[i_año] 
                                    break 
                                else: 
                                    print("Opción inválida.") 
                            except ValueError: 
                                print("Ingrese un número válido.") 
                        
                        meses = sorted(set(datetime.strptime(t.fecha, "%Y-%m-%d").month  
                                           for t in registro.transacciones 
                                           if datetime.strptime(t.fecha, "%Y-%m-%d").year == año_seleccionado)) 
                        print("Meses disponibles:") 
                        for i, mes in enumerate(meses): 
                            print(f"{i}: {nombres_meses[mes]}") 
                        
                        while True: 
                            try: 
                                i_mes = int(input("Seleccione el mes: ")) 
                                if 0 <= i_mes < len(meses): 
                                    mes_seleccionado = meses[i_mes] 
                                    break 
                                else: 
                                    print("Opción inválida.") 
                            except ValueError: 
                                print("Ingrese un número válido.") 
                        
                        transacciones_filtradas = [(idx, t) for idx, t in enumerate(registro.transacciones) 
                            if datetime.strptime(t.fecha, "%Y-%m-%d").year == año_seleccionado and
                            datetime.strptime(t.fecha, "%Y-%m-%d").month == mes_seleccionado] 
                        
                        if not transacciones_filtradas: 
                            print("No hay transacciones en ese mes.") 
                        else: 
                            print("Transacciones disponibles:") 
                            for i, (idx, t) in enumerate(transacciones_filtradas): 
                                print(f"{i}: {t.tipo} | {t.fecha} | ${t.monto} | {t.categoria} | {t.descripcion}") 
                            while True: 
                                try: 
                                    i_trans = int(input("Seleccione la transacción a modificar: ")) 
                                    if 0 <= i_trans < len(transacciones_filtradas): 
                                        indice_original = transacciones_filtradas[i_trans][0] 
                                        nuevo = editar_transaccion(registro.transacciones[indice_original]) 
                                        registro.modificar_transaccion(indice_original, nuevo) 
                                        actualizar_datos(archivo, registro) 
                                        print("Transacción modificada exitosamente.") 
                                        break 
                                    else: 
                                        print("Opción inválida.") 
                                except ValueError: 
                                        print("Ingrese un número válido.")

     

                
                elif subop == "3":  

                    trans_por_anio_mes = defaultdict(diccionario_lista)
                    for i, t in enumerate(registro.transacciones): 
                        try: 
                            anio, mes, _ = t.fecha.split('-') 
                            mes = mes.zfill(2)
                            trans_por_anio_mes[anio][mes].append((i, t))
                        except: 
                            continue 
                   
                    anios = sorted(trans_por_anio_mes.keys())
                    if not anios: 
                        print("No hay gastos registrados.") 
                        continue
    
                    print("\nAños disponibles:") 
                    for idx, anio in enumerate(anios, 0): 
                        print(f"{idx+1}. {anio}") 
                    try: 
                        anio_opcion = int(input("Seleccione el año: "))  
                        if 1 <= anio_opcion <= len(anios): 
                            anio_seleccionado = anios[anio_opcion - 1]  
                        else: 
                            print("Selección inválida.") 
                            continue
                    except (ValueError, IndexError): 
                        print("Selección inválida.") 
                        continue  
                    
                    nombres_meses = {
    '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
    '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
    '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'}
                    meses_dict = trans_por_anio_mes[anio_seleccionado] 
                    meses_disponibles = sorted(meses_dict.keys())
                    if not meses_disponibles: 
                        print("No hay meses con gastos en ese año.") 
                        continue
                    print("Meses disponibles:") 
                    for idx, mes in enumerate(meses_disponibles, 1): 
                        print(f"{idx}. {nombres_meses.get(mes, mes)}")
                    
                    try: 
                        mes_opcion = int(input("Seleccione el mes: ")) 
                        if 1 <= mes_opcion <= len(meses_disponibles): 
                            mes_seleccionado = meses_disponibles[mes_opcion - 1] 
                        else: 
                            print("Selección inválida.") 
                            continue 
                    except (ValueError, IndexError): 
                        print("Selección inválida.") 
                        continue 
                    
                    
                    transacciones_mes = meses_dict[mes_seleccionado] 
                    if not transacciones_mes: 
                        print("No hay transacciones para ese mes.") 
                        continue 
                    print("Transacciones disponibles:") 
                    for idx, (i_t, t) in enumerate(transacciones_mes, 1): 
                        print(f"{idx}. {t.tipo} | {t.fecha} | ${t.monto:.2f} | {t.categoria} | {t.descripcion}") 
                    try: 
                        trans_opcion = int(input("Seleccione la transacción a eliminar: ")) 
                        if 1 <= trans_opcion <= len(transacciones_mes): 
                            indice_eliminar = transacciones_mes[trans_opcion - 1][0] 
                            confirm = input(f"¿Está seguro que desea eliminar la transacción {trans_opcion}? (s/n): ").lower() 
                            if confirm == 's': 
                                registro.eliminar_transaccion(indice_eliminar) 
                                actualizar_datos(archivo, registro) 
                                print("Transacción eliminada exitosamente.") 
                            else: 
                                print("Eliminación cancelada.") 
                        else: 
                            print("Selección inválida.") 
                    except (ValueError, IndexError): 
                        print("Selección inválida.")

                elif subop == "4": 
                    nombres_meses = {
    "01": "Enero",
    "02": "Febrero",
    "03": "Marzo",
    "04": "Abril",
    "05": "Mayo",
    "06": "Junio",
    "07": "Julio",
    "08": "Agosto",
    "09": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
    }
                    resumen = registro.resumen_por_mes() 
                    if resumen: 
                        tabla = [] 
                        for mes_str, (suma, prom) in sorted(resumen.items()): 
                            partes = mes_str.split("-") 
                            año = partes[0] 
                            mes_num = partes[1] if len(partes) > 1 else "01" 
                            mes_nombre = nombres_meses.get(mes_num, mes_num) 
                            mes_con_nombre = f"{mes_nombre} {año}" 
                            tabla.append([mes_con_nombre, f"${suma:.2f}", f"${prom:.2f}"]) 
                            print(tabulate(tabla, headers=["Mes", "Total", "Promedio"], tablefmt="fancy_grid")) 
                    else: 
                        print("No hay datos para mostrar.")

                elif subop == "5":
                    maximo, minimo = registro.max_min_gasto()
                    if maximo is not None:
                        print(f"Máximo gasto: ${maximo:.2f}")
                        print(f"Mínimo gasto: ${minimo:.2f}")
                    else:
                        print("No hay gastos registrados.")

                elif subop == "6":
                    break

                else:
                    print("Opción inválida, intente nuevamente.")

        elif opcion == "2":
            while True:
                print("\n1. Gráfico torta (gastos por categoría)")
                print("2. Gráfico barras (gastos por año)")
                print("3. Histogramas por montos (gastos por montos)")
                print("4. Gráfico barras por categorías y años")
                print("5. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    grafico_torta_categoria(registro)
                elif subop == "2":
                    grafico_barras_anios(registro)
                elif subop == "3":
                    histograma_montos(registro)
                elif subop == "4":
                    grafico_barras_categoria_anio(registro)
                elif subop == "5":
                    break
                else:
                    print("Opción inválida, intente nuevamente.")

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    menu()

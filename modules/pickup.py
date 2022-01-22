#!/usr/bin/python3
"""Hora de partida menos 3:30 para pickup"""

def hora_pickup(hora, fecha):
    hora_vuelo = str(hora).split(":")
    h = int(hora_vuelo[0])
    m = int(hora_vuelo[1])
    h_flag = 0
    D_flag = 0

    # check for minute edge case
    if m >= 30:
        m = m - 30
    else:
        m = m + 30
        h_flag = 1

    # check for hour edge case
    if h < 3:
        if h_flag == 1:
            h = h + 24 - 4
        else:
            h = h + 24 - 3
        D_flag = 1
    elif h == 3:
        if h_flag == 1:
            h = 23
            D_flag = 1
        else:
            h = 0
    else:
        if h_flag == 1:
            h = h - 4
        else:
            h = h - 3

    # hora transformada exitosamente, pasar a string
    h_str = ""
    m_str = ""
    if h <= 9:
        h_str = "0" + str(h)
    else:
        h_str = str(h)
    if m <= 9:
        m_str = "0" + str(m)
    else:
        m_str = str(m)

    # hora del pickup lista
    pickup = h_str + ":" + m_str

    # checkear fecha edge case
    if D_flag == 1:
        fecha = str(fecha).split("-")
        dia = int(fecha[2])
        mes = int(fecha[1])
        año = int(fecha[0])
        M_flag = 0
        if dia == 1:
            mes = mes - 1
            M_flag = 1
            if M_flag == 1:
                if mes == 0:
                    mes = 12
                    año = año - 1
            if (mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12):
                dia = 31
            elif mes == 2:
                dia = 28
            else:
                dia = 30
        else:
            dia = dia - 1
        pickup = pickup + " (" + str(dia) + "/" + str(mes) + "/" + str(año) + ")"

    return (pickup)

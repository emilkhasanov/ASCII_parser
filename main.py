#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import time
import socket
import argparse

class serial_client():  # класс для использования последовательного порта

    def __init__(self):
        self.ports = []
        self.port = ''

    def ports_listener(self):  # функция для поиска подключенного оборудования (если подключено только одно оборудование
        print(list(serial.tools.list_ports.comports()))

        self.ports = serial.tools.list_ports.comports()
        print(self.ports)
        if type(self.ports) is list:
            self.port = self.ports[0].device
        else:
            self.port = self.ports.device
        return str(self.port)

    def command_worker(self, port_input, command_input, baudrate_input):  # отправка команды и получение ответа
        response = ''
        ser = serial.Serial(port_input, baudrate_input, 8, 'N', 1, timeout=1)  # открытие порта
        ser.write(command_input.encode(encoding='utf-8'))  # отправка команды
        delay = time.time() + 3  # назначение максимального времени прослушивания ответа
        while 1 == 1:
            if time.time() < delay:
                try:
                    line = ser.readline()
                    response = line.decode("Ascii")  # декодирование полученного ответа
                    if str(response[0]) == str(
                            command_input[-1]):  # проверка ответа на соответствие ожидаемому типу ответа
                        return response
                except:
                    pass
            else:
                print('response is None')
                return response  # возврат пустого ответа в случае не получения данных в течение тайм-аута


class tcp_client():  # класс работы с тср

    def __init__(self):
        self.sock = ''

    def tcp_worker(self, command_input, host_name, port):  # отправка команды и получение ответа
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5000)
        self.sock.connect((str(host_name), int(port)))
        self.sock.sendall(command_input.encode(encoding='utf-8'))  # отправка команды
        response_tcp = self.sock.recv(1024).decode("Ascii")  # получение ответа
        self.sock.close()
        print(response_tcp)
        if str(response_tcp[0]) == str(command_input[-1]):  # проверка ответа на соответствие ожидаемому типу ответа
            return response_tcp
        else:
            response_tcp = ''
            return response_tcp  # возврат пустого ответа в случае не получения данных в течение тайм-аута


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--command_list", help="command_list", type=list, default=['GET_A', 'GET_B', 'GET_C'], required=False)
    parser.add_argument("--port", help="com port", type=str, default='Com1', required=False)
    parser.add_argument("--baudrate", help="baudrate", type=int, default=9600, required=False)
    parser.add_argument("--host_name", help="host name", type=str, default='youtube.com')
    parser.add_argument("--tcp_port", help="tcp port", type=int, default=80, required=False)
    parser.add_argument("--client_choise", help="client_choice tcp or serial", type=str, default='tcp', required=False)

    # command_list = ['GET_A', 'GET_B', 'GET_C']  # список команд для отправки
    # port = 'Com1'  # '' пустое значение для авто поиска или название порта в явном виде, например 'Com1'
    # baudrate = 9600  # скорость для последовательного порта
    # host_name = 'youtube.com'  # адрес хоста для тср
    # tcp_port = 80  # порт для тср
    #
    # client_choise = 'tcp'  # serial or tcp

    args = parser.parse_args()
    command_list  = args.command_list
    port = str(args.port)
    baudrate = int(args.baudrate)
    host_name = str(args.host_name)
    tcp_port = int(args.tcp_port)
    client_choise = str(args.client_choise)

    if client_choise == 'serial':  # в случае выбора последовательного порта
        client = serial_client()  # запуск клиента последовательного порта
        if port == '':
            port = client.ports_listener()  # получение ком порта
        for i in range(0, len(command_list)):  # цикл отправки команд по тср
            response = 'start'  # начальное значение ответа для дальнейшего сравнения его изменения
            response = client.command_worker(port, command_list[i] + '\r\n', baudrate)  # отправка команды
            while response == 'start':  # ожидание изменения ответа
                pass
            print('response', response)  # вывод  значения ответа
    else:  # в случае выбора тср
        client = tcp_client()  # запуск тср клиента
        for i in range(0, len(command_list)):  # цикл отправки команд
            response = 'start'  # начальное значение ответа для дальнейшего сравнения его изменения
            response = client.tcp_worker(command_list[i] + '\r\n', host_name, tcp_port)  # отправка команды
            while response == 'start':  # ожидание изменения ответа
                pass
            print('response', response)  # вывод  значения ответа

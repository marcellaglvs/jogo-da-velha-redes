import socket
import time
import sys


def jogar_tcp(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 50000))

    id_msg = client.recv(1024).decode()
    print(f"Conectado via TCP! Seu simbolo eh: {id_msg.split(':')[1]}")

    while True:
        msg = client.recv(4096).decode()
        status, conteudo = msg.split(":", 1)

        if status == "VEZ":
            print(conteudo)
            jogada = input("Sua vez! Escolha uma posicao (0-8): ")

            inicio = time.time()
            client.sendall(jogada.encode())
            fim = time.time()

            latencia = (fim - inicio) * 1000
            print(f"> Latencia da jogada (RTT): {latencia:.2f} ms")

        elif status == "AGUARDE":
            print(conteudo)
            print("Aguardando a jogada do oponente...")

        elif status == "INVALIDO":
            print(f"\n[Aviso] {conteudo}")

        elif status == "FIM":
            print("\n=== FIM DE JOGO ===")
            print(conteudo)
            break

    client.close()


def jogar_udp(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (ip, 50000)

    client.sendto(b"JOIN", server_addr)

    id_msg, _ = client.recvfrom(1024)
    print(f"Conectado via UDP! Seu simbolo eh: {id_msg.decode().split(':')[1]}")

    while True:
        data, _ = client.recvfrom(4096)
        status, conteudo = data.decode().split(":", 1)

        if status == "VEZ":
            print(conteudo)
            jogada = input("Sua vez! Escolha uma posicao (0-8): ")

            inicio = time.time()
            client.sendto(jogada.encode(), server_addr)
            fim = time.time()

            latencia = (fim - inicio) * 1000
            print(f"> Latencia da jogada (RTT): {latencia:.2f} ms")

        elif status == "AGUARDE":
            print(conteudo)
            print("Aguardando a jogada do oponente...")

        elif status == "INVALIDO":
            print(f"\n[Aviso] {conteudo}")

        elif status == "FIM":
            print("\n=== FIM DE JOGO ===")
            print(conteudo)
            break

    client.close()


if __name__ == "__main__":
    print("=== CLIENTE DE JOGO DA VELHA ===")

    ip_servidor = input("Digite o IP do servidor (ex: 127.0.0.1): ")
    escolha = input("Escolha o protocolo (1 para TCP, 2 para UDP): ")

    if escolha == "1":
        jogar_tcp(ip_servidor)
    else:
        jogar_udp(ip_servidor)
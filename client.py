import socket
import time
import sys


def jogar_tcp(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 50000))

    id_msg = client.recv(1024).decode()
    print(f"Conectado via TCP! Seu simbolo eh: {id_msg.split(':')[1]}")

    # Variáveis de controle para o RTT funcionar em qualquer resposta
    esperando_rtt = False
    inicio = 0.0

    while True:
        # O recv fica bloqueado aqui esperando o servidor mandar algo
        msg = client.recv(4096).decode()
        
        # Se uma jogada foi enviada antes, calcula o tempo ASSIM que o pacote chega
        if esperando_rtt:
            fim = time.perf_counter()
            latencia = (fim - inicio) * 1000
            print(f"> Latencia da jogada (RTT): {latencia:.2f} ms")
            esperando_rtt = False  # Reseta para a próxima rodada

        status, conteudo = msg.split(":", 1)

        if status == "VEZ":
            print(conteudo)
            jogada = input("Sua vez! Escolha uma posicao (1-9): ")

            # Ativa o cronômetro imediatamente antes do envio
            inicio = time.perf_counter()
            esperando_rtt = True
            
            client.sendall(jogada.encode())

        elif status == "AGUARDE":
            print(conteudo)
            print("Aguardando a jogada do oponente...")

        elif status == "INVALIDO":
            print(f"\n[Aviso] {conteudo}")
            time.sleep(0.1)
            # Se a jogada foi inválida, o servidor responde na hora, então também precisamos resetar
            esperando_rtt = False 

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

    esperando_rtt = False
    inicio = 0.0

    while True:
        data, _ = client.recvfrom(4096)
        
        # Se uma jogada foi enviada, calcula o RTT assim que o datagrama de resposta chega
        if esperando_rtt:
            fim = time.perf_counter()
            latencia = (fim - inicio) * 1000
            print(f"> Latencia da jogada (RTT): {latencia:.2f} ms")
            esperando_rtt = False  # Reseta para a próxima jogada

        status, conteudo = data.decode().split(":", 1)

        if status == "VEZ":
            print(conteudo)
            jogada = input("Sua vez! Escolha uma posicao (1-9): ")

            inicio = time.perf_counter()
            esperando_rtt = True

            client.sendto(jogada.encode(), server_addr)

        elif status == "AGUARDE":
            print(conteudo)
            print("Aguardando a jogada do oponente...")

        elif status == "INVALIDO":
            print(f"\n[Aviso] {conteudo}")
            time.sleep(0.1)
            # Se a jogada foi inválida (ex: posição ocupada), o servidor responde na hora
            esperando_rtt = False

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
import socket
import sys

# Configurações de rede
HOST = '0.0.0.0'  # Escuta em todas as interfaces locais
PORT = 50000

def inicializar_tabuleiro():
    return [" " for _ in range(9)]

def exibir_tabuleiro(b):
    return f"\n {b[0]} | {b[1]} | {b[2]} \n---|---|---\n {b[3]} | {b[4]} | {b[5]} \n---|---|---\n {b[6]} | {b[7]} | {b[8]} \n"

def verificar_vitoria(b, p):
    vitorias = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(b[i] == b[j] == b[k] == p for i, j, k in vitorias)

def rodar_servidor_tcp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("\n[TCP] Servidor aguardando jogadores na porta", PORT)

    conn1, addr1 = server.accept()
    print(f"Jogador 1 (X) conectado de {addr1}")
    conn1.sendall(b"VOCE:X")

    conn2, addr2 = server.accept()
    print(f"Jogador 2 (O) conectado de {addr2}")
    conn2.sendall(b"VOCE:O")

    tabuleiro = inicializar_tabuleiro()
    jogadores = [(conn1, 'X', conn2), (conn2, 'O', conn1)]
    turno = 0

    while True:
        atual_conn, simbolo, outro_conn = jogadores[turno % 2]
        estado = exibir_tabuleiro(tabuleiro)
        atual_conn.sendall(f"VEZ:{estado}".encode())
        outro_conn.sendall(f"AGUARDE:{estado}".encode())

        try:
            dados = atual_conn.recv(1024).decode().strip()
            
            # Valida se é um número e se está entre 1 e 9
            if dados.isdigit() and 1 <= int(dados) <= 9:
                jogada = int(dados) - 1 # Converte para o índice do Python (0-8)
                
                if tabuleiro[jogada] == " ":
                    tabuleiro[jogada] = simbolo
                    
                    if verificar_vitoria(tabuleiro, simbolo):
                        final = exibir_tabuleiro(tabuleiro)
                        atual_conn.sendall(f"FIM:Voce venceu!{final}".encode())
                        outro_conn.sendall(f"FIM:Voce perdeu!{final}".encode())
                        break
                    elif " " not in tabuleiro:
                        final = exibir_tabuleiro(tabuleiro)
                        atual_conn.sendall(f"FIM:Empate!{final}".encode())
                        outro_conn.sendall(f"FIM:Empate!{final}".encode())
                        break
                    
                    turno += 1
                else:
                    atual_conn.sendall(b"INVALIDO:Posicao ocupada!")
            else:
                atual_conn.sendall(b"INVALIDO:Escolha um numero de 1 a 9!")
                
        except Exception:
            print("Conexao perdida.")
            break

    conn1.close()
    conn2.close()
    server.close()

def rodar_servidor_udp():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"\n[UDP] Servidor aguardando datagramas na porta {PORT}")

    clientes = []
    
    while len(clientes) < 2:
        data, addr = server.recvfrom(1024)
        if data.decode() == "JOIN" and addr not in [c[0] for c in clientes]:
            simbolo = 'X' if len(clientes) == 0 else 'O'
            clientes.append((addr, simbolo))
            server.sendto(f"VOCE:{simbolo}".encode(), addr)
            print(f"Jogador {simbolo} registrado do endereco {addr}")

    addr1, sim1 = clientes[0]
    addr2, sim2 = clientes[1]
    tabuleiro = inicializar_tabuleiro()
    turno = 0

    while True:
        atual_addr, simbolo = clientes[turno % 2]
        outro_addr = addr2 if turno % 2 == 0 else addr1

        estado = exibir_tabuleiro(tabuleiro)
        server.sendto(f"VEZ:{estado}".encode(), atual_addr)
        server.sendto(f"AGUARDE:{estado}".encode(), outro_addr)

        try:
            data, addr = server.recvfrom(1024)
            if addr == atual_addr:
                dados = data.decode().strip()
                
                # Valida se é um número e se está entre 1 e 9
                if dados.isdigit() and 1 <= int(dados) <= 9:
                    jogada = int(dados) - 1 # Converte para o índice do Python (0-8)
                    
                    if tabuleiro[jogada] == " ":
                        tabuleiro[jogada] = simbolo
                        
                        if verificar_vitoria(tabuleiro, simbolo):
                            final = exibir_tabuleiro(tabuleiro)
                            server.sendto(f"FIM:Voce venceu!{final}".encode(), atual_addr)
                            server.sendto(f"FIM:Voce perdeu!{final}".encode(), outro_addr)
                            break
                        elif " " not in tabuleiro:
                            final = exibir_tabuleiro(tabuleiro)
                            server.sendto(f"FIM:Empate!{final}".encode(), atual_addr)
                            server.sendto(f"FIM:Empate!{final}".encode(), outro_addr)
                            break
                        
                        turno += 1
                    else:
                        server.sendto(b"INVALIDO:Posicao ocupada!", atual_addr)
                else:
                    server.sendto(b"INVALIDO:Escolha um numero de 1 a 9!", atual_addr)
        except Exception:
            break

    server.close()

if __name__ == "__main__":
    print("=== SERVIDOR DE JOGO DA VELHA ===")
    escolha = input("Escolha o protocolo (1 para TCP, 2 para UDP): ")
    if escolha == '1':
        rodar_servidor_tcp()
    else:
        rodar_servidor_udp()


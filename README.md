# 🎮 Jogo da Velha: Demonstração de TCP vs UDP e Latência

## 📝 Descrição do Projeto

Este projeto consiste em uma aplicação de Jogo da Velha distribuída em rede, desenvolvida para a disciplina de Redes de Computadores. A aplicação utiliza a arquitetura cliente-servidor para permitir que dois jogadores disputem uma partida em tempo real através do prompt de comando.

O objetivo principal, além do entretenimento, é demonstrar de forma prática e visual conceitos fundamentais da **Camada de Transporte** e da **Camada de Aplicação**, tais como:

* **Comunicação Cliente-Servidor:** Um servidor centralizado coordena o estado do tabuleiro e os turnos, enquanto os clientes enviam as jogadas.
* **TCP vs UDP:** A aplicação permite alternar entre o protocolo orientado à conexão (TCP) e o protocolo não orientado à conexão (UDP), evidenciando a tolerância a falhas e o comportamento de ambos.
* **Medição de Latência:** O cliente calcula o *Round-Trip Time* (RTT) em milissegundos a cada jogada realizada, mostrando o impacto da infraestrutura de rede na experiência do usuário.
* **Portas e Endereçamento:** Utilização de portas lógicas (porta padrão `50000`) e endereçamento IP para direcionamento de sockets.

---

## 💻 Pré-requisitos e Ambiente de Execução

| Requisito | Detalhes |
| :--- | :--- |
| **Sistema Operacional** | Microsoft Windows |
| **Ambiente de Execução** | Apenas um computador físico, simulando a rede através de três janelas independentes do Prompt de Comando (CMD) |
| **Linguagem** | Python 3.x (utilizando as bibliotecas nativas `socket`, `sys` e `time`, sem necessidade de instalações externas via pip) |
| **Ferramenta de Simulação** | Software open-source **Clumsy** (necessário para a demonstração prática de latência e perda de pacotes) |

---

## 🚀 Instruções de Instalação e Execução

Como o teste ocorre localmente em uma única máquina através da interface de *loopback* (`127.0.0.1`), a latência padrão exibida no terminal seria próxima de `0ms`. Para simular o comportamento de uma rede real de longa distância (com atrasos e perda de pacotes) e cumprir os objetivos acadêmicos do trabalho, o software open-source **Clumsy** será executado em paralelo com o jogo.

Siga o passo a passo integrado abaixo para preparar o ambiente e iniciar a partida:

### 1. Preparando o Ambiente
* Certifique-se de ter os arquivos `server.py` e `client.py` na mesma pasta.
* Baixe e extraia o executável do [Clumsy](https://jagt.github.io/clumsy/download) (ferramenta leve de simulação de rede para Windows).

### 2. Ativando o Simulador de Rede (Clumsy)
Configure o atraso artificial na sua rede:
1. Abra o **Clumsy** como Administrador.
2. No campo **Filter**, digite exatamente: `tcp or udp`
3. Marque a caixa **Lag** e configure o tempo para `50` (adiciona 50ms de atraso, resultando em um RTT de ~100ms).
4. Marque a caixa **Drop** e configure a porcentagem para `5` (simula 5% de perda de pacotes).
5. Clique no botão **Start**. O simulador já está interceptando a rede local.

### 3. Executando o Servidor (Janela 1)
Abra o Prompt de Comando (CMD), navegue até a pasta dos arquivos do projeto e inicie o servidor:
```cmd
python server.py

```

O programa solicitará o protocolo de transporte desejado:

* Digite `1` para testar o comportamento em **TCP**
* Digite `2` para testar o comportamento em **UDP**

O servidor entrará em modo de escuta na porta `50000`.

### 4. Executando o Jogador 1 (Janela 2)

Abra uma segunda janela independente do CMD e execute o script do cliente:

```cmd
python client.py

```

* **IP do Servidor:** Digite `127.0.0.1`
* **Protocolo:** Escolha o mesmo protocolo selecionado no servidor (`1` ou `2`).
* O terminal informará que você é o **Jogador X** e solicitará que aguarde o oponente.

### 5. Executando o Jogador 2 (Janela 3)

Abra uma terceira janela do CMD e repita o comando do cliente:

```cmd
python client.py

```

* **IP do Servidor:** Digite `127.0.0.1`
* **Protocolo:** Escolha o mesmo protocolo selecionado no servidor.

O jogo iniciará imediatamente nas telas dos dois jogadores. Durante as jogadas, observe no terminal o cálculo do RTT refletindo as alterações aplicadas pelo Clumsy.

### 6. Como Jogar (Mapeamento do Tabuleiro)

Para realizar as jogadas, digite no terminal ativo o número de **1 a 9** correspondente à casa desejada, baseando-se no padrão visual do teclado numérico:

```text
 1 | 2 | 3 
---+---+---
 4 | 5 | 6 
---+---+---
 7 | 8 | 9 
```

> 💡 **Nota:** *O servidor valida as jogadas em tempo real. Se você digitar uma posição já ocupada, caracteres de texto ou números fora do limite (1-9), o servidor enviará um alerta de comando inválido e solicitará um novo input, garantindo a estabilidade do sistema contra falhas de digitação.*

### 7. Finalização

Ao encerrar os testes e fechar as janelas do jogo, vá até a interface do **Clumsy** e clique em **Stop** para que a rede local do seu computador volte ao funcionamento normal.

---

## 📊 O que observar durante os testes? (Análise de Comportamento)

Ao executar as partidas com o **Clumsy** ativado, preste atenção no comportamento dos terminais para notar a diferença crucial entre os protocolos:

### 🌐 Cenário 1: Jogo em modo TCP (Conexão Confiável)

* **Latência (RTT):** O valor exibido no terminal vai saltar para **mais de 100 ms** (50ms de ida + 50ms de volta, além do tempo de processamento).
* **Comportamento:** O jogo funcionará perfeitamente e nenhuma jogada será perdida. Caso o Clumsy intercepte e descarte um pacote (os 5% de perda), o protocolo TCP perceberá a ausência da confirmação (*ACK*), segurará o fluxo por uma fração de segundo e **retransmitirá o pacote automaticamente**. Na tela, você sentirá apenas uma leve resposta "pesada" ou um pequeno atraso na atualização do tabuleiro, mas os dados chegarão intactos.

> ℹ️ **Nota (Multiplexagem):** *Repare no terminal do servidor ao iniciar o TCP. Mesmo rodando os dois clientes no mesmo IP (`127.0.0.1`), o sistema operacional atribui uma **Porta de Origem** aleatória diferente para cada janela do cliente. O servidor diferencia os dois jogadores através do par `IP:Porta`, demonstrando o conceito prático de multiplexagem da Camada de Transporte.*

### ⚡ Cenário 2: Jogo em modo UDP (Não Orientado à Conexão)

* **Latência (RTT):** Nas jogadas bem-sucedidas, a latência também ficará na casa dos **100 ms**.
* **Comportamento:** O impacto da rede aqui é imediato e visual. Quando a perda de 5% atingir o pacote de uma jogada, **o dado sumirá no limbo**. Como o UDP não possui mecanismos nativos de confirmação ou retransmissão, o terminal do jogador achará que enviou a jogada, mas o servidor nunca a receberá. O jogo ficará travado esperando uma ação que nunca vai chegar, demonstrando na prática a fragilidade de um protocolo não confiável em redes instáveis.

> ⚠️ **Nota (Responsabilidade da Aplicação):** *O travamento do jogo no modo UDP evidencia que, ao escolher este protocolo, a garantia de entrega se torna **responsabilidade total da Camada de Aplicação** (através de timeouts ou retransmissões manuais no código). Como nossa aplicação foi projetada de forma simples para fins didáticos, a perda do pacote gera um estado de deadlock (espera infinita).*

---

## 🎥 Demonstração em Vídeo

[Clique aqui para assistir à demonstração do projeto](https://github.com/user-attachments/assets/361ad12f-4267-483a-aaec-725063e63df6)



---

## 👥 Autoria e Contribuições

Este projeto foi desenvolvido como parte da avaliação prática da disciplina de Redes de Computadores. Todos os integrantes do grupo participaram ativamente de todas as etapas de planejamento, modelagem e codificação do sistema. A divisão abaixo destaca o foco principal de liderança no desenvolvimento e a estratégia de contribuição e upload no GitHub:

* **Marcella Martins Gonçalves**
* *Contribuição:* Desenvolvimento da lógica central do Jogo da Velha, tratamento de estados na camada de aplicação, arquitetura do socket do lado do servidor e implementação do arquivo `server.py`.


* **José Mauro Pinto**
* *Contribuição:* Implementação da comunicação de rede (Sockets TCP e UDP), lógica de concorrência/turnos na camada de transporte, cálculo de latência (RTT) e implementação do arquivo `client.py`.


* **Marcos Junior Rodrigues Marcena**
* *Contribuição:* Engenharia de testes e ajustes nos códigos do sistema, simulação e análise de perdas e atrasos de pacotes na rede através do Clumsy, validação experimental dos protocolos, desenvolvimento do arquivo de documentação técnica `README.md` e gravação do material em vídeo.



```

```

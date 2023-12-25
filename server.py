import socket
import threading
import dataSet
from dataSet import options, legumes, frutas
import signal
import sys

# Função para gerar recibo após a compra ser finalizada
def gerarRecibo(completeUserName, carrinho, valores, totalCompra, valorUnitarioP):
    # Criação do recibo com o nome do cliente
    recibo = "===== Cupom Fiscal =====\n"
    recibo += f"Cliente: {completeUserName}\n\n"
    recibo += "{:<15} {:<20} {:<25} {:<20}\n".format("Item", "Quantidade", "Valor Unitário", "Total")

    # Preenchimento do recibo com os itens no carrinho do cliente 
    for item, totalItems in carrinho.items():
        valorUnitario = valorUnitarioP[len(carrinho) - 1]
        totalItem = valorUnitario * int(totalItems)
        recibo += "{:<15} {:<20} R${:<25} R${:<20.2f}\n".format(item, totalItems, valorUnitario, totalItem)

    recibo += "\nTotal da compra: R${:.2f}\n".format(totalCompra)
    recibo += "=======================\n"

    # Grava o recibo em um arquivo txt na pasta de recibos
    with open(f"recibos/recibo_{completeUserName}.txt", "w") as arquivo:
        arquivo.write(recibo)

    print("Recibo do cliente '{}' gerado com sucesso. Confira o arquivo recibo_{}.txt".format(completeUserName, completeUserName))

# Função para visualizar o carrinho tanto do lado do servidor quanto do lado do cliente caso solicitado pelo mesmo
def visualizarCarrinho(carrinho, valores, escolha, completeUserName):
    resul = ""
    precoQuant = 0
    resul += "========================================="
    resul += f"\nCliente: {completeUserName}"
    resul += f"\n{escolha.ljust(15)} Quant           Preço\n"
    for fruta, totalItems in carrinho.items():
        resul += f"{fruta.ljust(15)} {str(totalItems).ljust(15)} R${'{:.2f}'.format(float(valores[precoQuant]))}\n"
        precoQuant += 1
    resul += ("Total: R${:.2f}".format(sum(valores)))
    resul += "\n========================================="
    return resul

# Função responsavel por dar as opções de escolha para o cliente
def darOpcoes(clientSocket, completeUserName):
    global valorCaixa
    carrinho = {}
    valores = []
    valorUnitario = []

    # Função para finalizar as compras do cliente
    def finalizarCompras(carrinho, valores, completeUserName, clientSocket):
        clientSocket.sendall(visualizarCarrinho(carrinho, valores, escolhaUser, completeUserName).encode('utf-8'))
        compra = clientSocket.recv(1024).decode('utf-8')

        if compra == 'confirmar':
            print("{} efetuou o pagamento!".format(completeUserName))
            dataSet.compraClientes[completeUserName] = sum(valores)
            dataSet.valorCaixa += sum(valores)
            gerarRecibo(completeUserName, carrinho, valores, sum(valores), valorUnitario)
        else:
            print("{} Cancelou a compra: ".format(completeUserName))
            dataSet.compraClientes[completeUserName] = 'Cancelado'

    # Função para montar o carrinho enquanto o cliente realiza a compra
    def montarCarrinho(escolhaUser):
        while True:
            escolhaItem = clientSocket.recv(1024).decode('utf-8')
            if escolhaUser == 'legumes':
                if escolhaItem not in legumes:
                    sendValue = False
                    clientSocket.sendall(str(sendValue).encode('utf-8'))
                    print('Item solicitado por {} não está disponível'.format(completeUserName.split()[0]))
                else:
                    sendValue = True
                    clientSocket.sendall(str(sendValue).encode('utf-8'))
                    break
            elif escolhaUser == 'frutas':
                if escolhaItem not in frutas:
                    sendValue = False
                    clientSocket.sendall(str(sendValue).encode('utf-8'))
                    print('Item solicitado por {} não está disponível'.format(completeUserName.split()[0]))
                else:
                    sendValue = True
                    clientSocket.sendall(str(sendValue).encode('utf-8'))
                    break
        quantidade = clientSocket.recv(1024).decode('utf-8')
        if escolhaUser == 'legumes':
            carrinho[escolhaItem] = quantidade
            valores.append(int(quantidade) * float(legumes[escolhaItem]))
            valorUnitario.append(float(legumes[escolhaItem]))
        elif escolhaUser == 'frutas':
            carrinho[escolhaItem] = quantidade
            valores.append(int(quantidade) * float(frutas[escolhaItem]))
            valorUnitario.append(float(frutas[escolhaItem]))
        print(visualizarCarrinho(carrinho, valores, escolhaUser, completeUserName))
        while True:
            op = clientSocket.recv(1024).decode('utf-8')
            if op.isdigit() and int(op) == 1:
                montarCarrinho(escolhaUser)
            elif op.isdigit() and int(op) == 2:
                print("{} desconectado!".format(completeUserName))
                break
            elif op.isdigit() and int(op) == 3:
                clientSocket.sendall(visualizarCarrinho(carrinho, valores, escolhaUser, completeUserName).encode('utf-8'))
                break
            elif op.isdigit() and int(op) == 4:
                finalizarCompras(carrinho, valores, completeUserName, clientSocket)
                break
        print(visualizarCarrinho(carrinho, valores, escolhaUser, completeUserName))

    clientSocket.sendall("Escolhe entre 'Legumes' ou 'Frutas': ".encode('utf-8'))
    escolhaUser = clientSocket.recv(1024)
    clientSocket.sendall(options(escolhaUser.decode('utf-8')).encode('utf-8'))
    montarCarrinho(escolhaUser.decode('utf-8'))

# Função que faz o tratamento inicial com o cliente
def handleClient(clientSocket):
    global completeUserName
    mensagemBoasVindas = 'Bem vindo ao nosso servidor!'
    clientSocket.sendall(mensagemBoasVindas.encode('utf-8'))

    nameRecv = clientSocket.recv(1024)
    completeUserName = nameRecv.decode('utf-8')
    print('Usuario conectado: ', completeUserName)

    try:
        darOpcoes(clientSocket, completeUserName)
    except ConnectionResetError:
        print(f'{completeUserName} foi desconectado.')
    finally:
        clientSocket.close()

# Função para salvar informações dos clientes quando o servidor for encerrado
def salvarInformacoesClientes(signal, frame):
    # Cria um arquivo txt com o nome dos clientes que realizaram a compra e quanto cada um deles gastaram, além do valor total das vendas
    with open("relatorio-de-vendas-servidor/informacoes_clientes.txt", "w") as arquivo:
        arquivo.write("================ Relatório de Vendas ====================\n")
        for cliente, info in dataSet.compraClientes.items():
            arquivo.write(f"{cliente}: R${info}\n")
        arquivo.write("=========================================================\n")
        arquivo.write(f"Total de Vendas: R${dataSet.valorCaixa:.2f}\n")

    print("Informações dos clientes salvas.")
    # Mostra no terminal do servidor quanto de dinheiro tem o caixa após encerrar a execução do servidor
    print(f"Total de lucro das vendas: {dataSet.valorCaixa:.2f}")
    print("Para mais informações, verifique o relatorio gerado na pasta 'relatorio de vendas'! \nServidor Encerrado..." )
    sys.exit(0)

# Configuração do sinal para salvar informações dos clientes ao encerrar o servidor
signal.signal(signal.SIGINT, salvarInformacoesClientes)

HOST = 'localhost'
PORT = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
print('Servidor iniciado, aguardando conexões...')

while True:
    serverSocket.listen()
    clientSocket, address = serverSocket.accept()

    clientThread = threading.Thread(target=handleClient, args=(clientSocket,))
    clientThread.start()

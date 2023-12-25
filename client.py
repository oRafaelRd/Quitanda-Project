import socket

HOST = 'localhost'
PORT = 1024

# Função para finalizar as compras do lado do cliente
def finalizarCompras(clientSocket):
    print(clientSocket.recv(1024).decode('utf-8'))
    compra = input("Digite 'confirmar' para efetuar o pagamento ou 'cancelar' para cancelar a compra: ").lower()
    while compra not in ['confirmar', 'cancelar']:
        print("Opção inválida. Digite novamente.")
        compra = input("Digite 'confirmar' para efetuar o pagamento ou 'cancelar' para cancelar a compra: ").lower()
    
    clientSocket.sendall(compra.encode('utf-8'))
    
    if compra == 'confirmar':
        print("Pagamento efetuado com sucesso, Gerando recibo... ")
    else:
        print("Compra cancelada.")   

# Função para realizar compras 
def realizarCompras(clientSocket):
    while True:
        escolhaItem = input("Digite o item que você deseja: ").lower()
        clientSocket.sendall(escolhaItem.encode('utf-8'))
        itemDisponivel = clientSocket.recv(1024).decode('utf-8')
        if itemDisponivel == 'True':
            break
        else:
            print("Item não disponível no estoque, digite o item novamente: ")

    while True:
        quantidade = input("Quantos itens você deseja comprar desse produto? ")
        if quantidade.isdigit() and int(quantidade) > 0:
            break
        else:
            print("Quantidade inválida. Digite novamente.")

    clientSocket.sendall(quantidade.encode('utf-8'))

    while True:
        print('O que deseja fazer agora? \n [1] - Continuar comprando \n [2] - Cancelar compra \n [3] - Ver carrinho + total a ser pago \n [4] - Finalizar compra')
        op = input("Indique qual operação você deseja realizar: ")
        clientSocket.sendall(op.encode('utf-8'))
        if op.isdigit() and int(op) in range(1, 5):
            if int(op) == 1:
                print(itensDisponiveis)
                realizarCompras(clientSocket)
            elif int(op) == 2:
                print("Se desconectando do servidor")
                break
            elif int(op) == 3:
                print(clientSocket.recv(1024).decode('utf-8'))
            elif int(op) == 4:
                finalizarCompras(clientSocket)
                break
        else:
            print("Opção inválida. Digite novamente.")

    clientSocket.close()
    quit()

# Configuração do socket do cliente no lado do cliente
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))

# Recebimento da mensagem de boas-vindas do servidor quando o cliente se conecta ao servidor
mensagemServer = clientSocket.recv(1024)
print(mensagemServer.decode('utf-8'))

# Envio do nome do cliente para o servidor 
nome = input("Digite seu nome completo: ")
clientSocket.sendall(nome.encode('utf-8'))

# Recebe e exibe a mensagem de escolha de produtos
print(clientSocket.recv(1024).decode('utf-8'))
escolha = input('Digite aqui: ').lower()
while escolha not in ['frutas', 'legumes']:
    print("Digite corretamente!")
    escolha = input('Digite aqui: ').lower()

# Envio da escolha do cliente para o servidor
clientSocket.sendall(escolha.encode('utf-8'))

# Recebimento e exibição dos itens disponíveis no dataset do servidor de acordo com a escolha do cliente
itensDisponiveis = clientSocket.recv(1024).decode('utf-8')
print(itensDisponiveis)

# Chamada da função para que o cliente realize compras
realizarCompras(clientSocket)

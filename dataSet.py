#Arquivo que guarda as informações do servidor

# Variavel que guarda a quatidade de dinheiro no caixa do servidor
valorCaixa = 0

# Função que monta a lista com a categoria de itens escolhido pelo cliente
def options(choice):
    resul = ""  
    if choice == 'frutas':
        resul += "\n=== Opções de Frutas ===\n"
    
        for fruta, preco in frutas.items():
            resul += f'{fruta.ljust(20)} R${preco:.2f}\n'
    elif choice == 'legumes':
        resul += "\n=== Opções de Legumes ===\n"
    
        for legume, preco in legumes.items():
            resul += f'{legume.ljust(20)} R${preco:.2f}\n'
    
    return resul

# Dicionario que guarda o nome dos clientes que compraram algo, ou cancelaram a compra
compraClientes = {

}

# Dicionarios com itens e preço da unidade
frutas = {
    'maçã': 2.5,
    'banana': 1.0,
    'laranja': 1.8,
    'uva': 3.2,
    'morango': 4.0,
    'abacaxi': 2.7,
    'kiwi': 2.3,
    'pêssego': 2.5,
    'manga': 3.0,
    'melancia': 1.5
}

legumes = {
    'cenoura': 1.2,
    'batata': 1.5,
    'alface': 2.0,
    'abobrinha': 2.3,
    'tomate': 2.8,
    'cebola': 1.7,
    'brócolis': 2.5,
    'couve-flor': 2.4,
    'pimentão': 3.0,
    'espinafre': 2.2
}


import time, datetime, random


def criar_usuarios(usuarios):
    cpf = input('Digite o CPF: ')
    usuario = filtar_usuarios(cpf, usuarios)

    if usuario:
        print('Usuário já existe')
        return

    nome = input('Digite o nome: ')
    nascimento = input('Digite o nascimento: ')
    endereco = input('Digite o endereco: ')
    usuarios.append({'nome': nome, 'nascimento': nascimento, 'endereco': endereco, 'cpf': cpf})

    print('Usuário cadastrado com sucesso')


def filtar_usuarios(cpf, usuarios):
    verificar = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return verificar[0] if verificar else None


def criar_conta(agencia, contas, usuarios):
    cpf = input('Digite o CPF: ')
    filtro = filtar_usuarios(cpf, usuarios)
    if filtro:
        while True:
            conta = gerar_cc()
            verificar = filtar_conta_existente(conta, contas)
            if verificar is None:
                contas.append({'agencia': agencia, 'conta': conta, 'cpf': cpf,
                               'dados': {'saldo': 0, 'id': 0, 'extrato': [], 'saques': {'ultimaData': '', 'qtd': 0}}})
                print(f'Conta criada com sucesso\nAgência: {agencia} || Conta: {conta}')
                return
            elif verificar is not None:
                print('Conta já existente e vinculada a um usuário')
                return
    else:
        print('Usuário não existe, por favor, crie seu usuário')
        criar_usuarios(usuarios)
        criar_conta(agencia, contas, usuarios)


def filtar_conta_existente(conta_num, constas):
    verificar = [conta for conta in constas if conta['conta'] == conta_num]
    return verificar[0] if verificar else None


def filtrar_conta(cpf, contas):
    verificar = [conta for conta in contas if conta['cpf'] == cpf]
    return verificar[0] if verificar else None


def depositar(contas):
    cpf = input('Digite o CPF: ')
    retorno = filtrar_conta(cpf, contas)
    if retorno:
        valor = float(input('Digite o valor do deposito: R$'))
        if valor > 0:
            retorno['dados']['saldo'] += valor
            retorno['dados']['id'] += 1
            retorno['dados']['extrato'].append(
                {'id': retorno['dados']['id'], 'operacao': 'Deposito', 'valor': valor, 'data': datetime.datetime.now()})
            print(f'Operação: Depósito\nValor: R${valor:.2f}\nStatus: Aprovado')
            time.sleep(5)
            return
        else:
            print(f'Operação: Depósito\nValor: R${valor:.2f}\nStatus: Rejeitado\nMotivo: Valor negativo')
            time.sleep(5)
            return
    else:
        print(f'Operação: Depósito\nStatus: Rejeitado\nMotivo: Conta inexistente')
        time.sleep(5)
        return


def saque(contas, limite, qtd):
    cpf = input('Digite o CPF: ')
    retorno = filtrar_conta(cpf, contas)
    if retorno:
        if retorno['dados']['saques']['qtd'] < qtd:
            valor = float(input('Digite o valor do saque: R$'))
            if valor <= limite and valor < retorno['dados']['saldo']:
                retorno['dados']['saldo'] -= valor
                retorno['dados']['id'] += 1
                retorno['dados']['extrato'].append({'id': retorno['dados']['id'], 'operacao': 'Saque', 'valor': -valor,
                                                    'data': datetime.datetime.now()})
                if len(retorno['dados']['saques']) > 0:
                    if retorno['dados']['saques']['ultimaData'] == datetime.datetime.now().strftime("%d/%m/%Y"):
                        retorno['dados']['saques']['qtd'] += 1
                        print(f'Operação: Saque\nValor: R${valor:.2f}\nStatus: Aprovado')
                        time.sleep(5)
                        return
                    else:
                        retorno['dados']['saques']['qtd'] = 1
                        retorno['dados']['saques']['ultimaData'] = datetime.datetime.now().strftime("%d/%m/%Y")
                        print(f'Operação: Saque\nValor: R${valor:.2f}\nStatus: Aprovado')
                        time.sleep(5)
                        return
                else:
                    retorno['dados']['saques']['qtd'] = 1
                    retorno['dados']['saques']['ultimaData'] = datetime.datetime.now().strftime("%d/%m/%Y")
                    print(f'Operação: Saque\nValor: R${valor:.2f}\nStatus: Aprovado')
                    time.sleep(5)
                    return
            else:
                print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Valor acima do limite')
                time.sleep(5)
                return
        else:
            print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Limite de saque excedido')
            time.sleep(5)
            return
    else:
        print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Conta inexistente')
        time.sleep(5)
        return


def extrato(contas):
    soos = input('Digite o CPF: ')
    retorno = filtrar_conta(soos, contas)
    if retorno:
        str_trans = '\n'.join(
            [f'{t["id"]:>3} - {t["operacao"]:<10}: R${t["valor"]:>10.2f}' for t in retorno['dados']['extrato']])
        qtdLinha = max(len(linha) for linha in str_trans.strip().split('\n'))
        if qtdLinha > 0:
            div = '-' * qtdLinha
        else:
            str_trans = 'Não Foram realizadas movimentações'
            div = '-' * len(str_trans)
        extrato = f'''
{div}
{' '*10}Extrato
{div}
Agência: {retorno['agencia']}
Conta: {retorno['conta']}
Saldo: {retorno['dados']['saldo']:.2f}
{div}
{str_trans}
{div}
{datetime.datetime.now()}
{div}
'''.strip()
        print(extrato)
    else:
        print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Conta inexistente')
        time.sleep(5)
        return


def gerar_cc():
    return random.randrange(10000, 100000)


def menu():
    Menu = f'''
{'#' * 30}
#        Banco Foderal       #
{'#' * 30}
1 - criar conta
2 - Depósito
3 - Saque
4 - Extrato
0 - Sair
'''.strip()
    print(Menu)


def main():
    clientes = []
    LIMIT_SAQUE = 500
    LIMIT_QTD = 3
    AGENCIA = '0001'
    contas = []
    while True:
        menu()

        op = int(input('Escolha: '))

        if op == 0:
            print('Muito obrigado por usar o programa!')
            break
        elif op == 1:
            criar_conta(AGENCIA, contas, clientes)
        elif op == 2:
            depositar(contas)
        elif op == 3:
            saque(contas, LIMIT_SAQUE, LIMIT_QTD)
        elif op == 4:
            extrato(contas)


if __name__ == '__main__':
    main()
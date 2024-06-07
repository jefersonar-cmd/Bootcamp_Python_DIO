import time, datetime, random
MENU = f'''

{'#'*30}
#        Banco Memeral       #
{'#'*30}
1 - Depósito
2 - Saque
3 - Extrato
0 - Sair
'''
CONTA = random.randrange(100000,1000000)
LIMITE_SAQUE = 500
qtd_saque = 0
saldo = 0
transacoes = []
id = 0
while True:
    print(MENU)

    escolha = int(input('Escolha uma opção: '))
    if escolha == 1:
        entrada = float(input('Valor a ser depositado: R$'))
        if entrada > 0:
            saldo += entrada
            id += 1
            transacoes.append({'id': id, 'tipo': 'Depósito', 'valor': entrada})
            print(f'Operação: Depósito\nValor: R${entrada:.2f}\nStatus: Aprovado')
            time.sleep(3)
        else:
            print(f'Operação: Depósito\nValor: R${entrada:.2f}\nStatus: Rejeitado\nMotivo: Valor negativo')
            time.sleep(3)
    elif escolha == 2:
        if qtd_saque < 3:
            if saldo > 0:
                saque = float(input('Valor a ser Sacado: R$'))
                if saque <= LIMITE_SAQUE:
                    saldo -= saque
                    qtd_saque += 1
                    id += 1
                    transacoes.append({'id': id, 'tipo': 'Saque', 'valor': -saque})
                    print(f'Operação: Saque\nValor: R${saque:.2f}\nStatus: Aprovado')
                    time.sleep(3)
                else:
                    print(f'Operação: Saque\nValor: R${saque:.2f}\nStatus: Rejeitado\nMotivo: Valor acima de R$500')
                    time.sleep(3)
            else:
                print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Você não possui saldo disponível')
                time.sleep(3)
        else:
            print(f'Operação: Saque\nStatus: Rejeitado\nMotivo: Atingido limite de Saque diário')
            time.sleep(3)
    elif escolha == 3:
        transacoes_str = '\n'.join([f'{t["id"]:>3} - {t["tipo"]:<10}: R${t["valor"]:>10.2f}' for t in transacoes])
        trs_linha = max(len(linha) for linha in transacoes_str.strip().split('\n'))
        if trs_linha > 0:
            div = '-'*trs_linha
        else:
            transacoes_str = 'Não Foram realizadas movimentações'
            div = '-'*len(transacoes_str)
        extrato = f'''
{div}
Conta: {CONTA}
Saldo: {saldo:.2f}
{div}
{transacoes_str}
{div}
{datetime.datetime.now()}
'''.strip()
        print(extrato)
    elif escolha == 0:
        print('Obrigado por utilizar o sistema bancário')
        break
    else:
        print('Escolha uma opção válida')




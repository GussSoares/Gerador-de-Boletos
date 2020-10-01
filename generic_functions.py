# função para cálculo dos dígitos validadores do nosso número e do código de barras
def modulo_onze(sequencia, nn=False, cb=False):
    # inverte a sequência recebida
    sequencia = sequencia[::-1]

    # veriárvel responsável pelo somatório dos resultados das multiplicações do dígito por um número entre 2 e 9
    somatorio = 0

    # contador pro controle da sequência
    contador = 2
    for i in range(len(sequencia)):
        somatorio += int(sequencia[i]) * contador
        contador += 1

        # reinicia contador em 2
        if contador == 10:
            contador = 2

    # para código de barras, o somatório é multiplicado por 10
    if cb:
        somatorio *= 10
        digito_verificador = somatorio % 11

        # para o código de barras, o dígito verificador vira 1 em caso do cálculo ter gerado 0 ou 10
        if digito_verificador == 0 or digito_verificador == 10:
            return "1"
        else:
            return str(digito_verificador)

    # para o nosso número o somatório permanece
    if nn:
        digito_verificador = 11 - somatorio % 11
        # para o nosso número, o dígito verificador vira 0 em caso do cálculo ter gerado 1 e 1 para caso tenha gerado 10
        if digito_verificador == 1:
            return "0"
        elif digito_verificador == 10:
            return "1"
        else:
            return str(digito_verificador)


# função que gera o dígito verificador dos 3 primeiros campos de um boleto santander
def gerar_digito_verificador(sequencia):
    # inverte a sequência recebida
    sequencia = sequencia[::-1]

    # veriárvel responsável pelo somatório dos resultados das multiplicações de cada dígito por 2 ou 1
    somatorio = 0

    for i in range(len(sequencia)):
        if i % 2 == 0:
            if int(sequencia[i]) < 5:
                somatorio += int(sequencia[i]) * 2
            else:
                aux = str(int(sequencia[i]) * 2)
                somatorio += int(aux[0]) + int(aux[1])
        else:
            somatorio += int(sequencia[i])
    digito_verificador = 10 - somatorio % 10

    return str(digito_verificador)
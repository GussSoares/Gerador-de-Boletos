import datetime


# from decimal import Decimal

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

# TODO: utilização de dicionário de dados
class BoletoSantander(object):
    codigo_banco = "033"  # identificação do banco
    codigo_moeda = "9"  # código da moeda (9 para real e 8 para moeda estrangeira
    campos_fixos = ["9", "00000", "0"]  # campos fixos utilizados na geração do número digitável do boleto
    fator_data = datetime.date(1997, 10, 7)  # data base para gerar fator de vencimento
    codigo_beneficiario = "0282033"  # código do beneficiário (PSK) gerado pelo banco
    modalidade_carteira = "101"  # modalidade da carteira (101 para cobrança rápida com registro

    def __init__(self, data_vencimento, valor_nominal):
        self.data_vencimento = data_vencimento
        self.valor_nominal = valor_nominal
        self.fator_vencimento = self.gerar_fator_vencimento(data_vencimento, self.fator_data)
        self.nosso_numero = self.gerar_nosso_numero()
        self.codigo_de_barras, self.linha_digitavel = self.gerar_boleto(self.codigo_banco, self.codigo_moeda,
                                                                         self.campos_fixos,
                                                                         self.fator_vencimento, valor_nominal,
                                                                         self.codigo_beneficiario,
                                                                         self.nosso_numero, self.modalidade_carteira)

    # TODO: geração automática do campo "nosso número" para geração de boletos
    # gera o nosso número e seu código verificador
    @staticmethod
    def gerar_nosso_numero():
        nosso_numero = "566612457800"
        return nosso_numero + modulo_onze(nosso_numero, True)

    # TODO: geração automática da data a partir da geração do boleto considerando finais de semana e feriados
    # método para gerar o fator de vencimento do boleto a partir de sua data de vencimento
    @staticmethod
    def gerar_fator_vencimento(data_vencimento, fator_data):
        return str((data_vencimento - fator_data).days)

    # TODO: verificar dados (tipo e tamanho) antes de gerar o boleto
    # função geradora de código de barras (em número)
    @staticmethod
    def gerar_boleto(codigo_banco, codigo_moeda, campos_fixos, fator_vencimento, valor_nominal,
                     codigo_beneficiario, nosso_numero, modalidade_carteira):
        # sequência do código de barras em forma numérica
        codigo_de_barras = codigo_banco + codigo_moeda + fator_vencimento + str(valor_nominal).replace(".", "").zfill(
            10) + campos_fixos[0] + codigo_beneficiario + campos_fixos[1] + nosso_numero[5:] + campos_fixos[
                               2] + modalidade_carteira
        verificador_cb = modulo_onze(codigo_de_barras, False, True)

        # montar campos

        # primeiro campo da linha digitável
        primeiro_campo = codigo_banco + codigo_moeda + campos_fixos[0] + codigo_beneficiario[0:4]
        primeiro_campo += gerar_digito_verificador(primeiro_campo)

        # segundo campo da linha digitável
        segundo_campo = codigo_beneficiario[4:] + nosso_numero[0:7]
        segundo_campo += gerar_digito_verificador(segundo_campo)

        # terceiro campo da linha digitável
        terceiro_campo = nosso_numero[7:] + campos_fixos[2] + modalidade_carteira
        terceiro_campo += gerar_digito_verificador(terceiro_campo)

        # quarto campo da linha digitável
        # verificador_cb

        # quinto campo da linha digitável
        quinto_campo = fator_vencimento + str(valor_nominal).replace(".", "").zfill(10)

        linha_digitavel = primeiro_campo + segundo_campo + terceiro_campo + verificador_cb + quinto_campo

        return codigo_de_barras[0:4] + verificador_cb + codigo_de_barras[4:], linha_digitavel

    # TODO: verificar tamanho do boleto antes de conferir o verificador
    # método para checar dígito validador do código de barras
    @staticmethod
    def checar_dv_cb(cb):
        return cb[4]

    def formatar_linha_digitavel(self, linha_digitavel):
       return linha_digitavel[0:5] + "." + linha_digitavel[5:10] + " " + linha_digitavel[10:15] + "." + linha_digitavel[15:21] + " " + linha_digitavel[21:26] + "." + linha_digitavel[26:32] + " " + linha_digitavel[32] + " " + linha_digitavel[33:]

def gerar_primeiro_campo(codigo_banco, codigo_moeda, campo_fixo, codigo_beneficiario):
    primeiro_campo = codigo_banco + codigo_moeda + campo_fixo + codigo_beneficiario[0:4]

    print("---PRIMEIRO CAMPO DE DADOS---")
    print("código banco: {}\ncódigo moeda: {}\ncampo fixo: {}\nPSK: {}".format(codigo_banco, codigo_moeda, campo_fixo,
                                                                               codigo_beneficiario[0:4]))
    print("primeiro campo sem código verificador:", primeiro_campo)

    codigo_verificador = gerar_digito_verificador(primeiro_campo)
    print("dígito verificador do campo:", codigo_verificador)
    ipte_parcial = primeiro_campo + codigo_verificador

    print("--------------------------------------------------")
    print("primeiro campo com código verificador:", ipte_parcial)
    print("--------------------------------------------------")

    return ipte_parcial


def gerar_segundo_campo(codigo_beneficiario, nosso_numero):
    segundo_campo = codigo_beneficiario[4:] + nosso_numero[0:7]
    print("---SEGUNDO CAMPO DE DADOS---")
    print("código do beneficiário: {}\nnosso número: {}".format(codigo_beneficiario[4:], nosso_numero[0:7]))
    print("segundo campo sem código verificador:", segundo_campo)

    codigo_verificador = gerar_digito_verificador(segundo_campo)
    print("dígito verificador do campo:", codigo_verificador)
    ipte_parcial = segundo_campo + codigo_verificador

    print("--------------------------------------------------")
    print("segundo campo com código verificador:", ipte_parcial)
    print("--------------------------------------------------")

    return ipte_parcial


def gerar_terceiro_campo(nosso_numero, iof, modalidade_carteira):
    terceiro_campo = nosso_numero[7:] + iof + modalidade_carteira
    print("---TERCEIRO CAMPO DE DADOS---")
    print("nosso número: {}\niof: {}\nmodalidade da carteira: {}".format(nosso_numero[7:], iof, modalidade_carteira))
    print("terceiro campo sem código verificador:", terceiro_campo)

    codigo_verificador = gerar_digito_verificador(terceiro_campo)
    print("dígito verificador do campo:", codigo_verificador)
    ipte_parcial = terceiro_campo + codigo_verificador

    print("--------------------------------------------------")
    print("terceiro campo com código verificador:", ipte_parcial)
    print("--------------------------------------------------")

    return ipte_parcial


def gerar_quarto_campo(verificador):
    print("---QUARTO CAMPO DE DADOS---")
    print("verificador do código de barras: ", verificador)
    print("quarto campo (verificador do código de barras):", verificador)
    print("--------------------------------------------------")


def gerar_quinto_campo(fator_vencimento, valor_nominal):
    print("---QUINTO CAMPO DE DADOS---")
    print("fator vencimento: {}\nvalor nominal: {}".format(fator_vencimento, valor_nominal))
    print("quinto campo de dados:", fator_vencimento + str(valor_nominal).replace(".", "").zfill(10))


def gerar_cb(codigo_banco, codigo_moeda, fator_data, data_vencimento, valor_nominal, codigo_beneficiario, nosso_numero,
             modalidade_carteira, cnab_400=True):  # função geradora de código de barras (em número)
    """
    Posição Tamanho Picture     Conteúdo
    01-03   3       9 (03)      Identificação do Banco = 033
    04-04   1       9 (01)      Código da moeda = 9 (real)
    05-05   1       9 (01)      DV do código de barras
    06-09   4       9 (04)      Fator de vencimento
    10-19   10      9 (08)V99   Valor nominal
    20-20   1       9 (01)      Fixo “9”
    21-27   7       9 (07)      Código do beneficiário padrão Santander
    28-40   13      9 (13)      Nosso Número com DV
    41-41   1       9 (01)      Fixo “0”
    42-44   3       9 (03)      Tipo de Modalidade Carteira
                                101-Cobrança Rápida COM Registro
                                104-Cobrança Eletrônica COM Registro
    """
    layout_cb = ""
    if cnab_400:
        campos_fixos = ["9", "00000", "0"]
        valor_nominal = str(valor_nominal).replace(".", "").zfill(10)
        print("--------------------------------------------------")
        layout_cb = codigo_banco + codigo_moeda + fator_vencimento_cb(fator_data, data_vencimento) + valor_nominal + \
                    campos_fixos[0] + codigo_beneficiario + campos_fixos[1] + nosso_numero[5:] + campos_fixos[
                        2] + modalidade_carteira
    return layout_cb


def fator_vencimento_cb(data_vencimento, fator_data_vencimento):
    return str((data_vencimento - fator_data_vencimento).days)


# PRENCHIMENTO DE CAMPOS

# Posição 	Conteúdo
# 1 a 3    Código do banco
# 4        Código da Moeda - 9 para Real ou 8 - outras moedas
# 5        Fixo "9"
# 6 a 9    PSK - Código beneficiário (4 primeiros digitos)
# 10 a 12  Restante do PSK (3 digitos)
# 13 a 19  7 primeiros digitos do Nosso Número (N/N)
# 20 a 25  Restante do Nosso numero (8 digitos) - total 13 (incluindo digito verificador)
# 26 a 26  IOS
# 27 a 29  Tipo Modalidade Carteira
# 30 a 30  Dígito verificador do código de barras
# 31 a 34  Fator de vencimento (quantidade de dias desde 07/10/1997 até a data de vencimento)
# 35 a 44  Valor do título

"""
1º Campo: composto pelo código do banco, código da moeda, campo fixo "9", quatro
primeiras posições do código do beneficiário padrão Santander (PSK) e dígito verificador
deste campo.
"""

codigo_banco = "033"  # código do banco Santander
codigo_moeda = "9"  # código para moeda local (Real)
campo_fixo = "9"  # campo fixo que nunca muda na posição 5 do primeiro campo
codigo_beneficiario = "0282033"  # apenas as 4 primeiras posições [0:3]
primeiro_campo = gerar_primeiro_campo(codigo_banco, codigo_moeda, campo_fixo,
                                      codigo_beneficiario)  # chama a função que o retorna dígito verificador

"""
2º Campo: composto pelas 3 posições restantes do código do beneficiário
Santander (PSK), nosso número (N/N) com as 7 primeiras posições e dígito verificador
deste campo.
"""
nosso_numero = "566612457800"
nosso_numero += modulo_onze(nosso_numero, True)
# chama a função que o retorna dígito verificador do primeiro campo
segundo_campo = gerar_segundo_campo(codigo_beneficiario, nosso_numero)

"""
3º Campo: composto pelas 6 primeiras posições restante do N/N, 1 posição
referente ao IOF, 3 posições referente ao Tipo de Modalidade da Carteira mais o
dígito verificador deste campo.
"""

iof = "0"
modalidade_carteira = "101"  # cobrança rápida com registro
terceiro_campo = gerar_terceiro_campo(nosso_numero, iof, modalidade_carteira)

"""
4º campo: dígito verificador do código de barras (DAC)
"""
codigo_de_barras = "0339204600000273719028203356661245780020101"
verificador = modulo_onze(codigo_de_barras, False, True)
gerar_quarto_campo(verificador)

"""
5º campo: composto pelas 4 primeiras posições do fator vencimento (*) e as 10
últimas com o valor nominal do documento, com indicação de zeros a esquerda e sem
edição (sem ponto e vírgula).
"""

fator_data = datetime.date(1997, 10, 7)
data_vencimento = datetime.date(2003, 5, 15)
fator_vencimento = fator_vencimento_cb(data_vencimento, fator_data)
valor_nominal = 273.71
gerar_quinto_campo(fator_vencimento, valor_nominal)

"""
Nota 1: editar os três primeiros campos com um ponto (.), a ser inserido entre a 5ª e 6ª
posições de cada campo.

Nota 2: os dados da representação numérica não se apresentam na mesma ordem do
código de barras, mas sim de acordo com a seqüência descrita acima.

Nota 3: os dígitos verificadores referentes aos campos 1, 2, 3, não são
representados no código de barras.
"""

# CODÍGO DE BARRAS (teste)

teste = gerar_cb(codigo_banco, codigo_moeda, fator_data, data_vencimento, valor_nominal, codigo_beneficiario,
                 nosso_numero,
                 modalidade_carteira,
                 True
                 )

codigo_de_barras = codigo_de_barras[0:4] + verificador + codigo_de_barras[4:]
print("código de barras final: {}".format(codigo_de_barras))

ipte_completo = (primeiro_campo + segundo_campo + terceiro_campo + verificador + fator_vencimento + str(
    valor_nominal).replace(".", "").zfill(10)).replace(".", "")
print("IPTE Completo: ",
      primeiro_campo + " " + segundo_campo + " " + terceiro_campo + " " + verificador + " " + fator_vencimento + str(
          valor_nominal).replace(".", "").zfill(10))

data_teste = datetime.date(2003, 5, 15)
valor_teste = 273.71
boleto = BoletoSantander(data_teste, valor_teste)
vencimento = boleto.fator_vencimento
nossonumero = boleto.nosso_numero
codigobarras = boleto.codigo_de_barras
print("--------------------------------------------------")
print("Objeto BoletoSantander:\ndata: {}\nvalor: {}\nfator vencimento: {}".format(boleto.data_vencimento, boleto.valor_nominal,
                                                                         boleto.fator_vencimento))
print("nosso número: ", nossonumero)
print("código de barras: ", codigobarras)
print("dígito validador do códigod de barras: ", boleto.checar_dv_cb(codigobarras))
print("IPTE Completo: ", boleto.linha_digitavel)
print("Linha digitável formatada: ", boleto.formatar_linha_digitavel(boleto.linha_digitavel))
print("--------------------------------------------------")
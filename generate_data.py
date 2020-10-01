import datetime

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

    @staticmethod
    def formatar_linha_digitavel(linha_digitavel):
        return linha_digitavel[0:5] + "." + linha_digitavel[5:10] + " " + linha_digitavel[10:15] + "." + linha_digitavel[15:21] + " " + linha_digitavel[21:26] + "." + linha_digitavel[26:32] + " " + linha_digitavel[32] + " " + linha_digitavel[33:]
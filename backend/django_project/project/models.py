from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal
from django_pandas.managers import DataFrameManager

# Be careful with related_name and related_query_name. Why?
class BaseModel(models.Model):
    objects = DataFrameManager()
    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"

    ESTADOS_CHOICES = [
        (AC, "Acre"),
        (AL, "Alagoas"),
        (AP, "Amapá"),
        (AM, "Amazonas"),
        (BA, "Bahia"),
        (CE, "Ceará"),
        (DF, "Distrito Federal"),
        (ES, "Espírito Santo"),
        (GO, "Goiás"),
        (MA, "Maranhão"),
        (MT, "Mato Grosso"),
        (MS, "Mato Grosso do Sul"),
        (MG, "Minas Gerais"),
        (PA, "Pará"),
        (PB, "Paraíba"),
        (PR, "Paraná"),
        (PE, "Pernambuco"),
        (PI, "Piauí"),
        (RJ, "Rio de Janeiro"),
        (RN, "Rio Grande do Norte"),
        (RS, "Rio Grande do Sul"),
        (RO, "Rondônia"),
        (RR, "Roraima"),
        (SC, "Santa Catarina"),
        (SP, "São Paulo"),
        (SE, "Sergipe"),
        (TO, "Tocantins"),
    ]

    created = models.DateTimeField(auto_now=True, verbose_name=_("Data de criação"))
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name=_("Última modificacao")
    )
    isActive = models.BooleanField(default=True, null=True)
    isPublic = models.BooleanField(default=False, null=True)
    isRemoved = models.BooleanField(default=False, null=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    @classmethod
    def propriedades(cls):
        return list(map(lambda f: f.name, cls._meta.fields))

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Exception:
            return None

    def coord_from_address(self,address):
        try:
            url = f"http://45.56.102.198:8181/search.php?address={address}&format=json"
            return requests.get(url, timeout=20).json()        
        except Exception as e:
            print(e.__repr__())
            return [{}]


    def reverse_address_from_postal_code(self,postalcode):
        try:
            url = f"http://45.56.102.198:8181/search.php?postalcode={postalcode}&format=json"
            return requests.get(url, timeout=20).json()        
        except Exception as e:
            print(e.__repr__())
            return [{}]

    class Meta:
        abstract = True
        ordering = ["created"]

detecta_espacos = re.compile(r'\s+')
detecta_caracteres = re.compile(r'\D+')

class SefazRSBase():  
    TABELA_ITENS=9
    TABELA_TOTAIS=10
    TABELA_EMISSOR=4
    TABELA_ENDERECO_EMISSOR=5
    TABELA_CHAVE=7
    TABELA_CONSUMIDOR=8
    

    @property
    def soup_parser(self):
        return BeautifulSoup(self.original_html_content, 'html.parser')


    @property
    def nfe_container(self):
        container =  self.soup_parser.find(id="nfce")
        return container

    @property
    def all_tables(self):
        # todas = BeautifulSoup(f"<html><body>{self.soup_parser.find_all('table')}</body></html>", 'html.parser') 
        # [x.extract() for x in todas.find_all('script')]       
        return self.nfe_container.find_all('table')


    @property
    def all_tds(self):
        return self.nfe_container.find_all('td')

    @property
    def all_trs(self):
        return self.nfe_container.find_all('tr')



    @property
    def tabela_consumidor(self):
        return self.all_tables[self.TABELA_CONSUMIDOR]

    @property
    def tabela_emissor(self):
        return self.all_tables[self.TABELA_EMISSOR]

    @property
    def tabela_endereco_emissor(self):
        return self.all_tables[self.TABELA_ENDERECO_EMISSOR]



    @property
    def tabela_com_itens(self):
        return self.all_tables[self.TABELA_ITENS]


    @property
    def tabela_com_totais(self):
        try:        
            totais = self.all_tables[self.TABELA_TOTAIS]
            return totais
        except Exception as e:
            print(e.__repr__())
            print("totais com erro")
        return self.all_tables


    @property
    def tabela_com_chave(self):
        return self.all_tables[self.TABELA_CHAVE]


    @property
    def total_itens(self):
        return self.all_tables.__len__()




    @property
    def total_tabelas(self):
        index=0
        n = "#"*5
        # print(f"{n} {self.id} {n}")
        # print(self.all_tables[0])
        # print(f"{n} {index} {n}")
        # for t in self.all_tables:
        #    
        #     print(f"{n} {index} {n}")
        #     print(t)
        #     print(f"{n} {index} {n}")
        #     index+=1

        excluir=[0,1,2,3,6]
        return self.all_tables.__len__()




    @property
    def nfe_logo(self):        
        logo_parser = BeautifulSoup(f"<html><body>{self.first_table}</body></html>", 'html.parser')        
        logo = logo_parser.find("img")
        url = '/static/placeholder.png'
        if logo:
            url = logo.get('src','/static/placeholder.png')
        
        return url



    def processaItens(self):
        itens = list(map(lambda x:x, self.tabela_com_itens.find_all('tr')))
        lista_de_itens = itens[1:]
        lista_itens = []
     
        for item in lista_de_itens:
            item_parser = BeautifulSoup(f"<html><body>{item}</body></html>", 'html.parser')
            itens_list = list(map(lambda x:x.text, item_parser.find_all(class_='NFCDetalhe_Item')))

            if itens_list.__len__() >4:
                item_object = {
                    "codigo":itens_list[0],
                    "descricao":itens_list[1],
                    "qt":itens_list[2],
                    "unidade":itens_list[3],
                    "valor_unitario":itens_list[4],
                    "valor_total":itens_list[5]
                }
                lista_itens.append(item_object)
        return {
            "itens":lista_itens
        }


    def processaTotais(self):

        totais = list(map(lambda x:x.text, self.tabela_com_totais.find_all(class_='NFCDetalhe_Item')))

      

        if totais.__len__() > 7:
            valor_total = totais[1]
            valor_descontos = totais[3]
            valor_pago = totais[7]
            forma_pagamento = totais[6]
            
            objeto ={}

            try:
                valor = valor_total.replace(",",".")

                if valor.__len__():

                    valor_total_convertido=Decimal(valor.replace(".", "", valor.count(".") -1))
                    objeto.update({"valor_total":valor_total_convertido})
            except Exception as e:
                print(e.__repr__())
                print(valor_total.replace(",",""))
                print(valor_total)
                print("valor_total com erro")


            try:
                valor = valor_descontos.replace(",",".")
                if valor.__len__():
                    valor_descontos_convertido=Decimal(valor.replace(".", "", valor.count(".") -1))
                    objeto.update({"valor_descontos":valor_descontos_convertido})
            except Exception as e:
                # print(e.__repr__())
                print("valor_desconto com erro")
        
                


            try:
                valor = valor_pago.replace(",",".")
                if valor.__len__():

                    valor_pago_convertido=Decimal(valor.replace(".", "", valor.count(".") -1))
                    objeto.update({"valor_pago":valor_pago_convertido})
            except Exception as e:
                print( valor_pago.replace(",",""))
                print(valor_pago)
                print("valor_pago com erro")


            objeto.update({"forma_pagamento":forma_pagamento})
         
        return objeto

    def processaConsumidor(self):      
        cpf = list(map(lambda x:x.text.strip(), self.tabela_consumidor.find_all(class_='NFCCabecalho_SubTitulo')))
        return {
            "cpf":re.sub(detecta_caracteres,'', "".join(cpf))
        }

    def processaChaveDaNota(self):
        objeto = {}
        tabela_chave = self.tabela_com_chave
      
        chave_lista = list(map(lambda x:x.text.strip(), tabela_chave.find_all(class_='NFCCabecalho_SubTitulo')))
     
        

        try:
            chave_da_nota = re.sub(detecta_caracteres,'', chave_lista[3])

            protocolo_autorizacao = re.sub(detecta_caracteres,'', chave_lista[4])        
            numero_serie_e_data = re.sub(detecta_espacos,'\n', chave_lista[0]).split('\n')
            numero_da_nota = numero_serie_e_data[2]
            serie_da_nota = numero_serie_e_data[4]
            data_da_nota = numero_serie_e_data[8]
            hora_da_nota = numero_serie_e_data[9]

            objeto.update({
                "numero_da_nota":numero_da_nota,
                "serie_da_nota":serie_da_nota,
                "data_da_nota":data_da_nota,
                "hora_da_nota":hora_da_nota,
                "chave_da_nota":chave_da_nota,
                "protocolo_autorizacao":protocolo_autorizacao
                })
        except Exception as e:
            print(chave_lista)
            print(tabela_chave)
            print(e.__repr__())


        return objeto

    def processaEmissor(self):
        objeto = {}
        razao_social = self.tabela_emissor.find(class_='NFCCabecalho_SubTitulo')

        objeto.update({"razao_social":razao_social.text})
        
        cnpj_inscricao = self.tabela_emissor.find(class_='NFCCabecalho_SubTitulo1')
        sentence = re.sub(detecta_espacos, '\n', cnpj_inscricao.text.strip())
        result = sentence.split('\n')
        cnpj = re.sub(detecta_caracteres,'', result[1])
        objeto.update({"cnpj":cnpj})
        inscricao_estadual = re.sub(detecta_caracteres,'', result[4])
        objeto.update({"inscricao_estadual":inscricao_estadual})
        endereco_emissor = self.tabela_endereco_emissor
        endereco= re.sub(detecta_espacos, '\n', endereco_emissor.find(class_="NFCCabecalho_SubTitulo1").text.strip())
        endereco_do_emissor=' '.join(endereco.split('\n'))
        objeto.update({"endereco_emissor":endereco_do_emissor})

        

        return objeto


class StackedModel(BaseModel):
    stackOrder = models.FloatField(default=100, verbose_name=_("Ordem de exibição"))

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ["stackOrder"]

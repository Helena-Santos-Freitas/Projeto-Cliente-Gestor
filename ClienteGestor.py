from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

import sqlite3
import time

# Função para criar a conexão com o banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect('banco_CG.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

# Verifica se a tabela clientes existe, caso contrário, cria a tabela
def criar_tabela():
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute('''CREATE TABLE clientes IF NOT EXISTS (
                                nome text, 
                                rg text PRIMARY KEY, 
                                endereco text, 
                                email text, 
                                telefone text, 
                                data_de_nascimento text, 
                                data_da_compra text,
                                valor_da_compra real)''')
        conn.close()

class Cliente:
    def __init__(self, nome, rg, endereco, email, telefone, data_de_nascimento, data_da_compra, valor_da_compra):
        self.nome = nome
        self.rg = rg
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.data_de_nascimento = data_de_nascimento
        self.data_da_compra = data_da_compra
        self.valor_da_compra = valor_da_compra


def funcao_login():
    login.show()
    email = login.lineEmail.text()
    senha = login.lineSenha.text()
    entrar_email = 'admin'
    entrar_senha = 'admin'
    if email == entrar_email and senha == entrar_senha:
        login.close()
        gerenciamento.show()
    else:
        login.lineEdit.setText('E-mail ou senha incorretos')

def funcao_registro():
    gerenciamento.close()
    registro.show()
    try:
        nome = registro.lineNome.text()
        rg = registro.lineRg.text()
        endereco =  registro.lineEndereco.text()
        email =  registro.lineEmailR.text()
        telefone = registro.lineTelefone.text()
        data_de_nascimento = registro.lineDataN.text()
        data_da_compra = registro.lineDataCompra.text()
        valor_da_compra = registro.lineValorCompra.text()
    
    except ValueError as e:
       registro.lineRegistrou.setText(f"Erro de conversão: {e}")
    except AttributeError as e:
       registro.lineRegistrou.setText(f"Erro de atributo: {e}")
    cliente_instance = Cliente(nome, rg, endereco, email, telefone, data_de_nascimento, data_da_compra, valor_da_compra)
    if(rg != ""):
        conn = conectar_banco()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''INSERT INTO clientes (nome, rg, endereco, email, telefone, data_de_nascimento, data_da_compra, valor_da_compra)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (cliente_instance.nome, cliente_instance.rg, cliente_instance.endereco, cliente_instance.email, 
                                cliente_instance.telefone, cliente_instance.data_de_nascimento, cliente_instance.data_da_compra, 
                                cliente_instance.valor_da_compra))
                conn.commit()
                registro.lineRegistrou.setText('Cliente cadastrado com sucesso!')
            except sqlite3.Error as e:
                registro.lineRegistrou.setText(f'Erro ao cadastrar cliente: {e}')
            finally:
                conn.close()
        registro.close()
        gerenciamento.show()

    else:
        registro.close()
        gerenciamento.show()

def funcao_procurarcliente():
    gerenciamento.close()
    procurar.show()
    rg_cliente = procurar.lineRgPesquisar.text()
    
    if(rg_cliente != ""):
        conn = conectar_banco()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM clientes WHERE rg = ?", (rg_cliente,))
                cliente = cursor.fetchone()
                if cliente:
                    procurar.lineResultadoPesquisar.setText(
                            f"<html>"
                            f"<h3>Dados do Cliente</h3>"
                            f"<p><b>Nome:</b> {cliente[0]}</p>"
                            f"<p><b>RG:</b> {cliente[1]}</p>"
                            f"<p><b>Endereço:</b> {cliente[2]}</p>"
                            f"<p><b>Email:</b> {cliente[3]}</p>"
                            f"<p><b>Telefone:</b> {cliente[4]}</p>"
                            f"<p><b>Data de Nascimento:</b> {cliente[5]}</p>"
                            f"<p><b>Data da Compra:</b> {cliente[6]}</p>"
                            f"<p><b>Valor da Compra:</b> R$ {cliente[7]:.2f}</p>"
                            f"</html>"
                        )
                else:
                    procurar.lineResultadoPesquisar.setText("Cliente não encontrado.")
            except sqlite3.Error as e:
                procurar.lineResultadoPesquisar.setText(f"Erro ao acessar o banco de dados: {e}")
            finally:
                conn.close()

def funcao_editarcliente():
    gerenciamento.close()
    editar.show()
    editar.lineRgEditar.text()
    
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE rg = ?", (rg_cliente,))
        cliente = cursor.fetchone()

        if cliente:
            novo_nome = editar2.lineNomeEditar.text()
            novo_endereco = editar2.lineEnderecoEditar.text()
            novo_email = editar2.lineEmailEditar.text()
            novo_telefone = editar2.lineTelefoneEditar.text()

            try:
                cursor.execute("""
                    UPDATE clientes
                    SET nome = ?, endereco = ?, email = ?, telefone = ?
                    WHERE rg = ?
                """, (novo_nome, novo_endereco, novo_email, novo_telefone, rg_cliente))
                conn.commit()
                editar2.lineEditou.setText("Cliente atualizado com sucesso.")
            except sqlite3.Error as e:
                editar2.lineEditou.setText(f"Erro ao atualizar cliente: {e}")
            finally:
                conn.close()
        else:
            editar2.lineEditou.setText("Cliente não encontrado.")
            conn.close()
    
def funcao_excluircliente():
    gerenciamento.close()
    excluir.show()
    # rg_cliente = excluir.lineExcluirCliente.text()
    # print(rg_cliente)
    excluir.bConfirmar.clicked.connect(lambda: excluir_cliente(excluir.lineExcluirCliente.text()))

def excluir_cliente(rg_cliente):
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM clientes WHERE rg = ?', (rg_cliente,))
            conn.commit()
            str = f"Cliente excluído com sucesso! RG: {rg_cliente}"
            print(str)
            excluir.lineClienteExcluido.setText(str)
            
            # time.sleep(2)

        except sqlite3.Error as e:
            excluir.lineClienteExcluido.setText(f"Erro ao excluir cliente: {e}")
        finally:
            conn.close()


    # if excluir.bConfirmar.clicked.connect:
    #     excluir.lineClienteExcluido.setText('Cliente excluído!')

    


def tela_gereciamento():
    # login.close()
    procurar.close()
    gerenciamento.show()

def tela_registro():
    gerenciamento.close()
    registro.show()

def tela_registrar():#B voltar da tela de registro
    registro.close()
    gerenciamento.show()

def tela_editar_cliente():
    gerenciamento.close()
    editar.show()

def tela_editar_cliente_bvoltar():#B voltar da tela de editar cliente
    editar.close()
    gerenciamento.show()

def bcomfirmar_editar():    
   
    rg_cliente = editar.lineRgEditar.text()

    if(rg_cliente != ""):

        nomeCliente = ""
        enderecoCliente = ""
        rgCliente = ""
        telefoneCliente = ""
        emailCliente = ""
        dataNascCliente = ""
        dataCompraCliente = ""
        ValorCompraCliente = ""

        conn = conectar_banco()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM clientes WHERE rg = ?", (rg_cliente,))
                cliente = cursor.fetchone()
                if cliente:

                    nomeCliente = cliente[0]
                    rgCliente = cliente[1]
                    enderecoCliente = cliente[2]
                    emailCliente = cliente[3]
                    telefoneCliente = cliente[4]
                    dataNascCliente = cliente[5]
                    dataCompraCliente = cliente[6]
                    ValorCompraCliente = cliente[7]

                    
                    procurar.lineResultadoPesquisar.setText(f"Nome: {cliente[0]}\nRG: {cliente[1]}\nEndereço: {cliente[2]}\nEmail: {cliente[3]}\nTelefone: {cliente[4]}\n"
                        f"Data de Nascimento: {cliente[5]}\nData da Compra: {cliente[6]}\nValor da Compra: {cliente[7]}")
                else:
                    procurar.lineResultadoPesquisar.setText("Cliente não encontrado.")
            except sqlite3.Error as e:
                procurar.lineResultadoPesquisar.setText(f"Erro ao acessar o banco de dados: {e}")
            finally:
                conn.close()
        editar.close()
        editar2.show()


        editar2.lineEmailEditar.setText(emailCliente)
        editar2.lineNomeEditar.setText(nomeCliente)
        editar2.lineEnderecoEditar.setText(enderecoCliente)
        editar2.lineTelefoneEditar.setText(telefoneCliente)

        editar2.bEditarcliente.clicked.connect(lambda: editarCliente(rg_cliente))

   
def editarCliente(rg_cliente):
    editarEmail = editar2.lineEmailEditar.text()
    editarNome = editar2.lineNomeEditar.text()
    editarEndereco = editar2.lineEnderecoEditar.text()
    editarTelefone = editar2.lineTelefoneEditar.text()


    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        try:
           
            cursor.execute("""
                UPDATE clientes 
                SET nome = ?, email = ?, endereco = ?, telefone = ? 
                WHERE rg = ?
            """, (editarNome, editarEmail, editarEndereco, editarTelefone, rg_cliente))
            conn.commit()  
            editar2.lineEditou.setText("Cliente atualizado com sucesso!")
        except sqlite3.Error as e:
            editar2.lineEditou.setText(f"Erro ao acessar o banco de dados: {e}")
        finally:
            conn.close()

      
        editar2.close()
        gerenciamento.show()

    

# def editarCliente(editarEmail,editarNome,editarEndereco,editarTelefone,rg_cliente):
#     conn = conectar_banco()
#     if conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("UPDATE clientes SET nome = ?, email = ?, endereco = ?, telefone = ? WHERE rg = ?", (editarEmail,editarNome,editarEndereco,editarTelefone,rg_cliente))      
#         except sqlite3.Error as e:
#             procurar.lineResultadoPesquisar.setText(f"Erro ao acessar o banco de dados: {e}")
#         finally:
#             conn.close()

def bVoltarTelaEditar2():#B voltar da tela de editar cliente 2  
    editar2.close()
    editar.show()

def procurar_cliente():
    gerenciamento.close()
    procurar.show()
    
def voltar_tela_procurar():#B voltar da tela de procurar cliente
    procurar.close()
    gerenciamento.show()

# def funcao_excluircliente():
#     gerenciamento.close()
#     excluir.show()
    # if excluir.bConfirmar.clicked.connect:
    #     excluir.lineClienteExcluido.setText('Cliente excluído!')

def VoltarTelaBExcluir():#B voltar da tela de excluir cliente
    excluir.close()
    gerenciamento.show()

def listar_clientes():
    gerenciamento.close()
    
    listar.resultado.setRowCount(0)
    
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            
            if clientes:

                for row_number, cliente in enumerate(clientes):
                    listar.resultado.insertRow(row_number)  
                    
                    listar.resultado.setItem(row_number, 0, QTableWidgetItem(str(row_number + 1)))  
                    listar.resultado.setItem(row_number, 1, QTableWidgetItem(cliente[0]))  
                    listar.resultado.setItem(row_number, 2, QTableWidgetItem(cliente[1])) 
                    listar.resultado.setItem(row_number, 3, QTableWidgetItem(cliente[3]))  
                    listar.resultado.setItem(row_number, 4, QTableWidgetItem(cliente[2]))  
                    listar.resultado.setItem(row_number, 5, QTableWidgetItem(cliente[4])) 
            else:
                listar.resultado.setRowCount(1)
                listar.resultado.setItem(0, 0, QTableWidgetItem("Nenhum cliente cadastrado"))
        except sqlite3.Error as e:
            listar.resultado.setRowCount(1)
            listar.resultado.setItem(0, 0, QTableWidgetItem(f"Erro ao acessar o banco de dados: {e}"))
        finally:
            conn.close()

    listar.show()
    listar.bVoltarTelaEditar.clicked.connect(volta_listar_gerenciamento)

def volta_listar_gerenciamento():
    listar.close()
    gerenciamento.show()

app = QtWidgets.QApplication([])
login = uic.loadUi("login.ui")
registro = uic.loadUi("registro.ui")
gerenciamento = uic.loadUi("gerenciamento.ui")
procurar = uic.loadUi("procurarcliente.ui")
tela_registro_voltar = uic.loadUi("gerenciamento.ui")
tela_editar_cliente_voltar = uic.loadUi("gerenciamento.ui")
tela_editar_cliente2 = uic.loadUi("editar2.ui")
VoltarTelaEditar2 = uic.loadUi("editarcliente.ui")
tela_editar_cliente2_bvoltar = uic.loadUi("editarcliente.ui")
editar = uic.loadUi("editarcliente.ui")
editar2 = uic.loadUi("editar2.ui")
excluir = uic.loadUi("excluircliente.ui")
listar = uic.loadUi("listarClientes.ui")
tela_xcluir_Bvoltar = uic.loadUi("gerenciamento.ui")




login.bEnter.clicked.connect(funcao_login)
gerenciamento.bConfirmar1.clicked.connect(tela_registro)#esse botão abre a tela de registro
gerenciamento.bConfirmar2.clicked.connect(tela_editar_cliente)#esse botão abre a tela de editar cliente
gerenciamento.bConfirmar3.clicked.connect(procurar_cliente)#esse botão abre a tela de procurar cliente
gerenciamento.bConfirmar6.clicked.connect(tela_gereciamento)#esse botão abre a tela de gerenciamento que é a tela principal
gerenciamento.btnListarClientes.clicked.connect(listar_clientes)
registro.bRegistro.clicked.connect(funcao_registro)
procurar.bProcurar.clicked.connect(funcao_procurarcliente)
procurar.bVoltarTelaEditar.clicked.connect(tela_gereciamento)#essa volta para a tela de gerenciamento
registro.bVoltar.clicked.connect(tela_registrar)#essa volta para a tela de gerenciamento
editar.bVoltarTelaEditar.clicked.connect(tela_editar_cliente_bvoltar)#essa volta para a tela de editar cliente
editar.bProcurar.clicked.connect(bcomfirmar_editar)#essa abre a tela 2 de editar cliente
editar2.pushButton.clicked.connect(bVoltarTelaEditar2)#essa volta para a tela de editar cliente
gerenciamento.bConfirmar5.clicked.connect(funcao_excluircliente)#essa abre a tela de excluir cliente
excluir.bVoltarTelaExcluir.clicked.connect(VoltarTelaBExcluir)#essa volta para a tela de gerenciamento
excluir.bConfirmar.clicked.connect(funcao_excluircliente)



#excluir.bConfirmar.clicked.connect(funcao_excluircliente)



login.show()
# gerenciamento.show()

app.exec()


#registro.bConfirmar1.clicked.connect(funcao_registro) #vai coloar o cadadstrarClientes
#gerenciamento.bConfirmar3.clicked.connect(procurar_cliente)
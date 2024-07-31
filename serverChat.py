import socket
import threading 
import time

###########################################################################################################################################################################

def msgTreatment(conn, addr):

    cOnline.append(nome)

    mapa = {
            'conn': conn,
            'addr': addr,
            'nome': nome,
            'email': email,
            'last': 0
                    }
    
    novaListaOn[nome] = mapa

    print(f'\n[NOVA CONEXÃO] Usuário {nome}, de email {email}, se conectou pelo endereço {addr}\n')

    while True:

        try:

            msg = recvMsg()
            
            if msg:
                
                if msg == 'Chats privados':

                    print(f'[CHAT PRIVADO]>> o usuário {nome} escolheu a opção de "Chat privado"')

                    friend = recvMsg()

                    if friend in cOnline:

                        while True:

                            msgPriv = recvMsg()
                        
                            msgSeparada = msgPriv.split("=")
                            mensagem = msgSeparada[1]
                            mensagens.append(mensagem)

                            sendMsgPriv(msgPriv, friend)
                
                elif msg == 'Grupos':

                    print(f'[LISTA DE GRUPOS]>> o usuário {nome} escolheu a opção de "Grupos"')

                    msg = recvMsg()

                    if msg == 'Criar grupo':

                        criarGrupo()

                    elif msg != 'RETURN' or msg != 'Criar grupo':

                        nomeGrupo = msg

                        sendMsgGroup(nomeGrupo)

                elif msg == 'Criar grupo':
                    
                    criarGrupo()

                elif msg == 'Amigos':

                    amigo = recvMsg()

                    s.send(novaListaOn[amigo])

                elif msg.startswith('msg='):



                    msgSeparada = msg.split("=")
                    mensagem = msgSeparada[1]
                    mensagens.append(mensagem)
                    
                    sendMsgGroup()

        except:

            deleteClient()
            
            break

def criarGrupo():

    membros = []

    print(f'[CRIAR GRUPO]>> o usuário {nome} solicitou a criação de um grupo')

    membros.append(nome)

    evento = recvMsg()

    while evento != '-OK-' or evento != 'RETURN':

        membros.append(evento)

    if evento == '-OK-':

            evento2 = recvMsg()

            if evento2 != None:

                print(f'[GRUPO CRIADO]>> o usuário {nome} criou o grupo {evento2}')

                grupos[evento2] = membros

            else:

                print(f'[NOME DO GRUPO]>> insira o nome do grupo')

def sendMsgPriv(amigo):

    print(f'[ENVIANDO]>> Enviando mensagem particular para {amigo}')
    
    for i in range(novaListaOn['last'], len(mensagens)):
        
        msgEnvio = f"<{amigo}> "+mensagens[i]
        s.send(str(msgEnvio).encode())
        novaListaOn['last'] = i + 1
        time.sleep(0.2)

def sendMsgGroup(nomeGrupo):

    print(f'[ENVIANDO]>> {nome} está enviando mensagem para o grupo {nomeGrupo}')

def recvMsg():

    while True:

        try:

            msg = s.recv(2048).decode()

        except Exception:

            print('[ERRO]>> conexão com o cliente foi perdida')

            break

        return msg
    
def deleteClient(client):
    
    cOnline.remove(client)

###########################################################################################################################################################################

cOnline = []
grupos = {}
mensagens = []
novaListaOn = {}

host = 'localhost'
#O valor da porta é muito alto, pois o SO já utiliza as portas de valores baixo
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
    
print('[INICIANDO SOCKET]')

try:
    s.listen()

    print('[TENTATIVA DE CONEXÃO]>> Aguardando conexão de um cliente!')
            
except Exception:
            
    print('[ERRO]>> Erro ao tentar conectar um cliente.')
    time.sleep(5)
    exit()

while True:
            
        conn, addr = s.accept()

        nome, email = s.recv(1024).decode().split()

        print('[CONEXÃO BEM SUCEDIDA]>> Conectado em', addr)

        msgTreatment(conn, addr)

        thread = threading.Thread(target=msgTreatment, args=[conn, addr])
        thread.start()
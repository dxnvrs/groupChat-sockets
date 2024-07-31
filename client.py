###########################################################################################################################################################################
# import de dois dicionários feitos no arquivo 'serverChat.py'
#from serverChat import cOnline, grupos
import button

###########################################################################################################################################################################

# import da biblioteca responsável pela interface gráfica, PySimpleGUI
import PySimpleGUI as sg
from PySimpleGUI import *

###########################################################################################################################################################################

# import de bibliotecas para manipulação dos dados via socket com uso de threads 
import socket
from threading import Thread
import os
import time

###########################################################################################################################################################################
#                                                 ****************************************************************

#                                                 ~~~~ funções referentes a configuração da interface gráfica ~~~~ 

#                                                 ****************************************************************
###########################################################################################################################################################################

sg.theme('Dark Grey 14')

def windowA():
    layoutLeft = [[sg.Image(filename='iconMsn.png')],]
    layoutRight = [
           [sg.Text('Tela de Login')],
           [sg.Text('Nome: '), sg.Input(key='-NAME-')],
           [sg.Text('Email: '), sg.Input(key='-EMAIL-')],
           [Push(), 
            sg.Button('LOGIN'), 
            Push(), 
            sg.Button('CANCEL'), 
            Push()] ]
    
    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]
    
    return sg.Window('Tela de login', layout=layout, 
                     default_button_element_size=(8, 2))

def windowB():

    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')]]
    layoutRight = [
        [sg.Button('Chats privados')],
        [sg.Button('Grupos')],
        [sg.Button('Criar grupo')],
        [sg.Button('Amigos')]
    ]

    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Chat', layout=layout, 
                       default_button_element_size=(8, 2))
    while True:

        event, value = window.read()
        
        if event == sg.WIN_CLOSED:
            
            window.close()
            break
        
        elif event == 'Chats privados':

            sendMsg(event)

            window.close()
            window = privWindow()

        elif event == 'Grupos':

            sendMsg(event)

            if grupos == {}:

                window.close()
                window = windowNoGroup()
            
            else:
            
                window.close()
                window = windowGroup
        
        elif event == 'Criar grupo':
        
            sendMsg(event)

            window.close()
            window = windowCriarGrupo()
        
        elif event == 'Amigos':

            sendMsg(event)

            window.close()
            window = verPerfil()

        return window
        
def privWindow():

    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')],]
    layoutRight = [
        [sg.Text('Chats')],
        [sg.Listbox(values=cOnline, 
         enable_events=True, 
         size=(40,20), 
         key='-LIST-')],
        [sg.Button('RETURN')]
    ]
    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Chat', 
                     layout=layout, 
                     default_button_element_size=(8, 2))
    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:

            window.close()

            break

        elif event == '-LIST-':

            friend = values['LIST']
            window.close()

            sendMsg(friend)

            window = privChat(friend)

        elif event == 'RETURN':

            window.close()
            window = windowB()

    return window

def privChat(amigo):

    layout = [[sg.Text(f'{amigo}', size=(40, 1))],
        [sg.Output(size=(110, 30), font=('Helvetica 10'))],
        [sg.Button('', image_data=button.buttonClip, key='-ANEXO-'),
         sg.MLine(size=(60, 5), 
         enter_submits=True, 
         key='-QUERY-', 
         do_not_clear=False),
         sg.Button('SEND', bind_return_key=True),
         sg.Button('RETURN')]]

    window = sg.Window('Chat window', 
                       layout, 
                       font=('Helvetica', '13'), 
                       default_button_element_size=(8, 2))
    
    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()
            break
        
        elif event == 'SEND':

            msg = value['-QUERY-'].rstrip()

            print('<YOU> {}'.format(msg))

            msgPraMandar = 'msg='+msg
            
            sendMsg(msgPraMandar)
            
            msgRecebida = recvMsg()

            print(msgRecebida)

        elif event == 'RETURN':

            window.close()
            window = privWindow()

        return window
    
def windowNoGroup():

    layout = [[sg.Text('Você não está em nenhum grupo.')],
              [sg.Text('Crie um grupo e convide seus amigos!')],
              [sg.Button('Criar grupo')],
              [sg.Button('RETURN')]
    ]

    window = sg.Window('Grupos', 
                     layout, 
                     default_button_element_size=(8, 2))

    while True:
        event, value = window.read()
        
        if event == sg.WIN_CLOSED():
            
            window.close()

        elif event == 'Criar grupo':

            window.close()
            window = windowCriarGrupo()

        elif event == 'RETURN':

            window.close()
            window = windowB
        
        return window
    
def windowGroup():

    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')],]
    layoutRight = [[sg.Listbox(values=grupos, 
                    enable_events=True, 
                    size=(40,20),
                    key='-LIST-')],
                   [sg.Button('RETURN')]
    ]
    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Grupos', 
                     layout=layout, 
                     default_button_element_size=(8, 2))

    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()
        
        elif event == '-LIST-':

            grupoName = value['-LIST-']

            sendMsg(grupoName)

            window.close()
            window = grupo(grupoName)

        elif event == 'RETURN':

            window.close()
            window = windowB()

        return window

def grupo(nameGrupo):

    layout = [[sg.Text(f'{nameGrupo}', size=(40, 1))],
        [sg.Output(size=(110, 30), font=('Helvetica 10'))],
        [sg.Button('', image_data=button.buttonClip, key='-ANEXO-'),
         sg.MLine(size=(60, 5), 
         enter_submits=True, 
         key='-QUERY-', 
         do_not_clear=False),
         sg.Button('SEND', bind_return_key=True),
         sg.Button('RETURN')]]

    window = sg.Window('Group chat window', 
                       layout, 
                       font=('Helvetica', '13'), 
                       default_button_element_size=(8, 2))
    
    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()
            
            break
        
        elif event == 'SEND':

            msg = value['-QUERY-'].rstrip()
            print('<YOU>: {}'.format(msg))
            sendMsg(nameGrupo, msg)

        elif event == 'RETURN':

            window.close()
            window = windowGroup()

        return window

def windowCriarGrupo():
    
    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')]]
    layoutRight = [
        [sg.Text('Selecione os participantes do grupo')],
        [sg.Listbox(values=cOnline, 
         enable_events=True, 
         size=(40,20), 
         key='-LISTMEMBERS-')],
        [sg.Button('CONTINUE', key='-OK-'), 
         sg.Button('RETURN')]
    ]


    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Criar grupo', 
                       layout=layout, 
                       default_button_element_size=(8, 2))
    
    members.append('ADM-'+nomeUser)


    while True:

        event, value = window.read()

        client.send('ADM-'+nomeUser.encode())

        while event == '-LISTMEMBERS-':

            member = value['-LISTMEMBERS-']
            members = []
            members.append(member)
            
            sendMsg(member)
        
        if event == '-OK-':

            sendMsg(event)

            window.close()
            window = nomeGrupo()
        
        elif event == 'RETURN':

            sendMsg(event)

            window.close()
            window = windowB()
        
        return window

def nomeGrupo():

    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')]]
    layoutRight = [
        [sg.Text('Digite o nome do novo grupo:')],
        [sg.Input(key='-NOMEDOGRUPO-')],
        [sg.Button('CONTINUE', key='-OK-'), 
         sg.Button('RETURN')]
    ]
    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]
    
    window = sg.Window('Criar grupo',
                        layout=layout,
                        default_button_element_size=(8, 2))
    
    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()
            break

        elif event == 'RETURN':

            window.close()
            window = windowCriarGrupo()

        elif event == '-OK-':

            sendMsg(event)

            if value['-NOMEDOGRUPO-'] != None:

                gc = value['-NOMEDOGRUPO-']

                sendMsg(gc)

                window.close()
                window = grupo(gc)
            
            else:

                print('Insira o nome do grupo!')

        return window

def verPerfil():
    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')],]
    layoutRight = [[sg.Listbox(values=cOnline, 
                    enable_events=True, 
                    size=(40,20),
                    key='-FRIENDLIST-')],
                   [sg.Button('RETURN')]
    ]
    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Amigos', 
                     layout=layout, 
                     default_button_element_size=(8, 2))

    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()
        
        elif event == '-FRIENDLIST-':

            amigo = value['-FRIENDLIST-']

            sendMsg(amigo)

            window.close()
            window = perfil(amigo) 

        elif event == 'RETURN':

            window.close()
            window = windowB()

        return window

def perfil(friend):

    infoFriend = recvMsg()

    layoutLeft = [[sg.Image(filename='iconMsnMenor.png')],]
    layoutRight = [[sg.Text(friend, size=(40,20))],
                   [sg.Text(f'Email: {infoFriend['email']}')],
                   [sg.Text(f'Addr: {infoFriend['addr']}')],
                   [sg.Text(f'Conn: {infoFriend['conn']}')],
                   [sg.Button('RETURN')]
    ]

    layout = [
        [Column(layoutLeft),
        VSeparator(),
        Column(layoutRight)]
        ]

    window = sg.Window('Amigos', 
                     layout=layout, 
                     default_button_element_size=(8, 2))

    while True:

        event, value = window.read()

        if event == sg.WIN_CLOSED():

            window.close()

        elif event == 'RETURN':

            window.close()
            window = verPerfil()
###########################################################################################################################################################################
#                                                   ***********************************************************

#                                                   ~~~~ funções referentes a comunicação cliente-servidor ~~~~ 

#                                                   ***********************************************************
###########################################################################################################################################################################

# função que permite que o cliente receba mensagens de outros clientes com interceptação do servidor
def recvMsg():
    
    while True:
        try:

            msg = client.recv(2048).decode()

            if msg:
               
               print(msg)

               if msg.startswith('Arq'):
                   
                    filename = msg.split(': ')[-1]
                    filedata = client.recv(1024)

                    with open(filename, 'wb') as f:
                       
                       f.write(filedata)

                    print(f'Arquivo {filename} recebido')
            
            else:
               
                break

        except:

            client.close()
            print('\n[ERRO]>> conexão perdida\n')
            break
        
        return msg

# função que permite que o cliente envie informações para o servidor
def sendMsg(msg):

    while True:

        try:
            
            client.send(str(msg).encode())

        except:
            
            print('\n[ERRO]>> não foi possível enviar a mensagem\n')

            break

###########################################################################################################################################################################

nomeUser = ''
emailUser = ''
msg = ''

# endereço de ip e port são instanciados;
# '0.0.0.0' foi escolhido como endereço de ip, pois assim serão aceitas conexões com qualquer um dos ips associados a máquina
# 50000 foi escolhido como porta para não dar conflito com as portas já utilizadas na máquina, que geralmente são as de menor valor
host = 'localhost'
port = 50000

# socket do cliente é requisitado e armazenado, especificando a 
# família de endereço (IPv4, 'AF_INET') e o protocolo de transporte (TCP, 'SOCK_STREAM')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# aqui tenta-se iniciar a conexão do cliente com o servidor
# caso o servidor não esteja disponível, uma mensagem é printada na tela e o cliente é terminado
try:
    
    client.connect((host, port))
    print('\n[CONECTADO]>> o cliente está conectado\n')

except Exception:

    print('\n[ERRO]>> não foi possível conectar o host, pois o servidor está offline.\n')
    time.sleep(5)
    exit()

# no caso de sucesso de conexão do cliente, a janela de login é aberta
window = windowA()

# main event loop
while True:

    # as threads referentes às principais funções são instanciadas e iniciadas
    process1 = Thread(target=recvMsg, args=[])
    process2 = Thread(target=sendMsg, args=[msg])
    #process3 = Thread(target=windowA)

    process1.start()
    process2.start()
    #process3.start()

    # informações obtidas da página de login são coletadas
    event, value = window.read()

    # se a última interação com a página tiver sido um clique no 'x' da janela, 
    # então essa série de validações por 'if' é parada e consequentemente o programa para e a janela é fechada
    if event == sg.WIN_CLOSED or event == 'CANCEL':
        
        break
    
    # se a última interação com a página tiver sido um clique no botão 'LOGIN', então as informações 
    # obtidas nos textfields são armazenadas em 2 variáveis e uma nova janela é aberta enquanto
    # a de login é encerrada
    elif event == 'LOGIN':
        
        nomeUser = str(value['-NAME-']).encode()
        emailUser = str(value['-EMAIL-']).encode()

        tudo = nomeUser+emailUser
        client.send(tudo)
        #print(nomeUser)
        #client.send(emailUser)
        #print(emailUser)

        print(f'\n[CONEXÃO BEM SUCEDIDA]>> usuário {nomeUser}, de email {emailUser}, está conectado\n')

        cOnline = recvMsg()
        grupos = recvMsg()

        window.close()
        window = windowB() 

window.close()
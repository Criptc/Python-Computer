import socket
import threading
from time import sleep

global Memory, Storage, StoragePostion, MemoryPostion, time, Register
Memory = ['!' for x in range(1000)]
Storage = [0 for x in range(1000000)]
Register = [[0 for x in range(50)] for x in range(2)]
MemoryPostion = 0
time = 0

def Clock():
    while True:
        sleep(0.1)
        global time
        time = round(time + 0.1, 1)

def asciiit(var):
	out=''
	for i in range(len(var)):
		il=i+1
		if out!='':out=out+'~'+str(ord(str(var[i:il])))
		else:out=str(ord(str(var[i:il])))
	return out

def unasciiit(var):
	out='';var=var.split('~')
	for i in range(len(var)):il=i+1;out=out+str(chr(int(''.join(var[i:il]))))
	return out

def StoreMemory(data, StartAddress):
    global MemoryPostion, Memory
    for i in data:
        MemoryPostion = MemoryPostion + 1
        letter = '0x' + asciiit(i)
        Memory[MemoryPostion] = letter
    EndAddress = MemoryPostion
    return '0x' + str(StartAddress), '0x' + str(EndAddress)

def ReadMemory(StartAddress, EndAddress):
    StartAddress = int(StartAddress.replace('0x', ''))
    EndAddress = int(EndAddress.replace('0x', ''))
    global Memory 
    Output = ''
    try:
        for i in range(EndAddress - StartAddress + 1):
            Output = Output + unasciiit(Memory[StartAddress + i].replace('0x', ''))
    except:
        DumpMemory()
        raise Exception('Unassined memory accessed')
    return Output

def StoreStorage(Postion, Data):
    global Storage
    Postion = int(Postion.replace('0x', ''))
    Storage[Postion] = Data

def ReadStorage(Postion):
    global Storage
    Postion = int(Postion.replace('0x', ''))
    return Storage[Postion]

def DumpMemory():
    global Memory
    mem = Memory = [str(x) for x in Memory]
    data = ''.join(mem)
    data = data.replace('0x', ' ')
    data = data.replace('!', '')
    print(f'dumping {len(data)} bits of memory')
    print(data)

def CPU(instructions):
    i = instructions
    global Register
    if 'pt ass ' in i:
        i = i.replace('pt ass ', '')
        i = i.split('0x')
        A = ''.join(i[:1])
        B = ''.join(i[1:2])
        StoreStorage(B, A)
    elif 'pt sad ' in i:
        i = i.replace('pt sad ', '')
        i = i.split('0x')
        a = ''.join(i[:1])
        b = ''.join(i[1:2])
        A, B = StoreMemory(a, b)
        print(A, B)
    elif 'rd ass ' in i:
        i = i.replace('rd ass ', '')
        Data = ReadStorage(i)
        print(Data)
    elif 'rd sad ' in i:
        i = i.replace('rd sad ', '')
        i = i.split(' ')
        Start = ''.join(i[:1])
        End = ''.join(i[1:2])
        print(ReadMemory(Start, End))
    elif i == 'time':
        global time
        print(time)
    elif i == 'dmp sad':
        DumpMemory()
    elif i == 'exit':
        while True: exit(0)
    else:
        print(f'Error: unknow command {i}')
        exit(1)
TimeThread = threading.Thread(target=Clock)
TimeThread.start()

while True:
    inp = input('\\\\:')
    CPU(inp)


                                                                                                                                                                                                                                                                                                                              
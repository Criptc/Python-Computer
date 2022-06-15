import socket
import threading
from time import sleep, time as tim

global Memory, Storage, MemoryPostion, time, Register, End
Memory = ['~' for x in range(1000)]
Storage = ['~' for x in range(10000)]
Register = [['~' for x in range(50)] for x in range(2)]
MemoryPostion = 0
time = 0
End = False

def Clock():
    while True:
        sleep(0.1)
        global time, End
        if End:
            break
        time = round(time + 0.1, 1)

def TimeClock():
    while True:
        sleep(1)
        global End
        if End:
            break
        clck = round(tim()) + 436117077146035980
        StoreStorage('0x3', clck, System=True)

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

def StoreMemory(data):
    global MemoryPostion, Memory
    StartAddress = MemoryPostion + 1
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
        raise Exception('Unassined memory accessed')
    return Output

def StoreStorage(Postion, Data, System = False):
    global Storage
    Postion = int(Postion.replace('0x', ''))
    if System:
        Storage[Postion] = Data
    else:
        if Postion <= 4:
            print(f'Error: postions 0x0 through 0x5 reserved for system. Postion: {Postion}')
        else:
            Storage[Postion] = Data

def ReadStorage(Postion):
    global Storage
    Postion = int(Postion.replace('0x', ''))
    return Storage[Postion]

def DumpRegisters():
    global Register
    RegisterData = ' '.join(Register).replace('~', '').replace('  ', '')
    StoreStorage('0x0', RegisterData, System=True)
    Register = ['~' for x in range(8)]

def DumpMemory():
    global Memory
    MemoryData = ' '.join(Memory).replace('~', '').replace('  ', '')
    StoreStorage('0x1', MemoryData, System=True)
    Memory = ['~' for x in range(200)]

def DumpStorage():
    global Storage
    data = ' '.join(Storage)
    data = data.replace('~', ' ')
    data = data.replace('  ', '')
    Storage = ['~' for x in range(10000)]
    if data == '':
        StoreStorage('0x2', '~', System=True)
    else:
        StoreStorage('0x2', data, System=True)

def GPU(Data):
    print(Data)

def ALU(operand, Data):
    def add(Data):
        Data = Data.split(' ')
        a = ''.join(Data[:1])
        b = ''.join(Data[1:2])
        try:
            a = int(a)
            b = int(b)
        except:
            raise Exception(f'Data must be a number, not "{Data}"')
        return a + b
        
    
    def subtract(Data):
        Data = Data.split(' ')
        a = ''.join(Data[:1])
        b = ''.join(Data[1:2])
        try:
            a = int(a)
            b = int(b)
        except:
            raise Exception(f'Data must be a number, not "{Data}"')
        return a - b
    
    def And(Data):
        Data = Data.split(' ')
        a = ''.join(Data[:1])
        b = ''.join(Data[1:2])
        if a == b:
            return '1'
        else:
            return '0'
    
    def Or(Data):
        if 'str' in str(type(Data)):
            Data = Data.split(' ')
            a = ''.join(Data[:1])
            b = ''.join(Data[1:2])
            if a == '1':
                if b == '0':
                    return '1'
                else:
                    return '1'
            elif a == '0':
                if b == '1':
                    return '1'
                else:
                    return '0'
        else:
            raise Exception(f'Error: not type must be str not "{(str(type(Data)))}"')
    
    def Not(Data):
        if 'str' in str(type(Data)):
            if Data == '1':
                return '0'
            elif Data == '0':
                return '1'
            else:
                raise Exception(f'Error: must be 1 or 0, not "{Data}"')
        else:
            raise Exception(f'Error: not type must be str not "{(str(type(Data)))}"')
        
    def xor(Data):
        if 'str' in str(type(Data)):
            Data = Data.split(' ')
            a = ''.join(Data[:1])
            b = ''.join(Data[1:2])
            if a == '1':
                if b == '0':
                    return '1'
                else:
                    return '0'
            elif a == '0':
                if b == '1':
                    return '1'
                else:
                    return '0'
        else:
            raise Exception(f'Error: not type must be str not "{(str(type(Data)))}"')
    
    if operand.lower() == 'add' or operand == '+':
        return add(Data)
    elif operand.lower() == 'subtract' or operand == '-':
        return subtract(Data)
    elif operand.lower() == 'and':
        return And(Data)
    elif operand.lower() == 'or':
        return Or(Data)
    elif operand.lower() == 'not':
        return Not(Data)
    elif operand.lower() == 'xor':
        return xor(Data)
    elif operand.lower() == 'nand':
        return Not(And(Data))
    elif operand.lower() == 'nor':
        return Not(Or(Data))

def Random():
    first = True
    RandomNumbers = []
    while True:
        if not first:
            if random(0, 4) == 2:
                break
        RandomNumbers += str(random(random(0, 3), random(10, 100)))
        if first:
            first = False
    return str(choice(RandomNumbers))

def RandomBool():
    a = Random()
    b = Random()
    c = ALU('add', a + ' ' + b)
    d = ALU('subtract', str(c) + ' ' + str(Random()))
    if d % 2:
        return '0'
    else:
        return '1'

def schedule(function, time, argument = ''):
    argument = list(argument)
    time = int(time)
    if '' in argument: argument.remove('')
    while True:
        sleep(0.5)
        if int(ReadStorage('0x3')) >= time:
            if argument == ['']:
                function()
            else:
                if len(argument) == 1:
                    function(argument.pop(0))
                    break
                elif len(argument) == 2:
                    function(argument.pop(0), argument.pop(0))
                    break
                break

def Compiler(Data):
    if 'mov ' in Data:
        Data = Data.replace('mov ', '')
        if ' in ' in Data:
            Data = Data.replace(' in ', '~')
        if ', ssa' in Data:
            Data = Data.replace(', ssa', '').split('~')
            Postion = ''.join(Data[1:2])
            Data = ''.join(Data[:1])
            StoreStorage(Postion, Data)

ClockThread = threading.Thread(target=Clock)
TimeClockThread = threading.Thread(target=TimeClock)
ClockThread.start()
TimeClockThread.start()
sleep(2)



'''
#scheduler Test
Tim = ReadStorage('0x3')
GPU(Tim)
schedule(StoreStorage, int(Tim) + 3, argument = ('0x5', 'test'))
sleep(5)
ReadStorage('0x5')
sleep(0.2)
End = True
'''


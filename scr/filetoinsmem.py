def _regstrtoregnum(regstr:str)->int:
    regnum = {}
    regnum['$0'] = 0
    regnum['$zero']=0
    regnum['$at'] = 1
    regnum['$v0'] = 2
    regnum['$v1'] = 3
    regnum['$a0'] = 4
    regnum['$a1'] = 5
    regnum['$a2'] = 6
    regnum['$a3'] = 7
    regnum['$t0'] = 8
    regnum['$t1'] = 9
    regnum['$t2'] = 10
    regnum['$t3'] = 11
    regnum['$t4'] = 12
    regnum['$t5'] = 13
    regnum['$t6'] = 14
    regnum['$t7'] = 15
    regnum['$s0'] = 16
    regnum['$s1'] = 17
    regnum['$s2'] = 18
    regnum['$s3'] = 19
    regnum['$s4'] = 20
    regnum['$s5'] = 21
    regnum['$s6'] = 22
    regnum['$s7'] = 23
    regnum['$t8'] = 24
    regnum['$t9'] = 25
    regnum['$k0'] = 26
    regnum['$k1'] = 27
    regnum['$gp'] = 28
    regnum['$sp'] = 29
    regnum['$fp'] = 30
    regnum['$ra'] = 31
    return regnum[regstr]
def _analyseIns(ins:str)->{}:
    res={}
    res['label']=None
    if(ins.find(':')!=-1):
        res['label']=ins.strip(':')
        return res
    elif(ins=='syscall'):
        res['label']='syscall'
        return res
    res['op']=ins.split()[0]
    operands=ins.split()[1].split(',')
    if(res['op']=='add'):
        res['rs']=operands[1]
        res['rt']=operands[2]
        res['rd']=operands[0]
        res['imm']=None
    elif(res['op']=='addi'):
        res['rs'] =operands[1]
        res['rt'] =None
        res['rd'] =operands[0]
        res['imm'] =operands[2]
    elif (res['op'] == 'beq'):
        res['rs'] =operands[0]
        res['rt'] =operands[1]
        res['rd'] =None
        res['imm'] =operands[2]
    elif (res['op'] == 'bne'):
        res['rs'] =operands[0]
        res['rt'] =operands[1]
        res['rd'] =None
        res['imm'] =operands[2]
    elif (res['op'] == 'lw'):
        imm=operands[1].split('(')[0]
        regbase=operands[1].split('(')[1].split(')')[0]
        res['rs'] =regbase
        res['rt'] =None
        res['rd'] =operands[0]
        res['imm'] =imm
    elif (res['op'] == 'sw'):
        imm=operands[1].split('(')[0]
        regbase=operands[1].split('(')[1].split(')')[0]
        res['rs'] =regbase
        res['rt'] =operands[0]
        res['rd'] =None
        res['imm'] =imm
    elif (res['op'] == 'slt'):
        res['rs'] =operands[1]
        res['rt'] =operands[2]
        res['rd'] =operands[0]
        res['imm'] =None
    elif (res['op'] == 'syscall'):
        res['rs'] =None
        res['rt'] =None
        res['rd'] =None
        res['imm'] =None
    return res
class Instruction:
    def __init__(self, res:{}):
        self.op=res['op']
        self.rs=res['rs']
        self.rt=res['rt']
        self.rd=res['rd']
        self.imm=res['imm']
def getInsmem(filename)->[]:
    assembler_file=open(filename,'r')
    i=0
    labelcnt=0
    labeltable={}
    inslist=[]
    for code_line in assembler_file.readlines():
        i+=1
        ins=_analyseIns(code_line.strip().strip())
        #print(ins)
        if(ins['label']):
            labelcnt+=1
            labeltable[ins['label']]=i+1-labelcnt
        else:
            inslist.append(ins)
    for ins in inslist:
        ins.pop('label')
        if(ins['op']=='bne' or ins['op']=='beq'):
            ins['imm']=int(labeltable[ins['imm']])
            if(ins['rs']):
                ins['rs']=_regstrtoregnum(ins['rs'])
            if(ins['rt']):
                ins['rt']=_regstrtoregnum(ins['rt'])
            if(ins['rd']):
                ins['rd']=_regstrtoregnum(ins['rd'])
        else:
            if(ins['rs']):
                ins['rs']=_regstrtoregnum(ins['rs'])
            if(ins['rt']):
                ins['rt']=_regstrtoregnum(ins['rt'])
            if(ins['rd']):
                ins['rd']=_regstrtoregnum(ins['rd'])
            if(ins['imm']):
                ins['imm']=int(ins['imm'])
    print(inslist)
    return inslist



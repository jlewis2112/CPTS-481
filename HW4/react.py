"""
Joseph Lewis
HW 4
nuclear physics
module
"""

"""
needed code for the previous quiz. 
"""

class Particle:

    def __init__(self, sym, chg, massNumber):
        self.sym = sym
        self.chg = chg
        self.massNumber = massNumber

    def __str__(self):
        return self.sym
        
    def __repr__(self):
        className = self.__class__.__name__
        return "{className}({self.sym!r}, {self.chg!r}, {self.massNumber!r})"
 
 #particle extension part       
    def __add__(self, other):
        return (self, other)
        
    def __radd__(self, other):
        return (other, self)
        
class Nucleus(Particle):
    def __str__(self):
        return "({}){}".format(self.massNumber, self.sym)
        
em = Particle("e-", -1, 0)
ep = Particle("e+", 1, 0)
p = Particle("p", 1, 1)
n = Particle("n", 0, 1)
nu_e = Particle("nu_e", 0, 0)
gamma = Particle("gamma", 0, 0)

d = Nucleus("H", 1, 2)
li6 = Nucleus("Li", 3, 6)
he4 = Nucleus("He", 2, 4)

"""
exception code
"""

class unbalancedCharge(Exception):
    def __init__(self, diff):
        print("unbalanced charge error: ", diff)
        
class unbalancedNumber(Exception):
    def __init__(self, diff):
        print("unbalanced massNumbers error: ", diff)

"""
Reaction Class
"""
class Reaction:
    def __init__(self, left, right):
        self.ls = left
        self.rs = right
        self.unbalanced()
    
    def unbalanced(self):
        lc = 0 #left right charge
        rc = 0
        lm = 0 #left right mass
        rm = 0
        if(isinstance(self.ls, Particle)):
            lc = self.ls.chg
            lm = self.ls.massNumber
        else:
            for x in self.ls:
                lc += x.chg
                lm += x.massNumber
        if(isinstance(self.rs, Particle)):
            rc = self.rs.chg
            rm = self.rs.massNumber
        else:
            for x in self.rs:
                rc += x.chg
                rm += x.massNumber
        diff = abs(lc - rc)
        if diff != 0:
            raise unbalancedCharge(diff)
        diff = abs(lm - rm)
        if diff != 0:
            raise unbalancedNumber(diff)

    def __str__(self):
        result = ""
        if(isinstance(self.ls, Particle)):
            if self.ls.massNumber > 1:
                result = result + "(" + str(self.ls.massNumber) + ")" + str(self.ls.sym) + "-> "
            else:
                result = result + str(self.ls.sym) + "-> "
        else:
            for x in self.ls:
                if x.massNumber > 1:
                    result = result + "(" + str(x.massNumber) + ")" + str(x.sym) + " + "
                else:
                    result = result + str(x.sym) + " + "
            result = result[0:-2] + "-> "
        if(isinstance(self.rs, Particle)):
            if self.ls.massNumber > 1:
                result = result + "(" + str(self.ls.massNumber) + ")" + str(self.ls.sym)
            else:
                result = result + str(self.ls.sym)
        else:
            for x in self.rs:
                if x.massNumber > 1:
                    result = result + "(" + str(x.massNumber) + ")" + str(x.sym) + " + "
                else:
                    result = result + str(x.sym) + " + "
            result = result[0:-3]
        return result


"""
chain reaction Class
"""
  
class ChainReaction():

    def __init__(self, name):
        self.name = name
        self.chain = []
        self.net = ""
        
        
    def addReaction(self, reaction):
        netL = [] #left side matter
        netR = [] #right side matter
        self.chain.append(reaction)
        for x in self.chain:
            if(isinstance(x.ls, Particle)):
                netL.append(x.ls)
            else:
                for y in x.ls:
                    netL.append(y)
        for x in self.chain:
            if(isinstance(x.rs, Particle)):
                netR.append(x.rs)
            else:
                for y in x.rs:
                    netR.append(y)
                    
        for lsx in netL:
            if lsx in netR:
                netL.remove(lsx)
                netR.remove(lsx)
        for rsx in netR:
            if rsx in netL:
                netL.remove(rsx)
                netR.remove(rsx)
                
        netReact = ""
        for net in netL:
            netReact = netReact + net.__str__() + " + "
        netReact = netReact[0:-2] + "-> "
        for net in netR:
            netReact = netReact + net.__str__() + " + "
        netReact = netReact[0:-3]
        self.net = netReact
        
        
    def __str__(self):
        result = self.name + " chain: \n"
        for react in self.chain:
        	result = result + react.__str__() + "\n"
        result = result + "net:\n" + self.net
        return result
    
                
        


#for test purposes     
    
if __name__ == '__main__':
    print("test 1 ", Reaction((li6, d), (he4, he4)))#test reaction class
    print("test 1b ", Reaction(li6 + d, he4 + he4))
    
    try:
        print(Reaction((p,d) , (he4, he4)))
    except unbalancedCharge:
        print("test 2 charge error caught")    
    try:
        print(Reaction(p,d),(he4, he4))
    except unbalancedNumber:
        print("Test 3 mass error caught")
        
    print("chain reaction test")
    he3 = Nucleus("He", 2, 3)
    chnPP = ChainReaction( " proton - proton (branch I) ")
    for rctn in (Reaction((p, p) , (d, ep, nu_e)),
                 Reaction(( p, p ) , (d , ep, nu_e )),
                 Reaction(( d, p ) , (he3, gamma)),
                 Reaction(( d, p ) , (he3, gamma)),
                 Reaction(( he3, he3) , (he4 , p , p))): 
        chnPP.addReaction(rctn)
    print(chnPP)
              


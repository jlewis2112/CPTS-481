
"""
Joseph Lewis
HW3 Roman Numeral Module
"""




numerals = [(1000000,"(M)"),(900000,"(C)(M)"), (500000,"(D)"),(400000,"(C)(D)"),(100000,"(C)"), (90000,"(X)(C)"), (50000,"(L)"), (40000, "(X)(L)"), (10000,"(X)"), (9000,"(I)(X)"), (5000, "(V)"), (4000, "M(V)"), (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]

class Roman:
    number = None #string roman numeral number
    intValue = None #int value of the numeral
    
    #constructor
    def __init__(self, num):
        if(isinstance(num, int)):
            if(num > 2000000):
                raise ValueError("ValueError, value over 2000000")  
            else: 
                self.intValue = num
                self.setNumeral(num)
        else:
            raise ValueError("ValueError, input needs to be an int")
    
    #used to set the numeral integer    
    def setNumeral(self, num):
        result = ""
        if num == 0:
            self.number = 'N'
            return
        elif num < 0:
            result = "-"
            num = -num
        num2 = num
        while num2 >= 1:
            for intx, numx in numerals:
                while num2 >= intx:
                     result = result + numx
                     num2 -= intx
        self.number = result
        
    def __str__(self):
        return str(self.number)
        
    def __repr__(self):
        return "Roman("+str(self.intValue)+")"
        
#arthmetic operations *****************************
        
    def __add__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue + next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue + next)
        
    def __radd__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue + next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue + next)
            
    def __sub__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue - next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue - next)
            
    def __mul__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue * next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue * next)
 
    def __rmul__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue * next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue * next) 
            
    def __truediv__(self, next):
        if(isinstance(next, Roman)):
            return (Roman(self.intValue // next.intValue), Roman(self.intValue % next.intValue))
        elif(isinstance(other, int)):
            (Roman(self.intValue // next), Roman(self.intValue % next))  
            
    def __floordiv__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue // next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue // next)
            
    def __pow__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue ** next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue ** next)
            
    def __rpow__(self, next):
        if(isinstance(next, Roman)):
            return Roman(self.intValue ** next.intValue)
        elif(isinstance(other, int)):
            return Roman(self.intValue ** next)
            
    def __eq__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue == next.intValue
        elif(isinstance(other, int)):
            return self.intValue == next
            
    def __ne__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue != next.intValue
        elif(isinstance(other, int)):
            return self.intValue != next
            
    def __lt__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue < next.intValue
        elif(isinstance(other, int)):
            return self.intValue < next
            
    def __le__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue <= next.intValue
        elif(isinstance(other, int)):
            return self.intValue <= next
            
    def __gt__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue > next.intValue
        elif(isinstance(other, int)):
            return self.intValue > next
            
    def __ge__(self, next):
        if(isinstance(next, Roman)):
            return self.intValue >= next.intValue
        elif(isinstance(other, int)):
            return self.intValue >= next
            
    def __neg__(self):
        return Roman(-self.intValue)

#create the global variables        
for a in range(1001):
    valuex = Roman(a).number
    globals()[valuex] = Roman(a)

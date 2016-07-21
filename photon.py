#from pithy import *



import json
from pylab import *
from commands import getoutput as go
class photon:
    """A particle object belongs to a class developed to help you communicate to your photon in the wild. Each photon has two attributes that it needs to work.

    Attributes:
        name: A string representing the name of the Photon you wish to communicate with. Your photon ID would also suffice. Note that it is case sensitive.
        access: This is your Particle account access token passed as a string. This is necessary to access your functions and prevents people from abusing your Photon.
    
    Functions:
        getDevices(): Returns the devices associated with the access token
        getConnection(): Returns whether the device of the same name is connected to the internet
        getFunctions():Returns the functions known by the Photon. Functions can be accessed with push()
        getVariables(): Returns the variables known to the Photon. Variables can be accessed 
        fetch(String variable): Returns the value associated with a given variable name
        push(String variable,String argument):Executes the particular funciton with a given String argument
        
        
    Your Particle Photon code will look something like this:
    
        double var1;
        int var2;
        void setup()
        {
        ...
            Particle.function("PithyName1",function2Execute);
            Particle.function("PithyName2",function3Execute);
            Particle.variable("PithyName3",var1);
            Particle.variable("PithyName4",var2);
        ...
        }
        
        void loop()
        {
        ...
        }
        
        int funcion2Execute(String args)
        {
        ...
        }
        int funcion3Execute(String args)
        {
        ...
        }
        
    """
    def __init__(self, name, access):
        """Return a particle object whose name is *name* and access token is *access*"""
        self.access = access
        self.name = name
        
    def getDevices(self):
        """Returns the status of any and every device attached to your Particle account. This s handy for finding out if your Photon/Cores are connected to the internet"""
        self.devices = self.cmd("")
        for i in range(size(self.devices)):
            if(self.devices[i]['connected']==True):
                print "%s is connected" %self.devices[i]['name']
            else:
                print "%s is not connected" %self.devices[i]['name']
        return json.dumps(self.devices, sort_keys=True, indent=4, separators=(',', ': '))
        
    def getConnection(self):
        """Returns the status of any and every device attached to your Particle account. This s handy for finding out if your Photon/Cores are connected to the internet"""
        self.devices = self.cmd("")
        for i in range(size(self.devices)):
            if(self.devices[i]['name']==self.name):
                if(self.devices[i]['connected']==True):
                    return True
                else:
                    return False
        return False
        #return self.devices
        
    def getFunctions(self):
        """Returns the functions of the device correspoding to the Photon of the same name. This is handy for knowing what functions the Photon is able to execute.
        E.G.
        
        If you Photon code contains the following lines in setup():          
        
        Particle.function("PithyName1",function2Execute);
        Particle.function("PithyName2",function3Execute);
        
        Then calling getFunctions() in pithy will return
        
        PithyName1
        PithyName2
        """
        self.functions = self.cmd("/%s/"%self.name)
        return json.dumps(self.functions['functions'], sort_keys=True, indent=4, separators=(',', ': '))
        #return self.functions['functions']
        
    def getVariables(self):
        """Returns the name and types of variables for the device correspoding to the Photon of the same name. This is handy for knowing what variables the Photon is able to return.
        E.G.
        
        If you Photon code contains the following lines:
        double var1;
        int var2;
        
        Particle.variable("PithyName3",var1);
        Particle.variable("PithyName4",var2);
        
        Then calling getVariables() in pithy will return
        
        PithyName3: double
        PithyName4: int
        """        
        self.functions = self.cmd("/%s/" %self.name)
        return json.dumps(self.functions['variables'], sort_keys=True, indent=4, separators=(',', ': '))
        #return self.functions['variables']
        
    def cmd(self,cmd,params=None):
        """Simple helper function to access the internet. You should not need to call this function ever, ever ,ever. When you instantiate a particle object, all of the particle functions and variables you wish to access are pushed to specific websites on the Particle servers. This class accesses that data by creating a website and passing your id and access token """
        base = "https://api.particle.io/v1/devices"
        cmder = "curl -s %s%s -H 'Authorization: Bearer %s'" %(base,cmd,self.access)
        if params != None:
            cmder += " -d args=%s" % params
        out = go(cmder)
        return json.loads(out)

    def fetch(self,var):
        """Returns the value associated with the given Particle variable.
        E.G.
        
        If you Photon code contains the following lines:
        double var1;
        int var2;
        
        Particle.variable("PithyName3",var1);
        Particle.variable("PithyName4",var2);
        

        If you call fetch("PithyName3") then the function will return the value associated with var1
        """   
        return self.cmd("/%s/%s/" % (self.name,var))['result']
        
    def push(self,var,val):
        """Executes the function associated with the given Particle variable.
        E.G.
        
        If you Photon code contains the following lines:
        Particle.function("PithyName1",function2Execute);
        Particle.function("PithyName2",function3Execute);
        
        int funcion2Execute(String args)
        {
        ...
        }
        int funcion3Execute(String args)
        {
        ...
        }
        

        If you call push("PithyName1","strArg") then the code will send the String argument *strArg* to the particle server and tell the Photon to execute the function *function2Execute* using the argument *strArgs*.
        """  
        return self.cmd("/%s/%s/" % (self.name,var),params = val)['return_value']
    
    def flash(self,file=None):
        if file == None:
            return "Empty File"
        elif go("ls files").find(file) == -1:
            return "No Such File"
        base = "https://api.particle.io/v1/devices/%s" %(self.name)
        cmder = "curl -s -X PUT -F file=@files/%s %s -H 'Authorization: Bearer %s'" %(file,base,self.access)
        out = go(cmder)
        if(json.loads(out)['ok']):
            return json.loads(out)['message']
        else:
            return json.loads(out)['output']
        
        
    def move(self,angle):
        return self.push('move',angle)
        
    def attachServo(self,pin):
        return self.push('attachServo',pin)
    
    def getPin(self,pin):
        return self.push('getPin',pin)
    
    def attachServo(self):
        return self.push('attachServo','')
        
    def setInput(self,pin):
        temp = self.fetch('String2')
        temp = temp.split(',')
        if int(unicode(temp[self.getPin(pin)])) == -1:
            return self.push('setInput',pin)
        return -1
    
    def setOutput(self,pin):
        temp = self.fetch('String2')
        temp = temp.split(',')
        if int(unicode(temp[self.getPin(pin)])) == -1:
            return self.push('setOutput',pin)
        return -1
        
    def getPinMode(self,pin):
        t = self.push('setOutput',pin)    
        if t == 1:
            print 'INPUT'
        elif t==0:
            print 'OUTPUT'
    
    def analogRead(self,pin):
        return self.push('analogRead',pin)
    
    def digitalRead(self,pin):
        return self.push('digitalRead',pin)
        
    def analogWrite(self,pin,value):
        return self.push('analogWrite',pin+str(value))
    
    def digitalWrite(self,pin,value):
        return self.push('digitalWrite',pin+str(value))

    def setFreq(self,value):
        return self.push('setFreq',value)
        
    def getTone(self,pin):
        return self.push('getPulse',pin)
        
        
        
        
        
if __name__ == "__main__":
    ac = "abc123"
    g = photon("class1",ac)
    g.getDevices()
    print g.setFreq(500)
    print g.setInput('A0')
    print g.setInput('A0')
    #print g.flash("temp.ino")

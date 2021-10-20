class C3DAux(object):

    __instance = None
    nombre = None
    label = 0
    temp = 0

    def getLabel(self):
        self.label +=1
        return str(self.label)

    def getTemp(self):
        self.temp +=1
        return str(self.temp)

    def __new__(cls):
        if C3DAux.__instance is None:
            C3DAux.__instance = object.__new__(cls)
        return C3DAux.__instance

#ricardo = SoyUnico()
#ricardo.nombre = "Ricardo Moya"
#print(ricardo)
#ramon = SoyUnico()
#ramon.nombre = "Ramón Invarato"
#print(ramon)

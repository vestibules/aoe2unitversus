import requests, json, time

unitsSummary = {} # contains the created id + unit name to easy display
listValues = []   # contains a list of all characteristics value of the selected unit
listUnits = []    # contains created units objects

class unit:
    def __init__(self,dic):
        self.name = dic.get('name')
        self.life = dic.get('hit_points')
        self.attackPoint = self.getAttackPoint(dic)
        self.cacArmor = self.getArmorcac(dic)
        self.rangeArmor = self.getRangeArmor(dic)
    
    def isAlive(self):
        if self.life > 0:
            return True
        else:
            print(f'{self.name} trépasse !')
            return False
    
    def getAttackPoint(self,dic):
        exists = dic.get('attack')
        if exists:
            return exists
        else:
            return 0
    
    def getArmorcac(self,dic):
        stats = dic.get('armor')
        stats = stats.split('/')
        stats = stats[0]
        return stats

    def getRangeArmor(self,dic):
        stats = dic.get('armor')
        stats = stats.split('/')
        stats = stats[1]
        return stats

class physicalUnit(unit):
    typeUnit = 'Unité au corps à corps'
    def __init__(self,list):
        super().__init__(list)

    def attack(self, oponent):
        calcul = int(self.attackPoint) - int(oponent.cacArmor)
        if calcul < 1:
            calcul = 1
            oponent.life -= calcul
        else:
            oponent.life -= calcul
        absorbed = self.attackPoint - calcul
        armorMessage = f"L'amure corps à corps a absorbé {absorbed} dégâts."
        print(f"{self.name} inflige {calcul} dégâts à {oponent.name} ! {armorMessage}" )

class rangeUnit(unit):
    typeUnit = 'Unité à distance'
    def __init__(self,valuelist):
        super().__init__(valuelist)

    def attack(self, oponent):
        calcul = int(self.attackPoint) - int(oponent.rangeArmor)
        if calcul < 1:
            calcul = 1
            oponent.life -= calcul
        else:
            oponent.life -= calcul
        absorbed = self.attackPoint - calcul
        armorMessage = f"L'amure perçage a absorbé {absorbed} dégâts."
        print(f"{self.name} inflige {calcul} dégâts à {oponent.name} ! {armorMessage}" )

def choiceUnit():
    global listUnits
    while len(listUnits) < 2:
        choice = int(input())
        selected = response[choice - 1]
        testType = selected.get('range')
        if testType:
            listUnits.append(rangeUnit(selected))
        else:
            listUnits.append(physicalUnit(selected))
    for i in listUnits:
        print(f'{i.name} : {i.typeUnit}')
        print(f'Armure corps à corps : {i.cacArmor} | Armure perçage : {i.rangeArmor}')

def battle(objectlist):
    while objectlist[0].isAlive() == True or objectlist[1].isAlive == True:
        for i in range(len(objectlist)):
            objectlist[i].attack(objectlist[i-1])
            time.sleep(0.5)
        for i in range(len(objectlist)):
            if objectlist[i].isAlive() == False:
                for i in objectlist:
                    if i.life > 0:
                        print(f'{i.name} est victorieux !')
                return

r = requests.get('https://age-of-empires-2-api.herokuapp.com/api/v1/units')
response = json.loads(r.content)
response = response.get('units')

for i in range(len(response)):
    id = response[i].get('id')
    name = response[i].get('name')
    unitsSummary.setdefault(id,name)

for id,name in unitsSummary.items():
    print(f'{id} : {name}')

choiceUnit()
battle(listUnits)
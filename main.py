import requests, json, time

unitsSummary = {} # contains the created id + unit name to easy display
listValues = []   # contains a list of all characteristics value of the selected unit
listUnits = []    # contains created units objects

class unit:
    ATB = 0
    def __init__(self,dic):
        self.name = dic.get('name')
        self.life = dic.get('hit_points')
        self.attackPoint = self.getAttackPoint(dic)
        self.cacArmor = self.getArmorcac(dic)
        self.rangeArmor = self.getRangeArmor(dic)
        self.reload_time = dic.get('reload_time')
    
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

    def getATB(self):
        self.ATB += 1
        if self.ATB < self.reload_time:
            return False
        else:
            self.ATB = 0
            return True



class physicalUnit(unit):
    position = 0
    typeUnit = 'Unité au corps à corps'
    def __init__(self,dic):
        super().__init__(dic)
        self.speed = dic.get('movement_rate')

    def attack(self, oponent):
        if oponent.typeUnit == 'Unité à distance':
            while self.position < oponent.range:
                print(f'{self.name} se rapproche ...')
                self.position += self.speed
                return
        canAttack = self.getATB()
        if canAttack:
            if self.attackPoint == 0:
                print(f'{self.name} ne fait aucun dégât !')
                return
            calcul = int(self.attackPoint) - int(oponent.cacArmor)
            if calcul < 1:
                calcul = 1
                oponent.life -= calcul
            else:
                oponent.life -= calcul
            absorbed = self.attackPoint - calcul
            armorMessage = f"L'armure corps à corps a absorbé {absorbed} dégâts."
            print(f"{self.name} inflige {calcul} dégâts à {oponent.name} ! {armorMessage}" )
        else:
            return

class rangeUnit(unit):
    typeUnit = 'Unité à distance'
    def __init__(self,dic):
        super().__init__(dic)
        self.range = self.getRange(dic)
        self.speed = dic.get('movement_rate')
        self.position = self.getRange(dic)

    def getRange(self,dic):
        stat = dic.get('range')
        if (self.name).lower() == 'archer':
            return 3
        else:
            try:
                if '.' in stat or '(' in stat:
                    stat = int(stat[0])
                    return stat
                elif len(stat) > 2:
                    statList = stat.split('-')
                    stat = int(statList[1])
                    return stat
            except TypeError:
                return stat

    def attack(self, oponent):
        if oponent.typeUnit == 'Unité à distance':
            while self.position < oponent.range:
                print(f'{self.name} se rapproche ...')
                self.position += self.speed
                return
        canAttack = self.getATB()
        if canAttack:
            if self.attackPoint == 0:
                print(f'{self.name} ne fait aucun dégât !')
                return
            calcul = int(self.attackPoint) - int(oponent.rangeArmor)
            if calcul < 1:
                calcul = 1
                oponent.life -= calcul
            else:
                oponent.life -= calcul
            absorbed = self.attackPoint - calcul
            armorMessage = f"L'armure perçage a absorbé {absorbed} dégâts."
            print(f"{self.name} inflige {calcul} dégâts à {oponent.name} ! {armorMessage}" )
        else:
            return

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
    while objectlist[0].isAlive() or objectlist[1].isAlive():
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
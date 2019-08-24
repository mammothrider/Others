import random
class BullAndCow:
    def __init__(self):
        self.law = {}
        self.legalnumber = []
        self.fullAnswer = self.getAllLegalAnswer(res = [])
        print(len(self.fullAnswer))
    
    def isLegal(self, num):
        for key in self.law:
            tmpScore = self.getScore(key, num)
            #如果已知有n个准确位，则合法数必然有且仅有n个和已知的准确位
            #如果已知有n个匹配位，则合法数有且仅有n和和已知的匹配位
            if tmpScore[0] != self.law[key][0] or sum(tmpScore) != sum(self.law[key]):
            # if tmpScore[0] < self.law[key][0] or sum(tmpScore) != sum(self.law[key]):
                return False
        return True
    # import pysnooper
    # @pysnooper.snoop()
    def getAllLegalAnswer(self, first = None, second = None, third = None, res = None):
        if first and second and third:
            num = first + second + third
            if self.isLegal(num):
                res.append(num)
            return res

        next = set(map(str, range(1, 10))) - set([first, second, third])
        for k in next:
            if not first:
                self.getAllLegalAnswer(first = k, res = res)
            elif not second:
                self.getAllLegalAnswer(first = first, second = k, res = res)
            else:
                self.getAllLegalAnswer(first = first, second = second, third = k, res = res)

        return res
        
    def selectNumber(self):
        if not self.law:
            return "123"
            
        pos = self.getAllLegalAnswer(res = [])
        count = len(pos)
        print("Count", count)
        print(pos)
        if count <= 2:
            return pos[0]
            
        targetNumber = ''
        targetCount = 9999
        # t = random.randint(0, count - 1)
        # targetNumber = pos[t]
        
        for tmptrg in self.fullAnswer:
            if tmptrg in self.law:
                continue
                
            res = {}
            for tmpans in pos:
                #assume answer, get posible result
                score = self.getScore(tmptrg, tmpans)
                if score in res:
                    continue
                
                #try solve, count left number
                self.pushResult(tmptrg, score[0], score[1])
                tmppos = self.getAllLegalAnswer(res = [])
                self.popResult(tmptrg)
                
                res[score] = len(tmppos)
                
            #max left number less than current, select
            maxres = max(res.values())
            if maxres < targetCount:
                targetCount = maxres
                targetNumber = tmptrg
        return targetNumber
        
    def getScore(self, tar, ans):
        hsum = 0
        csum = 0
        for i in range(len(tar)):
            if tar[i] == ans[i]:
                csum += 1
            elif tar[i] in ans:
                hsum += 1
        return (csum, hsum)
        
    def pushResult(self, number, correct, half):
        self.law[number] = (correct, half)
        
    def popResult(self, number):
        self.law.pop(number, None)


def decodeSecret():
    solver = BullAndCow()
    while True:
        print("Law", solver.law)
        number = solver.selectNumber()
        print(number)
        res = input()
        if res == "new":
            solver = BullAndCow()
            continue
            
        a, b = res.split(" ")
        solver.pushResult(number, int(a), int(b))
        
        
def testIsLegal():
    solver = BullAndCow()
    solver.pushResult("123", 0, 1)
    solver.pushResult("456", 0, 2)
    solver.pushResult("789", 0, 0)
    print(solver.law)
    print(sorted(solver.getAllLegalAnswer(res = [])))
            
# testIsLegal()
decodeSecret()
# solver = BullAndCow()
# print(len(solver.getAllLegalAnswer(res = [])))
# print(len(solver.getAllLegalAnswer(res = [])))
# print(len(solver.getAllLegalAnswer(res = [])))
# print(len(solver.getAllLegalAnswer(res = [])))
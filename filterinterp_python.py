import math

class FilterInterpreter():
    def __init__(self):
        self.current_observation = {}

    def initializeFilterProgram(self, filterText):
        pass
    def setCurrentObservation(self, current_observation):
        self.current_observation = current_observation

    def interpret(self):
        filteron = False
        falling = False
        currentfilterid = self.current_observation['candidate']['fid']
        currentmagnitude = self.current_observation['candidate']['magpsf']
        currentdate = self.current_observation['candidate']['jd']
        prevcandidates = self.current_observation['prv_candidates']
        if (prevcandidates):
            filtermatch = False
            i = len(prevcandidates) - 1
            while ((i >= 0) and ((not filtermatch))):
                lastfilterid = prevcandidates[i]['fid']
                filtermatch = lastfilterid == currentfilterid
                if (filtermatch):
                    lastmagnitude = prevcandidates[i]['magpsf']
                    lastdate = prevcandidates[i]['jd']
                    falling = ((lastmagnitude - currentmagnitude) / (currentdate - lastdate)) < 0
                    
                i -= 1
            filteron = falling
        return filteron


def isMatch(studentA, studentB):
    eastSide = ('stone', 'bates', 'mcafee', 'freeman')
    westSide = ('tower', 'claflin', 'severance', 
    'munger', 'lakehouse', 'beebee', 'cazenove', 'pomeroy', 'shafer')
    if studentA['availability'] == studentB['availability']:
        return True 
    if studentA['resHall'] in westSide and studentB['resHall'] in westSide:
        return True
    if studentA['resHall'] in eastSide and studentB['resHall'] in eastSide:
        return True 
    return False 
    



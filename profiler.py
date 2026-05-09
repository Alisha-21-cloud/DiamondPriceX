changingParam = ['Cut','Color','Clarity']
changingValues = [['Ideal','Premium','Very Good','Good','Fair'],['G','E','F','H','D','I','J'],['SI1 (Slightly Included)','VS2 (Very Slightly Included)','SI2 (Slightly Included)','VS1 (Very Slightly Included)','VVS2 (Very Very Slightly Included)','VVS1 (Very Very Slightly Included)','IF (Internally Flawless, best quality)','I1 (Included, lowest quality)']]


def generateProfile(data):
    Diamond_Profile = []
    for x in data:
        if x in changingParam:
            X_index = changingParam.index(x)
            newStrings = x + '  :  ' + changingValues[X_index][int(data[x])]
        else:
            newStrings = x + '  :  ' + data[x]
        Diamond_Profile.append(newStrings)
    print(Diamond_Profile)
    return Diamond_Profile
import re

def preFileOperations():
    with open("survivors.csv","w+") as file2:
        file2.write("CIVILIZATIONS,CIV. DIFICULTY,POP. LIMIT,CASTLE AGE,IMPERIAL AGE,BOMBARD TOWERS,BONUS,PENALTY")

def populationPopulator(default_pop="30",castle_pop="",imperial_pop=""):
    """function to populate 'pop' string"""   
    pop = f"starting = {default_pop}"
    if castle_pop == "" and imperial_pop == "":
        pass
    if castle_pop != "":
        pop += f"\ncastle age ={castle_pop}"
    if imperial_pop != "":
        pop += f"\nimperial age ={imperial_pop}"
    return pop

def parser():
    with open("survivors.txt","r") as file:
        lines = file.readlines()

    startFlag = False
    nextLineAfterStart = False
    civ = difficulty = castle = imperial = bombard ="nil"
    default_pop ="30"
    castle_pop=imperial_pop=pop=bonus=penalty=""
    preFileOperations()
    for line in lines:
        if line.find("=====") != -1:                                                        #for removing decoration
            if startFlag:                                                                   #will execute when "====" is not start of a new civ                     
                with open("survivors.csv","a+") as file2:
                    line = "\n{0},{1},\"{2}\",{3},{4},{5},\"{6}\",\"{7}\"".format(civ,difficulty,pop,castle,imperial,bombard,bonus,penalty)
                    file2.write(line)
                    civ = difficulty = castle = imperial = bombard ="nil"
                    default_pop ="30"
                    castle_pop=imperial_pop=pop=bonus=penalty=""                        
                startFlag = False                    
            else:                                                                           #will execute when "====" is start of new civ
                startFlag = True
                nextLineAfterStart = True

        elif nextLineAfterStart and line.find("=====") == -1:                               #for finding civ name
            nextLineAfterStart = False
            civ = line.split(":")[0].strip(" \n")
            if civ.find(",") !=-1:
                civ = civ.split(",")
                civ = '\n'.join(civ)
                civ = f"\"{civ}\""

        elif line.find("Difficulty") != -1 :                                                #for finding difficulty
            difficulty = line.split(":")[1].strip(" \n")   

        elif re.search("castle Age:",line,re.IGNORECASE) and line.find("Pop limit") == -1:  #for finding castle age kill and time requirements
            if line.find("kills") != -1:
                castle = line.split(":")[1].strip(" \n")

        elif line.find("Imperial Age:") != -1 and line.find("Pop limit") == -1:             #for finding imperial age kill and time requirements
            imperial = line.split(":")[1].strip(" \n")

        elif line.find("Bombard Tower") != -1 :                                             #for finding bombard tower kill requirements
            if line.find("NO") != -1:
                bombard = "no bombard tower"
            if line.find("Free") != -1:
                bombard = "free bombard tower"
            elif line.find("kills") != -1:                    
                bombard = line.split(":")[1].strip(" \n")
            else:
                pass

        elif line.find("Pop limit") != -1 :                                                 #for finding pop limit 
            if line.find("Imperial") != -1:                                                 #for pop limit with both imperial and castle
                splited_line = line.split("+")
                imperial_pop = splited_line[2].split(":")[1].strip(" \n")
                castle_pop = splited_line[1].split(":")[1].strip(" \n")
            elif line.find("Castle") != -1 and line.find("Imperial") == -1:                 #for pop limit with only castle
                splited_line = line.split(":")
                if line.find("+ Pop limit in Castle age:") !=-1:
                    castle_pop = splited_line[1].strip(" \n")                        
                else:
                    castle_pop = splited_line[1].split(" ")[1]
            else:                                                                           #for pop limit with no castle or imperial
                default_pop = line.split(":")[1].strip(" \n")                
            pop = populationPopulator(default_pop,castle_pop,imperial_pop)

        elif (line.find("+") != -1 or line.find("=") != -1) and line.find("Pop limit") == -1 and line.find("==") == -1:    #for finding bonus
            bonus+=line.replace("=","+",1).replace("+", "->",1).strip(" ")        

        elif line.find("- ") != -1 :                                                        #for finding bonus point with - sign
            penalty+= line.strip(" ")

if __name__ == "__main__":
    parser()
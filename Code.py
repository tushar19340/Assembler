
temp = open("temp.txt","w")
fileName = input("enter file name to be assembled :")
test = open(fileName)
code = open("machineCode.txt","w")


noOfCodeLines = 0

for s in test:
	noOfCodeLines += 1
	s = s.strip()
	if(len(s) != 0):
		if( s.find("/") == -1):
			temp.write(s)
			temp.write("\n")
		else:
			if(s[0] =="/"):
				continue
			else:

				temp.write(s[:s.find("/")])
				temp.write("\n")
temp.close()
f = open('temp.txt',"r")

opcode={"CLA":"0000", "LAC":"0001", "SAC":"0010", "ADD":"0011", "SUB":"0100", "BRZ":"0101", "BRN":"0110", "BRP":"0111", "INP":"1000", "DSP":"1001", "MUL":"1010", "DIV":"1011", "STP":"1100"}


############################LABEL TABLE################################################
labelCount = 0
for s in f:
	s = s.split()
	if(s[0] not in opcode  and s[0][-1] == ":"):
		labelCount += 1

# print(labelCount)
labelTable = [ [0 for i in range(2)] for j in range(labelCount)]
lableList = []
f.seek(0)
address = 0
i = 0
location_counter = 0

for s in f:
	address += 1
	s = s.split()
	if(s[0] not in opcode and s[0][-1] == ":"):
		labelTable[i][0] = s[0]
		labelTable[i][1] = location_counter
		lableList += [s[0]]
		i += 1
	location_counter += 1

address2 = address
# print(labelTable)
##############################################################LABEL TABLE FINISHED#######################################################################
                                                                   
##############################################################SYMBOL TABLE ##############################################################################                                                                    

f.seek(0)
symbolList = []
literalList = []
symbolCount = 0
literalCount = 0
symbolTable = []
literalTable = []
location_counter = 0

for s in f:
	s = s.split()
	if(len(s) == 2):
		# print(s[0])
		# print(type(s[1]))
	
		if(s[0] in opcode):
			if(s[1].isdigit() == False):
				if(s[1][0] == "="):
					if(s[1] not in literalList):
						literalList += [s[1]]
						literalTable += [[s[1],bin(address)[2:]]]
						address += 1
						literalCount += 1
				elif((s[1] + ":") in lableList):
					location_counter -= 1
				else:
					if(s[1] not in symbolList and (s[1] + ":") not in lableList and s[0] != "CLA" ):
						symbolTable += [[s[1],bin(address)[2:] ]]
						symbolList += [s[1]]
						symbolCount += 1
						address += 1
					# print(s[1])

	elif(len(s) == 3):
		if(s[2].isdigit() == False):
			if(s[2][0] == "="):
				if(s[2] not in literalList):
					literalTable += [[s[2],bin(address)[2:]]]
					address += 1
					literalList += [s[2]]
					literalCount += 1
			elif( (s[2] + ":") in lableList ) :
				location_counter -= 1
			else:
				if(s[2] not in symbolList):
						symbolList += [s[2]]
						symbolTable += [[s[2], bin(address)[2: ] ]]
						symbolCount += 1
						address += 1
				# print(s[2])
	location_counter += 1


f.seek(0)
opList = []

for s in f:
	s = s.split()
	if(s[0] not in lableList):
		opList += [s[0]]

# print(opList)


###############################################ONE PASS FINISHED#########################################
print("LABEL TABLE : ")
for i in labelTable:
	print(*i)

print(" ")

print("SYMBOL TABLE : ")
for i in symbolTable:
	print(*i)

print(" ")

print("LITERAL TABLE : ")
for i in literalTable:
	print(*i)


# print(labelTable)
# # print(lableList)
# # print(symbolList)
# print(symbolTable)
# # print(literalList)
# print(literalTable)
# print(symbolCount, literalCount)
code = open("machineCode.txt","w")

def findLabel(label):
	for i in labelTable:
		if(i[0] == label):
			return i[1]

def findSymbol(symbol):
	for i in symbolTable:
		if(i[0] == symbol):
			return i[1]

def findLiteral(literal):
	
	for i in range(len(literalTable)):
		if(literalTable[i][0] == literal):
			return literalTable[i][1]


def Make8Bit(binary):
	if(len(binary) == 8):
		return binary
	elif(len(binary) < 8):
		s = ""
		for i in range(0, (8 - len(binary) )):
			s += "0"
		s += binary
		return s

##################################################################ERROR CHECKING#########################################################################
errorFile = open("errorFile.txt","w")
errorcheck = 0
errorLines = []

##############out of bounds error#####################
if(noOfCodeLines > 255):
	errorFile.write("Not enough memory ")
	errorcheck = 1
########################invalid opcode##########################

f.seek(0)
line = -1
for s in f:
	line += 1
	
	s = s.split()
	if(len(s) == 1):
		if(s[0] not in opcode and s[0] not in lableList):
			errorFile.write("Invalid opcode used in Line ")
			errorFile.write(str(line))
			errorFile.write("\n")
			errorFile.write("\n")
			errorLines += [line]

	if(len(s) == 2):

		if(s[0] not in opcode and s[0] not in lableList):

			errorFile.write("Invalid opcode used in Line ")
			errorFile.write(str(line))
			errorFile.write("\n")
			errorFile.write("\n")
			errorLines += [line]
	if(len(s) == 2):
		if(s[0] in opcode):
			continue
		elif(s[0] in lableList and s[1] not in opcode):
			errorFile.write("Invalid Opcode in Line ")
			errorFile.write(str(line))
			errorFile.write("\n")
			errorFile.write("\n")
			errorLines += [line]
	if(len(s) == 3):
		if(s[0] in lableList and s[1] not in opcode):

			errorFile.write("Invalid Opcode in Line ")
			errorFile.write(str(line))
			errorFile.write("\n")
			errorFile.write("\n")
			errorLines += [line]
	


		

####################checked################################



###################stop not found##########################
stopCheck = 0
for op in opList:
	if(op == "STP"):
		stopCheck = 1


if(stopCheck == 0):
	errorFile.write("STP not found")
	errorFile.write("\n")
	errorFile.write("\n")
	errorcheck = 1
	

################checked##################################





###############multiple label deifnition###################
wrongLabel = []
for i in range (len(lableList)):
	for j in range( len(lableList)):
		if(i != j and lableList[i] == lableList[j] and lableList[i] not in wrongLabel):
			wrongLabel += [lableList[i]]
			errorFile.write(" multiple label definition error: ")
			errorFile.write(lableList[i])
			errorFile.write("\n")
			errorFile.write("\n")
			errorcheck = 1


			

##################checked########################




##################invalid no. of operands#########################
f.seek(0)
line = 0
for s in f:
	s = s.split()
	if(len(s) >= 4):
		errorFile.write("invalid no. of operands: ")
		errorFile.write(s[2])
		errorFile.write(" ")
		errorFile.write(s[3])
		errorFile.write(" Line No. :")
		errorFile.write(str(line))
		errorFile.write("\n")
		errorFile.write("\n")
		
	if(s[0] == "CLA" and len(s) == 2):
		errorFile.write("No operand required but given ")
		errorFile.write(s[0])
		errorFile.write(" Line No. :")
		errorFile.write(str(line))
		errorFile.write("\n")
		errorFile.write("\n")
		
	if(len(s) == 3  and s[1] == "CLA" ):
		errorFile.write("No operand required ")
		errorFile.write(s[1])
		errorFile.write("Line No. :",)
		errorFile.write(str(line))
		errorFile.write("\n")
		errorFile.write("\n")

	if(len(s) == 1 and s[0] != "CLA" and s[0] != "STP" ): 
		errorFile.write("Not enough operands are given")
		errorFile.write("\n")
		errorFile.write("\n")
		errorLines += [line]

		
	line += 1	

###################################checked##################################



#################################invalid lable in brn brz brp#######################
f.seek(0)
line = 0
for s in f:
	s = s.split()
	for i in range(len(s)):
		if(len(s) == 2):
			if("BRZ" == s[0] or "BRN" == s[0] or "BRP" == s[0]):
				if(s[1] not in lableList and s[1].isdigit == False):
					errorFile.write("Invalid address provided: ")
					errorFile.write(s[1])
					errorFile.write(" Line No.: ")
					errorFile.write(str(line))
					errorcheck = 1
				
		if(len(s) == 3):
			if("BRZ" == s[1] or "BRN" == s[1] or "BRP" == s[1] and s[0] in lableList):
				if(s[2] not in lableList and s[2].isdigit == False):
					errorFile.write("Invalid address provided: ")
					errorFile.write(s[2])
					prierrorFile.write(" Line No.: ")
					errorFile.write(str(line))
					errorFile.write("\n")
					errorFile.write("\n")
					errorcheck = 1
	line += 1
################################checked##########################################



################################checking division by zero error##################
f.seek(0)
line = 0
for s in f:
	s = s.split()
	for i in range(len(s)):
		if("DIV" in s ):
			if( (len(s) == 2 and s[1] =="0")  or (len(s) == 3 and s[2] == "0")):
				errorFile.write("division by zero error in line : " )
				errorFile.write(str(line))
				errorFile.write("\n")
				errorFile.write("\n")
				errorLines += [line]
	line+= 1
				


################################################checked#################################################



###################################checking for fatal errors############################
if(errorcheck == 1):
	exit()

##################################################################ERROR CHECKING DONE####################################################################
f.seek(0)
labelChecker = 0
line = 0
for s in f:
	s = s.split()
	# print(errorLines)
	if(line not in errorLines):
		for i in range(len(s)):
			if(s[i] in opcode):
				code.write(opcode[s[i]])
				code.write(" ")

			elif(s[i] in symbolList):
				binary = str(findSymbol(s[i]))
				code.write(Make8Bit(binary))
			
			elif(s[i] in literalList):
				binary = str(findLiteral(s[i]))
				# print(binary)
				code.write(Make8Bit(binary))

			elif(s[i].isdigit()):
				binary = bin(int(s[i]))[2:]
				code.write(Make8Bit(binary))
			
			elif(s[i] in lableList):
				continue
			
			else:
				if((s[i] + ":" ) in lableList):
					binary = bin( int(findLabel(s[i] + ":")))[2:]
					code.write(Make8Bit(binary))
		code.write("\n")

	line += 1
	


import random

DIGITS = [0,1,2,3,4,5,6,7,8,9]

L_ALPHABETS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
U_ALPHABETS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SYMBOLS = ['@', '#', '$', '-', '/', '|', '~', '!']

class generatePassword:
	
	def __init__(self,uk):
		self.unique_key = str(uk)
		self.min_length = 25
		self.max_length = 45

	def appendRandomData(self,password,rd,rla,rua,rs):
		_l = [rua,rs,rla,rd] 
		for i in _l:
			password.append(i)

	def randomPickup(self,password,pl,unique_key):
		for i in range(0,pl,4):
			r_digit = str(random.choice(DIGITS))
			r_u_alphabets = random.choice(U_ALPHABETS)
			r_l_alphabets = random.choice(L_ALPHABETS)
			r_symbol = random.choice(SYMBOLS)
			self.appendRandomData(password,r_digit,r_l_alphabets,r_u_alphabets,r_symbol)
		password.append(unique_key)
		random.shuffle(password)
		password_str = ''.join(password)
		return password_str

	def generate(self):
		password = []
		unique_key__len = len(str(self.unique_key))
		min_length = self.min_length
		max_length = self.max_length - unique_key__len
		password_length = random.randint(min_length,max_length)
		g_password = self.randomPickup(password,password_length,self.unique_key)
		return g_password

def generateID(unique_key):
	gp = generatePassword(uk=unique_key)
	password = gp.generate()
	return password


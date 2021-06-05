class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.id_token = 0
		self.actual_token = self.tokens[self.id_token]
		self.last_token = ''
	def advance( self ):
		self.id_token += 1
		if self.id_token < len(self.tokens):
			self.actual_token = self.tokens[self.id_token]
			self.last_token = self.tokens[self.id_token - 1]

	def expect(self, item, arg = None):
		og = self.id_token
		possible = False
		if item != None:
			try:
				if arg == None:
					ans = item()
				else:
					ans = item(arg)
				if type(ans) == bool:
					possible = ans
				else:
					possible = True
			except:
				possible = False
		self.id_token = og
		self.actual_token = self.tokens[self.id_token]
		self.last_token = self.tokens[self.id_token - 1]
		return possible

	def read(self, item, type = False):
		if type:
			if self.actual_token.type == item:
				self.advance()
				return True
			else:
				return False
		else:
			if self.actual_token.value == item:
				self.advance()
				return True
			else:
				return False
	value, result, value1, value2 = 0,0,0,0
	def Expr(self):
		while self.expect(self.Stat()):
			self.Stat()
			self.read(";")
			while self.expect(self.white}}()):
			self.read('white', True)
		while self.expect(self.read(white}".")):
		self.read("white.")

	def Stat(self):
		value=0;
		re=self.Expression(re)
		self.value>()
		print("Resultado: ",value)

	def Expression(self,result):
		 result1,result2=0,0
		re=self.Term(re)
		self.result1>()
		while self.expect(self.read("+")) or self.expect(self.read("-")):
			if self.expect(self.read("+")):	
				self.read("+")
				re=self.Term(re)
				self.result2>()
				result1+=result2
	
			elif self.expect(self.read("-")):
				self.read("-")
				re=self.Term(re)
				self.result2>()
				result1-=result2
		result=result1
		return result

	def Term(self,result):
		result1,result2=0,0
		result1=self.Factor(result1)
		while self.expect(self.read("*")) or self.expect(self.read("/")):
			if self.expect(self.read("*")):	
				self.read("*")
				re=self.Factor(re)
				self.result2>()
				result1*=result2
	
			elif self.expect(self.read("/")):
				self.read("/")
				re=self.Factor(re)
				self.result2>()
				result1/=result2
		result=result1
		return result

	def Factor(self,result):
		sign=1
		if self.expect(self.read('-')):
			self.read("-")
			sign = -1
		result=self.Number(result)if self.expect(self.Number(result>
)):
			
			
		elif self.expect(self.read("(")):
			self.read("(")
			result=self.Expression(result)
			self.read(")")
		 result*=sign 

	def Number(self,refdoubleresult):
		self.read('number', True)if self.expect(self.number
	()):
			
			
		elif self.expect(self.decnumber()):
		decnumberresult = float(last_oken.value)


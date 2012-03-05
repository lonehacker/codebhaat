import urllib2,urllib
import json
import hashlib
import settings
from time import gmtime,strftime



"""
ready() - returns True if result available, False if result not available
result - Result of the evaluation (in old format)

"""
class Checker():
	def submit(self,args):
		name, language,program,filename, tests, time_limit = args
		langcode = 0
		url = url+'?token='+token
		self.tests = tests
		if(language=='c'):
			langcode = 1
		elif(language=='c++'):
			langcode = 2
		elif(language=='java'):
			langcode = 4
		json_dict = {}
		inputlist = []
		json_dict['lang'] = langcode
		json_dict['source'] = program
		for i in tests:
			inputpath=i['input']
			f = open(inputpath,"r")
			inputlist.append(f.read())
			f.close
		json_dict['testcases'] = inputlist 
		self.hash = hashlib.sha1(program+strftime("%H%M%S",gmtime())).hexdigest()
		json_dict['hash'] = self.hash
		json_data = json.dumps(json_dict)
		# convert str to bytes (ensure encoding is OK)
		post_data = json_data.encode('utf-8')
		print post_data
		# now do the request for a url
		req = urllib2.Request(url)
		req.add_data(post_data)
		req.add_header('Content-Type','application/json')
		try:
			response = urllib2.urlopen(req).read()
			responsedict = json.loads(response)
			self.key = responsedict['key']
			return True
		except HTTPError,e:
			if (e.code == 400):
				print "Error"
				self.key = -1
				return False
			
	
	# Code has been submitted twice.
	def ready(self):
		if(self.key == -1):
			return False
		geturl = urllib.urlencode({'key':self.key,'token':token})
		try:
			response = urllib2.urlopen(urllib2.Request(geturl)).read()
			responsedict = json.loads(response)
			if(responsedict['status'] == "Processed"):
				#check for error condition
				result['successful'] = True
				result['marks'] = 0
				if(responsedict['result'] is not None):
					if(responsedict['result']['result'] != 255):
						for test,op,time,signal in zip(self.tests,responsedict['result']['stdout'],responsedict['result']['time'],responsedict['result']['signal']):
							if(signal == 62 or signal == 25):
								continue
							outputpath = i['output']
							f = open(outputpath,"r")
							output = f.read()
							if(output.strip() == op.strip()):
								if time > test['time_limit_soft']:
									exceed_time = time - test['time_limit_soft']
									max_exceed_time = test['time_limit'] - test['time_limit_soft']
									result['marks'] += round(test['marks']*((max_exceed_time - exceed_time)/max_exceed_time), 2)
								else:
									result['marks'] += test['marks']
							else:
								result['successful'] = False
								result['error']=case or 'Runtime Exceeded'
								break
					else:
						result['error'] = 'Compilation Error'
						result['successful'] = False

				if not result['successful']:
					result['marks'] = 0
				return True
			else:
				return False
		except HTTPError,e:
			return False
	def __init__(self):
		
		self.key = -1
		self.hash = ""
		self.result = {}
		self.tests = []
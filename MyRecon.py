import os
#import file
import subprocess
import re

folder=""
success_endpoints=[]
redirect_endpoints=[]
unauthorized_endpoints=[]

def find_url(string): 
  
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url] 

def find_subdomain(domain):
	cmd="python ./Sublist3r/sublist3r.py -d "+domain+" -o subdomain.txt"
	try:
		print("obtaining subdomain information.....")
		rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		rsp.communicate()
		print('completed obtaining subdomain information')
	except:
		print('failed to obtain subdomain')

def find_endpoints(domain):
	#Feeding each subdomain to fuzz directories using dirhunt
	print("Start getting endpoints for each subdomain")
	domain=domain.rstrip("\n")
	cmd="dirhunt "+domain+" > dirhunt.log 2>&1"
	print("Finding endpoints of "+domain)
	try:
		rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		rsp.communicate()
		print('Obtained endpoint information')
	except:
		print('failed to obtain endpoint')

	#Now read the endpoints and append it into a list
	f=open("dirhunt.log")
	lines=f.readlines()
	for line in lines:
		try:
			newendpoint=find_url(line)[0]
		except:
			newendpoint=""
		if "200" in line:
			success_endpoints.append(newendpoint)
		if "30" in line:
			redirect_endpoints.append(newendpoint)
		if "403" in line:
			unauthorized_endpoints.append(newendpoint)

	f.close()

def print_endpoint_result():
	with open('endpoints.txt', 'w') as filehandle:
		filehandle.write('200:\n')
		for item in success_endpoints:
			filehandle.write('%s\n' % item)
		filehandle.write('----------------------\n')
		filehandle.write('30x:\n')
		for item in redirect_endpoints:
			filehandle.write('%s\n' % item)
		filehandle.write('403:\n')
		for item in unauthorized_endpoints:
			filehandle.write('%s\n' % item)


def find_sourcecode(domain):
	pass
	#to do


domain=input("Input a domain: ")
find_subdomain(domain)
f=open("subdomain.txt")
for endpoint in f:
	find_endpoints(endpoint)
f.close()
print_endpoint_result()







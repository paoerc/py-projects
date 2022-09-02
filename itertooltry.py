import shutil, os, glob, re, filecmp, sys, itertools, pathlib

module = sys.argv [1]
source = sys.argv[2] #source should NOT have / at the end
destination = sys.argv[3]
wildcard = module.upper()

pastepattern = destination + '/Modules/' + wildcard + "/vectors"
pastetiming =  destination + '/Modules/' + wildcard + "/timing"

funcpath = glob.glob(source + "/tmp-pattern/" + wildcard + "*/")     #/home/mc_aurix/UserData/Kristine/autogen/test_M3990BUP0AA932022-08-11_scan351/tmp-pattern/SCAN..../

strip = str(funcpath).strip("['']")

path = glob.glob(strip + "*")                     #/home/mc_aurix/UserData/Kristine/autogen/test_M3990BUP0AA932022-08-11_scan351/tmp-pattern/SCAN..../func, module, scan folders (array)


#print (path)
#path1= str(funcpath).strip("'[]'")					#stripped /home/mc_aurix/UserData/Kristine/autogen/test_M3990BUP0AA932022-08-11_scan351/tmp-pattern/SCAN..../func, module, scan folders string

combi = list(itertools.combinations(path, 2))
#duo = combi [i]
complist =[]
for duo in combi : 
	makeitastring = str(duo)
	breakcombi = makeitastring.split(",")					
	accessfirst = breakcombi[0]
	firstfolder = accessfirst.strip("(''")		
	strip1 = os.path.basename(firstfolder)
	
	accessfirst1 = breakcombi[1]
	secondfolder = accessfirst1[2:]
	secondfolder1 = str(secondfolder.strip("'')"))

	strip2 = os.path.basename(secondfolder1)

	if strip1.startswith(module) and strip2.startswith(module):
			
		timingsource=(firstfolder + "/tmp_v93k/timing/timing")
		eqn_orig= os.listdir(timingsource)
		eqn = [x for x in eqn_orig if x.endswith(".eqn") or x.endswith(".wave") or x.startswith("mport")]
		a = len(eqn)
		b= 0	
		
		while b < a:
			f1 = eqn [b]
			fullpathf1 = (timingsource + "/" + f1)
			ytimingsource=(secondfolder1 + "/tmp_v93k/timing/timing")
			eqn1_orig = os.listdir(ytimingsource)
			eqn1 = [x for x in eqn1_orig if x.endswith(".eqn") or x.endswith(".wave") or x.endswith(".tim")]			
			c = len (eqn1)
			if a == c: 
				f2 = eqn1 [b]
				fullpathf2 = (ytimingsource + "/" + f2)
				if f1 == f2 :
					comp = filecmp.cmp(fullpathf1, fullpathf2, shallow=True)
					complist.append(comp)
			
				###  LONG VERSION 	
					# if comp == True and f1 == f2:
						# print (strip1,"==>",f1)
						# print (strip2,"==>", f2,  "\n")
						# print(comp, "----timing matched", "\n")									
					if comp == False:
						print (strip1, "and" , strip2, "TIMING MISMATCH", "\n")
									
			b+=1
			
if all(complist) == True:
	print ("\n\n============DONE!! ALL TIMING MATCHED==============\n\n")	
else :
	print ("\n\n==================CHECK TIMING!!!==================\n\n")		
for folder in path :
		patterns = folder.split("/")
		last = str(patterns[-1:])
		strip1 = last.strip("['']")
		if strip1.startswith(module):
			vectors=(strip + strip1 + "/tmp_v93k/vectors")
			for file in glob.glob(vectors+"/*.pat"):
				patsname = os.path.basename(file)
				
				if module == 'scan' : 
					if re.search('io+',patsname) :
						shutil.copy(file, pastepattern+"/scan_io_pdelay")
						patsname_print = print(patsname, "copied" , "\n")
					elif re.search("lbist+",patsname) or re.search("reset+",patsname):
						shutil.copy(file, pastepattern+"/scan_lbist")
						patsname_print = print(patsname, "copied" , "\n")
					elif re.search("delay+",patsname) :
						shutil.copy(file, pastepattern+"/scan_delay")
						patsname_print = print(patsname, "copied" , "\n")
					else :
						shutil.copy(file,pastepattern+"/scan_stuck")
						patsname_print = print(patsname, "copied" , "\n")
				
				else : 
					shutil.copy(file, pastepattern)
			
					patsname_print = print(patsname, "copied" , "\n")
			
			for timing in glob.glob(strip + strip1 + "/tmp_v93k/timing/timing/*") :
				timename = os.path.basename(timing)
				if timename.endswith(".eqn"):
					shutil.copy(timing, pastetiming + "/eqn")
				elif timename.endswith(".wave") :
					shutil.copy(timing, pastetiming + "/wave")
				else : 
					shutil.copy(timing, pastetiming)

import time
import zotero2notion as zn

while 1:
	print("Checking zotero...")
	try:
		zn.execute()
	except:
		print("Some error happened!!!")
	print("Sleeping...")
	for t in range(1,10):
		print("==",end = " ",flush = True)
		time.sleep(1)
	print("")

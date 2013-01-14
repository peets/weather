#!/usr/bin/env python2
import feedparser, os.path, sys, re, time

condFile = "conditions"
iconDir = "icons/"
url = "http://www.weatheroffice.gc.ca/rss/city/qc-147_e.xml"

def updateCondFile (cond):
	cf = open(condFile, 'r+')
	for line in cf:
		if line.startswith(cond):
			break
	else:
		cf.write(cond + '\n')
	cf.close()

def getCurrentConditions(entries):
	returnInfo = {}
	cc = {}
	for e in entries:
		if e.category == "Current Conditions":
			cc = e
			break
	else:
		return {"error":"Error: Current Conditions not found"}
	for l in cc.description.split("\n"):
		#print l
		matches = re.search("<b>([^:]+):</b>([^<]+)<br ?/>", l)
		k = matches.group(1).strip()
		returnInfo[k] = matches.group(2).strip()
	return returnInfo

def toDzen():
	output = []
	d = feedparser.parse(url)
	cc = getCurrentConditions(d.entries)

	if "error" in cc:
		return cc["error"]

	if "Condition" in cc:
		updateCondFile(cc["Condition"])
		fn = iconDir + cc["Condition"] + ".xbm"
		if os.path.exists(fn):
			output.append("^i(" + fn + ")")
		else:
			output.append(cc["Condition"])
	if "Temperature" in cc:
		T = re.sub(r"&deg;", u'\u00b0', cc["Temperature"])
		output.append("^fg(#a1cdef)" + T + "^fg()")
	return ("^p(4)".join(output)).encode("utf_8")

if __name__ == "__main__":
	while(1):
		sys.stdout.write(toDzen() + "\n")
		sys.stdout.flush()
		time.sleep(60 * 15)

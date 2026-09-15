from pybasicwiki import basicwiki as bw
from pybasicwiki import HTMLFormatter

txt = """==hi==\nTest\n\npa''rag''raph 2\n[[Link to something]] test\n----\n[[Link to something else|Else]]\n==byte==\nbye\n"""
txt = """==About SensorBoard==
SensorBoard is a system of [[device]]s to [[read]] calorimetry data and storage of all that data on a single server.

See [[/experiment|Experiments ''are'' fun]] page to '''start's cool''' an experiment.

See [[/experiment|Experiments|300px]] page to start an experiment.

Don't include [[links]]: with colon after them.

: ''Indented [[Namespace:link]] italicized.''

Bold with possession such as '''smore'es''' and stuff.

This line ==is not a heading== because equals does not span the whole line.

\"\"\"
Blockquote ''no italics''.
Second line.
Third line.
\"\"\"

Items:
* Tacos
* Meat
** [[Chicken]]
** Beef
* Onions

{| class="prettytable"
|-
!! Meat !! Vegetable
|-
|| Beef || Lettuce
|-
|| Chicken || Corn
|}

Items:
* Meat
** [[Chicken]]
** Beef

{{Main|EKG | Holter|Pacer}}

{{Info Box|noparametersjusttext|anothertextparameter}}

{{Info Box|title=Hi|footer=[[Anterior STEMI|Anterior]], [[Lateral STEMI|Lateral]]}}

{{Navbox
|title=[[Pacemaker]]s
|templatename=Navbox Pacemaker
|labelwidth=150px
|group1=Important Pages
|list1=[[Theory of pacing]] • [[Pacemaker timing]] • [[Asynchronous pacing]]
|group2=[[Pacing modes]]
|list2=[[AAI]] • [[VVI]] • [[DDI]] • [[DDIR]] • [[VDD]] • [[DDD]] • [[DDDR]] • [[AOO]] • [[VOO]] • [[DOO]]
|group3=EKG rhythms
|list3=[[APR]] • [[VPR]] • [[AVDUAL]] • [[BIVP]] • [[LBBAP]] • [[DAPR]] • [[DVPR]]
|group4=Types
|list4=[[Transvenous pacemaker|Transvenous]] • [[Leadless pacemaker|Leadless]] • [[Temporary pacemaker|Temporary]] • [[Transcutaneous pacemaker|Transcutaneous]]
|group5=Pacing timing
|list5=[[Lower rate limit|LRL]] • [[Upper sensor rate|USR]] • [[Upper tracking rate|UTR]] • [[PVARP]]
|group6=[[Pacemaker malfunction|Failures]]
|list6=[[Failure to capture]] • [[Failure to sense]] • [[Undersensing]] • [[Oversensing]]
|group7=[[Device interrogation|Interrogation]]
|list7=[[Battery status]] • [[Presenting rhythm]] • [[Underlying rhythm]] • [[Arrhythmia log]] • Testing ([[Threshold]], [[Sensitivity]], [[Sensing]])
|group8=Others
|list8=[[Safety pacing]]
|group10=Companies
|list10=[[Abbott]]/St Jude • [[Biotronik]] • [[Boston Scientific]] • [[Medtronic]]
}}


and more things at the end.

~~~~
"""

print(txt)

def link(href, text=None):
	if text is None:
		return ("/wiki/something/%s" % href, href)
	else:
		return ("/wiki/something/%s" % href, text)

class TestHTMLFormatter(HTMLFormatter):
	"""Need to subclass to test template and signature"""
	def template(self, title, params, parserobj):
		return "{{%s | %s}}" % (title, str(params))

	def signature(self, t, parserobj):
		return "~~~SIGNATURE~~~"

f = TestHTMLFormatter(link)
def token_analyzer(tokens):
	# Modify token stream
	tokens.append( bw.text("Tokens analyzed") )
	tokens.append( bw.newline() )
	tokens.append( bw.newline() )
	print(tokens)
	return tokens

ret = bw.parseFormatter(txt, f, token_analyzer=token_analyzer)
print('============================')
print(ret)


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

Items:
* Tacos
* Meat
** [[Chicken]]
** Beef
* Onions

{{Info Box|noparametersjusttext|anothertextparameter}}

{{Info Box|title=Hi|footer=[[Anterior STEMI|Anterior]], [[Lateral STEMI|Lateral]]}}

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


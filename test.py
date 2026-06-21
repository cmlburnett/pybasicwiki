from pybasicwiki import basicwiki as bw
from pybasicwiki import HTMLFormatter

txt = """==hi==\nTest\n\npa''rag''raph 2\n[[Link to something]] test\n----\n[[Link to something else|Else]]\n==byte==\nbye\n"""
txt = """==About SensorBoard==
SensorBoard is a system of [[device]]s to [[read]] calorimetry data and storage of all that data on a single server.

See [[/experiment|Experiments]] page to start an experiment.

See [[/experiment|Experiments|300px]] page to start an experiment.

:Indented

Bold with possession such as '''smore'es''' and stuff.

This line ==is not a heading== because equals does not span the whole line.

Items:
* Tacos
* Meat
** [[Chicken]]
** Beef
* Onions


and more things at the end.
"""

print(txt)

def link(href, text=None):
	if text is None:
		return ("/wiki/something/%s" % href, href)
	else:
		return ("/wiki/something/%s" % href, text)

f = HTMLFormatter(link)
ret = bw.parseFormatter(txt, f)
print('============================')
print(ret)


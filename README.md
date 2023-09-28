# pybasicwiki
Very simple wiki parser. I created this for a cherrypy project so that I can document things online rather than hard editing template files. Wiki syntax is similar to MediaWiki but very simplified.

To use it:
	from pybasicwiki import basicwiki, HTMLFormatter
	def linker(href, text):
		if text is None:
			return ("/wiki/%s" % href, href)
		else:
			return ("/wiki/%s" % href, text)

	f = HTMLFormatter(linker)
	html = basicwiki.parseFormatter(wiki, f)

Supply a callback function to modify links when formatting to HTML.
Alternatively, a generator style parser can be used if you want to custom format every tag:

	for t in basicwiki.parse(wiki)
		if t.name == 'h1':
			# Do something
			pass
		elif t.name == 'italic':
			# Do something
			pass
		elif t.name == 'text':
			# Do something
			pass
		else:
			# Ignore
			pass


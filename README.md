# pybasicwiki
Very simple wiki parser. I created this for a cherrypy project so that I can document things online rather than hard editing template files. Wiki syntax is similar to MediaWiki but very simplified.

To use it:

	from pybasicwiki import basicwiki, HTMLFormatter
	def linker(href, text):
		# Do something here to check if it's a wiki page to link internally, otherwise link externally?
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

Supported syntax:
- ''italics''
- '''bold'''
- ''''italics and bold'''''
- =H1 header=
- ==H2 header==
- ===H3 header===
- ====H4 header====
- =====H5 header=====
- [[Link to a page]]
- [[Link to a page|Short text]]
- ---- (a horizontal rule)


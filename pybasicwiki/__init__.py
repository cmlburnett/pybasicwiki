import re

class HTMLFormatter:
	def __init__(self, linkresolver):
		self._linkresolver = linkresolver

	def __call__(self, t):
		props = dir(self)
		if t.name() in props:
			f = getattr(__class__, t.name())
			return f(self, t)
		else:
			raise KeyError("Attempted to format token %s but no function found to format it" % t.name())

	def text(self, t):
		return t.text()

	def newline(self, t):
		return "<br /><br />"

	def italic(self, t):
		return "<em>%s</em>" % t.text()

	def bold(self, t):
		return "<b>%s</b>" % t.text()

	def bolditalic(self, t):
		return "<em><b>%s</b></em>" % t.text()

	def hr(self, t):
		return "<hr />"

	def h1(self, t): return "<h1>%s</h1>" % t.text()

	def h2(self, t): return "<h2>%s</h2>" % t.text()

	def h3(self, t): return "<h3>%s</h3>" % t.text()

	def h4(self, t): return "<h4>%s</h4>" % t.text()

	def h5(self, t): return "<h5>%s</h5>" % t.text()

	def link(self, t):
		r = self._linkresolver(t.link(), None)
		return '<a href="%s">%s</a>' % (r[0], r[1])

	def linktxt(self, t):
		r = self._linkresolver(t.link(), t.text())
		return '<a href="%s">%s</a>' % (r[0], r[1])

class basicwiki:
	class newline:
		def __str__(self): return "newline()"
		def __repr__(self): return str(self)
		def name(self): return 'newline'

	class hr:
		def __str__(self): return "hr()"
		def __repr__(self): return str(self)
		def name(self): return 'hr'

	class text:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "text(%s, %d)" % (self._text, len(self._text))
		def __repr__(self): return str(self)
		def name(self): return 'text'
		def text(self): return self._text

	class italic:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "italic(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'italic'
		def text(self): return self._text

	class bold:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "bold(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'bold'
		def text(self): return self._text

	class bolditalic:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "bolditalic(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'bolditalic'
		def text(self): return self._text

	class h1:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "h1(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h1'
		def text(self): return self._text

	class h2:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "h2(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h2'
		def text(self): return self._text

	class h3:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "h3(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h3'
		def text(self): return self._text

	class h4:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "h4(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h4'
		def text(self): return self._text

	class h5:
		def __init__(self, txt):
			self._text = txt
		def __str__(self): return "h5(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h5'
		def text(self): return self._text

	class link:
		def __init__(self, url):
			self._url = url
		def __str__(self): return "link(%s)" % self._url
		def __repr__(self): return str(self)
		def name(self): return 'link'
		def link(self): return self._url
		def text(self): return None

	class linktxt:
		def __init__(self, url, txt):
			self._url = url
			self._text = txt
		def __str__(self): return "linktxt(%s,%s)" % (self._url, self._text)
		def __repr__(self): return str(self)
		def name(self): return 'linktxt'
		def link(self): return self._url
		def text(self): return self._text

	# Compile regular expressions in order of processing as some should be done in order
	res = [
		('h5', re.compile("""=====([^=]+)=====""")),
		('h4', re.compile("""====([^=]+)====""")),
		('h3', re.compile("""===([^=]+)===""")),
		('h2', re.compile("""==([^=]+)==""")),
		('h1', re.compile("""=([^=]+)=""")),
		('bolditalic', re.compile("""'''''([^']+)'''''""")),
		('bold', re.compile("""'''([^']+)'''""")),
		('italic', re.compile("""''([^']+)''""")),
		('hr', re.compile('^----$')),
		('linktxt', re.compile('\\[\\[([^]]+)[|]([^]]+)\\]\\]')),
		('link', re.compile('\\[\\[([^]]+)\\]\\]')),
	]

	@staticmethod
	def parseFormatter(txt, formatter):
		ret = []
		for t in __class__.parse(txt):
			ret.append( formatter(t) )

		return "".join(ret)

	@staticmethod
	def parse(txt):
		"""Tokenize and generate tokens as a generator"""
		final = []
		lines = txt.split('\n')
		for line in lines:
			ret = __class__.tokenize(line)
			final += ret

		for t in final:
			yield t

	@staticmethod
	def tokenize(txt):
		"""Tokenize the string @txt into a list of tokens"""

		#print('Tokenize "%s"' % txt)
		if not len(txt):
			return [__class__.newline()]

		ret = []
		matches = False
		for k,v in __class__.res:
			r = v.search(txt)
			if r:
				s = r.span()
				#print(['hit', k, r, s])
				if s[0] != 0:
					#print(['pre', s[0], txt[0:s[0]]])
					pre = __class__.tokenize(txt[0:s[0]])
					ret += pre

				if k == 'italic':
					matches = True
					ret.append(__class__.italic( r.group(1) ))
				elif k == 'bold':
					matches = True
					ret.append(__class__.bold( r.group(1) ))
				elif k == 'bolditalic':
					matches = True
					ret.append(__class__.bolditalic( r.group(1) ))
				elif k == 'h1':
					matches = True
					ret.append(__class__.h1( r.group(1) ))
				elif k == 'h2':
					matches = True
					ret.append(__class__.h2( r.group(1) ))
				elif k == 'h3':
					matches = True
					ret.append(__class__.h3( r.group(1) ))
				elif k == 'h4':
					matches = True
					ret.append(__class__.h4( r.group(1) ))
				elif k == 'h5':
					matches = True
					ret.append(__class__.h5( r.group(1) ))
				elif k == 'hr':
					matches = True
					ret.append(__class__.hr())
				elif k == 'link':
					matches = True
					ret.append(__class__.link( r.group(1) ))
				elif k == 'linktxt':
					matches = True
					ret.append(__class__.linktxt( r.group(1),r.group(2) ))
				else:
					raise ValueError("Unrecognized token name '%s' for '%s'" % (k, txt))

				if s[1] < len(txt):
					#print(['post', s[1], len(txt), txt[s[1]:]])
					post = __class__.tokenize(txt[s[1]:])
					ret += post

				if matches:
					break

		if not matches:
			ret.append( __class__.text(txt) )

		return ret

__all__ = ['basicwiki', 'HTMLFormatter']


import re

class HTMLFormatter:
	def __init__(self, linkresolver):
		self._linkresolver = linkresolver
		self.priortoken = None
		self.priortokennonnewline = None

	def __call__(self, t):
		props = dir(self)
		if t.name() in props:
			ret = ""

			if isinstance(t, basicwiki.newline) and isinstance(self.priortoken, basicwiki.newline):
				if isinstance(self.priortokennonnewline, basicwiki.ul):
					ret += "</li></ul>\n"
				elif isinstance(self.priortokennonnewline, basicwiki.ol):
					ret += "</li></ol>\n"
				elif isinstance(self.priortokennonnewline, basicwiki.tab):
					ret += "</blockquote>\n"

			if isinstance(self.priortoken, basicwiki.newline) and isinstance(t, basicwiki.newline):
				self.priortokennonnewline = None

			print([t, self.priortoken, self.priortokennonnewline])

			kls = type(self)
			f = getattr(kls, t.name())
			ret += f(self, t)

			# Save the prior token and prior non-newline token
			self.priortoken = t
			if isinstance(t, basicwiki.ul) or isinstance(t, basicwiki.ol) or isinstance(t, basicwiki.tab):
				self.priortokennonnewline = t

			return ret
		else:
			raise KeyError("Attempted to format token %s but no function found to format it" % t.name())

	def eol(self, t):
		if isinstance(self.priortokennonnewline, basicwiki.ul):
			return "</ul>"
		elif isinstance(self.priortokennonnewline, basicwiki.ol):
			return "</ol>"
		elif isinstance(self.priortokennonnewline, basicwiki.tab):
			return "</blockquote>"
		else:
			return ""

	def text(self, t):
		# Text is striped of whitespace but one space back to separate from links, etc
		return " " + t.text() + " "

	def newline(self, t):
		if isinstance(self.priortoken, basicwiki.newline):
			if isinstance(self.priortoken, basicwiki.newline):
				return "<br />\n"
			else:
				return "\n"
		else:
			return "\n"

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

	def ul(self, t):
		if isinstance(self.priortokennonnewline, basicwiki.ul):
			if self.priortokennonnewline.level() == t.level():
				return "</li><li>"
			elif self.priortokennonnewline.level() < t.level():
				return "\n<ul>\n<li>"
			else:
				return "</li>\n</ul>\n</li>\n<li>"
		else:
			return "<ul>\n<li>"

	def ol(self, t):
		if isinstance(self.priortokennonnewline, basicwiki.ol):
			if self.priortokennonnewline.level() == t.level():
				return "<li>"
			elif self.priortokennonnewline.level() < t.level():
				return "\n<ol>\n<li>"
			else:
				return "</li>\n</ol>\n</li>\n<li>"
		else:
			return "<ol>\n<li>"

	def tab(self, t):
		if isinstance(self.priortokennonnewline, basicwiki.tab):
			if self.priortokennonnewline.level() == t.level():
				return ""
			elif self.priortokennonnewline.level() < t.level():
				return "\n<blockquote>"
			else:
				return "</blockquote>"
		else:
			return "<blockquote>"

	def link(self, t):
		r = self._linkresolver(t.link(), None)
		return '<a href="%s">%s</a>' % (r[0], r[1])

	def linktxt(self, t):
		r = self._linkresolver(t.link(), t.text())
		return '<a href="%s">%s</a>' % (r[0], r[1])

	def signature(self, t):
		raise NotImplementedError("Need to subclass this to handle signatures")

class basicwiki:
	class EOL:
		def __str__(self): return "eol()"
		def __repr__(self): return str(self)
		def name(self): return 'eol'

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
			self._text = txt.strip()
		def __str__(self): return "text(%s, %d)" % (self._text, len(self._text))
		def __repr__(self): return str(self)
		def name(self): return 'text'
		def text(self): return self._text

	class italic:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "italic(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'italic'
		def text(self): return self._text

	class bold:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "bold(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'bold'
		def text(self): return self._text

	class bolditalic:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "bolditalic(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'bolditalic'
		def text(self): return self._text

	class h1:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "h1(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h1'
		def text(self): return self._text

	class h2:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "h2(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h2'
		def text(self): return self._text

	class h3:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "h3(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h3'
		def text(self): return self._text

	class h4:
		def __init__(self, txt):
			self._text = txt.strip()
		def __str__(self): return "h4(%s)" % self._text
		def __repr__(self): return str(self)
		def name(self): return 'h4'
		def text(self): return self._text

	class h5:
		def __init__(self, txt):
			self._text = txt.strip()
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
			self._text = txt.strip()
		def __str__(self): return "linktxt(%s,%s)" % (self._url, self._text)
		def __repr__(self): return str(self)
		def name(self): return 'linktxt'
		def link(self): return self._url
		def text(self): return self._text

	class ul:
		def __init__(self, lvl):
			self._level = lvl
		def __str__(self): return "ul(%d)" % (self._level,)
		def __repr__(self): return str(self)
		def name(self): return "ul"
		def level(self): return self._level

	class ol:
		def __init__(self, lvl):
			self._level = lvl
		def __str__(self): return "ol(%d)" % (self._level,)
		def __repr__(self): return str(self)
		def name(self): return "ol"
		def level(self): return self._level

	class signature:
		def __init__(self): pass
		def __str__(self): return "signature()"
		def __repr__(self): return str(self)
		def name(self): return "signature"

	class tab:
		def __init__(self, lvl):
			self._level = lvl
		def __str__(self): return "tab(%d)" % (self._level,)
		def __repr__(self): return str(self)
		def name(self): return "tab"
		def level(self): return self._level

	# Compile regular expressions in order of processing as some should be done in order
	res = [
		# Accept ordered and unordered lists at the start of a line
		('ul', re.compile('^(\*+)[ ]*')),
		('ol', re.compile('^(\#+)[ ]*')),

		('h5', re.compile("""^=====([^=]+)=====$""")),
		('h4', re.compile("""^====([^=]+)====$""")),
		('h3', re.compile("""^===([^=]+)===$""")),
		('h2', re.compile("""^==([^=]+)==$""")),
		('h1', re.compile("""^=([^=]+)=$""")),
		('bolditalic', re.compile("""'''''([^'']+)'''''""")),
		('bold', re.compile("""'''([^'']+)'''""")),
		('italic', re.compile("""''([^'']+)''""")),
		('hr', re.compile('^----$')),
		('linktxt', re.compile('\\[\\[([^|\]]+)[|]([^\]]+)\\]\\]([\S]*)')),
		('link', re.compile('\\[\\[([^\]]+)\\]\\]([\S]*)')),
		# Any number of tildes will capture signature
		('signature', re.compile('~{3,}')),
		# Accept tabs only at the start of a line
		('tab', re.compile('^(:{1,})')),
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
			final.append(__class__.newline())
		final.append(__class__.EOL())

		for t in final:
			#print(t)
			yield t

	@staticmethod
	def tokenize(txt):
		"""Tokenize the string @txt into a list of tokens"""

		print('Tokenize "%s"' % txt)
		if not len(txt):
			return []

		ret = []

		# First first match on the line
		first = None
		for k,v in __class__.res:
			r = v.search(txt)
			if r:
				if first is None:
					first = (r, k, v)
				else:
					if r.span()[0] < first[0].span()[0]:
						first = (r, k, v)

		if not first:
			# It's all text so single token of text()
			return [__class__.text(txt)]

		r = first[0]
		k = first[1]
		v = first[2]

		# Get rest of line
		pre = txt[0:r.span()[0]]
		post = txt[r.span()[1]:]

		# Everything before the token is text
		ret.append(__class__.text(pre))

		if k == 'italic':
			ret.append(__class__.italic( r.group(1) ))
		elif k == 'bold':
			ret.append(__class__.bold( r.group(1) ))
		elif k == 'bolditalic':
			ret.append(__class__.bolditalic( r.group(1) ))
		elif k == 'h1':
			ret.append(__class__.h1( r.group(1) ))
		elif k == 'h2':
			ret.append(__class__.h2( r.group(1) ))
		elif k == 'h3':
			ret.append(__class__.h3( r.group(1) ))
		elif k == 'h4':
			ret.append(__class__.h4( r.group(1) ))
		elif k == 'h5':
			ret.append(__class__.h5( r.group(1) ))
		elif k == 'hr':
			ret.append(__class__.hr())
		elif k == 'link':
			txt = r.group(1)
			if r.group(2) and len(r.group(2)):
				print(['---------------', r.group(2), '-------------'])
				ret.append(__class__.linktxt( r.group(1),r.group(1)+r.group(2) ))
			else:
				ret.append(__class__.link( r.group(1) ))
		elif k == 'linktxt':
			txt = r.group(2)
			if r.group(3) and len(r.group(3)):
				print(['---------------', r.group(3), '-------------'])
				txt += r.group(3)
			ret.append(__class__.linktxt( r.group(1),r.group(2) ))

		elif k == 'ul':
			ret.append(__class__.ul(len(r.group(1))))
		elif k == 'ol':
			ret.append(__class__.ol(len(r.group(1))))
		elif k == 'tab':
			ret.append(__class__.tab(len(r.group(1))))

		elif k == 'signature':
			ret.append(__class__.signature())

		else:
			raise ValueError("Unrecognized token name '%s' for '%s'" % (k, txt))

		# Process everything left in the line
		ret += __class__.tokenize(post)

		return ret

__all__ = ['basicwiki', 'HTMLFormatter']


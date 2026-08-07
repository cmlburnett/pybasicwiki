import re

class HTMLFormatter:
	def __init__(self, linkresolver):
		self._linkresolver = linkresolver
		self.priortoken = None
		self.priortokennonnewline = None

		self._template = None
		self._template_tokens = []

	def __call__(self, t, parserobj, ignoretemplate=False):
		"""
		Call when to form a token @t.
		The parser object @parserobj is used when needing to recursively parse (eg, templates).
		Provide @ignoretemplate as True when the token should just be processed even within a template; in fact, this is necessary when parsing tokens within the template overtwise everything gets double-stacked.
		"""

		props = dir(self)
		if t.name() in props:
			# Within a template, so defer rendering to HTML until the end of the template is found
			if self._template is not None and not isinstance(t, basicwiki.templateend) and not ignoretemplate:
				self._template_tokens.append(t)
				return ""

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

			#print([t, self.priortoken, self.priortokennonnewline])

			kls = type(self)
			f = getattr(kls, t.name())
			ret += f(self, t, parserobj)

			# Save the prior token and prior non-newline token
			self.priortoken = t
			if isinstance(t, basicwiki.ul) or isinstance(t, basicwiki.ol) or isinstance(t, basicwiki.tab):
				self.priortokennonnewline = t

			return ret
		else:
			raise KeyError("Attempted to format token %s but no function found to format it" % t.name())

	def eol(self, t, parserobj):
		if isinstance(self.priortokennonnewline, basicwiki.ul):
			return "</ul>"
		elif isinstance(self.priortokennonnewline, basicwiki.ol):
			return "</ol>"
		elif isinstance(self.priortokennonnewline, basicwiki.tab):
			return "</blockquote>"
		else:
			return ""

	def text(self, t, parserobj):
		# Text is striped of whitespace but one space back to separate from links, etc
		return t.text()

	def newline(self, t, parserobj):
		if isinstance(self.priortoken, basicwiki.newline):
			if isinstance(self.priortoken, basicwiki.newline):
				return "<br />\n"
			else:
				return "\n"
		else:
			return "\n"

	def italic(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<em>%s</em>" % ''.join(mid)

	def bold(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<b>%s</b>" % ''.join(mid)

	def bolditalic(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<em><b>%s</b></em>" % ''.join(mid)

	def hr(self, t, parserobj):
		return "<hr />"

	def h1(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<h1>%s</h1>" % ''.join(mid)

	def h2(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<h2>%s</h2>" % ''.join(mid)

	def h3(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<h3>%s</h3>" % ''.join(mid)

	def h4(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<h4>%s</h4>" % ''.join(mid)

	def h5(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		return "<h5>%s</h5>" % ''.join(mid)

	def ul(self, t, parserobj):
		if isinstance(self.priortokennonnewline, basicwiki.ul):
			if self.priortokennonnewline.level() == t.level():
				return "</li><li>"
			elif self.priortokennonnewline.level() < t.level():
				return "\n<ul>\n<li>"
			else:
				return "</li>\n</ul>\n</li>\n<li>"
		else:
			return "<ul>\n<li>"

	def ol(self, t, parserobj):
		if isinstance(self.priortokennonnewline, basicwiki.ol):
			if self.priortokennonnewline.level() == t.level():
				return "<li>"
			elif self.priortokennonnewline.level() < t.level():
				return "\n<ol>\n<li>"
			else:
				return "</li>\n</ol>\n</li>\n<li>"
		else:
			return "<ol>\n<li>"

	def tab(self, t, parserobj):
		if isinstance(self.priortokennonnewline, basicwiki.tab):
			if self.priortokennonnewline.level() == t.level():
				return ""
			elif self.priortokennonnewline.level() < t.level():
				return "\n<blockquote>"
			else:
				return "</blockquote>"
		else:
			return "<blockquote>"

	def link(self, t, parserobj):
		r = self._linkresolver(t.link(), None)
		return '<a href="%s">%s</a>' % (r[0], r[1])

	def linktxt(self, t, parserobj):
		mid = [self(_, parserobj, ignoretemplate=True) for _ in t.text()]
		r = self._linkresolver(t.link(), ''.join(mid))
		return '<a href="%s">%s</a>' % (r[0], r[1])

	def template(self, title, params, parserobj):
		raise NotImplementedError("Need to subclass this to handle templates")

	def signature(self, t, parserobj):
		raise NotImplementedError("Need to subclass this to handle signatures")

	def templatestart(self, t, parserobj):
		if self._template is not None:
			raise ValueError("Attempted to template within a template, not supported (%s inside %s)" % (str(t), str(self._template)))
		self._template = t

		return ""

	def templateend(self, t, parserobj):
		kls = type(self)
		props = dir(self)

		if self._template is None:
			return "}}"
			#raise ValueError("Found end of template but not within a template")

		params = []
		for tt in self._template_tokens:
			if isinstance(tt, basicwiki.text):
				if len(tt.text()) == 0:
					continue

				parts = tt.text().split("|")
				for part in parts:
					# It's just more text, not a new parameter
					if '=' not in part:
						if not len(part): continue

						# If nothing there yet, just add it on as a string
						if not len(params):
							params.append(part)
						else:
							# If the last item is a string then concat
							if type(params[-1]) == str:
								params[-1] = params[-1] + part
							# Otherwise it's a named parameter so add the text on to the parameter value
							else:
								params[-1][-1] += part
					else:
						# Add a named parameter
						k,v = part.split('=',1)
						params.append( [k,v] )
			else:
				f = getattr(kls, tt.name())
				x = f(self, tt, parserobj)
				if len(params) and type(params[-1]) == list:
					params[-1][-1] += x
				else:
					params.append(x)

		# Template name/title
		title = self._template.title()

		# TODO: render all tokens since self._template as parameters to the template
		self._template = None
		self._template_tokens.clear()

		# Render template by supplying the template name/title and its parameters provided
		return self.template(title, params, parserobj)

	def tableofcontents(self, t, parserobj):
		# Default is to not show anything
		return ""

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

	class templatestart:
		def __init__(self, title):
			self._title = title
		def __str__(self): return "templatestart(%s)" % (self._title,)
		def __repr__(self): return str(self)
		def name(self): return "templatestart"
		def title(self): return self._title

	class templateend:
		def __init__(self): pass
		def __str__(self): return "templateend()"
		def __repr__(self): return str(self)
		def name(self): return "templateend"

	class tableofcontents:
		def __init__(self): pass
		def __str__(self): return "tableofcontents"
		def __repr__(self): return str(self)
		def name(self): return "tableofcontents"

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
		('bolditalic', re.compile("""'''''((?:[^']|'[^'])*?)'''''""")),
		('bold', re.compile("""'''((?:[^']|'[^'])*?)'''""")),
		('italic', re.compile("""''((?:[^']|'[^'])*?)''""")),
		# At least four hyphens but any number is a horizontal rule
		('hr', re.compile('^-{4,}$')),
		('linktxt', re.compile('\\[\\[([^|\]]+)[|]([^\]]+)\\]\\]([a-zA-Z0-9]*)')),
		('link', re.compile('\\[\\[([^\]]+)\\]\\]([a-zA-Z0-9]*)')),
		('templatestart', re.compile('\{\{([a-zA-Z0-9_ ]+)')),
		('templateend', re.compile('\}\}')),
		# Any number of consecutive tildes will capture signature
		('signature', re.compile('~{3,}')),
		# Accept tabs only at the start of a line
		('tab', re.compile('^(:{1,})')),
	]

	@staticmethod
	def parseFormatter(txt, formatter, token_analyzer=None):
		"""
		Parse the wiki text @txt into tokens, then format each token with @formatter.
		Prior to formatting, pass the tokens to the token analyzer @token_analyzer (can read, write, modify, prune, trim, delete, addend, etc the token stream) and must return a list of tokens.
		"""
		tokens = []
		for t in __class__.parse(txt):
			tokens.append(t)

		if token_analyzer:
			tokens = token_analyzer(tokens)
			if tokens is None:
				raise ValueError("Token analyzer %s did not return a list of tokens" % str(token_analyzer))

		html = [formatter(t, __class__) for t in tokens]

		return "".join(html)

	@staticmethod
	def parse(txt):
		"""Tokenize and generate tokens as a generator"""
		final = []
		lines = txt.split('\n')
		for line in lines:
			ret = __class__.tokenize(line, True)
			final += ret
			final.append(__class__.newline())
		final.append(__class__.EOL())

		found_first_header = False
		for t in final:
			# Find first header and inject a table of contents token
			if not found_first_header:
				if t.name() in ('h1','h2','h3','h4','h5'):
					found_first_header = True
					yield __class__.tableofcontents()
			yield t

	@staticmethod
	def tokenize(txt, truestartofline=False):
		"""Tokenize the string @txt into a list of tokens"""

		if not len(txt):
			return []

		ret = []

		# Permit matching to these only if @truestartofline is True
		startonly = ['ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'tab']

		# First first match on the line
		first = None
		for k,v in __class__.res:
			r = v.search(txt)

			# If not start of line, reject those that must be start of the line
			if k in startonly and not truestartofline:
				continue

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

		rs = r.span()

		# Get rest of line
		pre = txt[0:rs[0]]
		if len(r.groups()) > 0:
			intra = r.group(1)
		else:
			intra = None
		post = txt[rs[1]:]

		# Everything before the token is text
		ret.append(__class__.text(pre))

		if k == 'italic':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.italic(i))
		elif k == 'bold':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.bold(i))
		elif k == 'bolditalic':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.bolditalic(i))
		elif k == 'h1':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.h1(i))
		elif k == 'h2':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.h2(i))
		elif k == 'h3':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.h3(i))
		elif k == 'h4':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.h4(i))
		elif k == 'h5':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.h5(i))
		elif k == 'hr':
			i = __class__.tokenize(r.group(1))
			ret.append(__class__.hr())
		elif k == 'link':
			txt = r.group(1)
			if r.group(2) and len(r.group(2)):
				txt += r.group(2)
				ret.append(__class__.linktxt( r.group(1), [__class__.text(txt)] ))
			else:
				ret.append(__class__.link( r.group(1) ))
		elif k == 'linktxt':
			txt = r.group(2)
			if r.group(3) and len(r.group(3)):
				txt += r.group(3)

			i = __class__.tokenize(txt)
			ret.append(__class__.linktxt( r.group(1), i ))

		elif k == 'ul':
			ret.append(__class__.ul(len(r.group(1))))
		elif k == 'ol':
			ret.append(__class__.ol(len(r.group(1))))
		elif k == 'tab':
			ret.append(__class__.tab(len(r.group(1))))

		elif k == 'signature':
			ret.append(__class__.signature())

		elif k == 'templatestart':
			ret.append(__class__.templatestart(r.group(1)))
		elif k == 'templateend':
			ret.append(__class__.templateend())

		else:
			raise ValueError("Unrecognized token name '%s' for '%s'" % (k, txt))

		# Process everything left in the line
		ret += __class__.tokenize(post)

		return ret

__all__ = ['basicwiki', 'HTMLFormatter']


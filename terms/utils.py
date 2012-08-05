# coding: utf-8

from HTMLParser import HTMLParser


class NeutralHTMLReconstructor(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.out = []

    def concat_attrs(self, attrs):
        return ''.join(' %s="%s"' % (attr[0], attr[1]) for attr in attrs)

    def handle_startendtag(self, tag, attrs):
        attrs = self.concat_attrs(attrs)
        self.out.append('<%s%s />' % (tag, attrs))

    def handle_starttag(self, tag, attrs):
        attrs = self.concat_attrs(attrs)
        self.out.append('<%s%s>' % (tag, attrs))

    def handle_endtag(self, tag):
        self.out.append('</%s>' % tag)

    def handle_charref(self, name):
        self.out.append('&#%s;' % name)

    def handle_entityref(self, name):
        self.out.append('&%s;' % name)

    def handle_data(self, data):
        self.out.append(data)

    def handle_comment(self, data):
        self.out.append('<!--%s-->' % data)

    def handle_decl(self, decl):
        self.out.append('<!%s>' % decl)

    def handle_pi(self, data):
        self.out.append('<?%s>' % data)

    def unknown_decl(self, data):
        self.out.append('<![%s]>' % decl)

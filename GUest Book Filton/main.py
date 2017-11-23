#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")
    def post(self):
        sporocilo = self.request.get("message")
        podatki=self.request.get("ime")
        email_naslov=self.request.get("email")
        if not podatki:
            podatki="Neznanec"
        if "<script>" in sporocilo:
            return self.write("Ne mores me :p")
        message=Message(text=sporocilo, name=podatki, meil=email_naslov)
        message.put()
        return self.write(message)

class MessageHandler(BaseHandler):
    def get(self):
        messages=Message.query().fetch()
        params={"message_list": messages}
        return self.render_template("message_list.html", params=params)

class MessageShowHandler(BaseHandler):
    def get(self, id):
        message=Message.get_by_id(int(id))
        params={"message":message}
        return self.render_template("message.html", params=params)






app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/messages', MessageHandler),
    webapp2.Route('/message/<id:\d+>', MessageShowHandler),
], debug=True)

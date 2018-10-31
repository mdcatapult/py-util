# -*- coding: utf-8 -*-
import re

class Detect:

    mimetype = ""
    html = re.compile("(text/(html))|(application/x(html).*)")
    rtf = re.compile("(text/(rtf))")
    calendar = re.compile("(text/(calendar))")
    text = re.compile("(text/.*)")


    def __init__(self, mimetype):
        self.mimetype = mimetype


    def is_html(self):
        return self.html.match(self.mimetype)


    def is_rtf(self):
        return self.rtf.match(self.mimetype)
    

    def is_calendar(self):
        return self.calendar.match(self.mimetype)
    

    def is_text(self):
        return self.text.match(self.mimetype)
    

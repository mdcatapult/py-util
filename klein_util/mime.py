# -*- coding: utf-8 -*-
import re

class Detect:

    mimetype = ""
    html = re.compile("(text/(html))|(application/x(html).*)")
    rtf = re.compile("(text/(rtf))")
    calendar = re.compile("(text/(calendar))")
    text = re.compile("(text/.*)")
    archive = re.compile("application/(gzip|vnd.ms-cab-compressed|x-(7z-compressed|ace-compressed|alz-compressed|apple-diskimage|arj|astrotite-afa|b1|bzip2|cfs-compressed|compress|cpio|dar|dgc-compressed|gca-compressed|gtar|lzh|lzip|lzma|lzop|lzx|par2|rar-compressed|sbx|shar|snappy-framed|stuffit|stuffitx|tar|xz|zoo)|zip)")

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

    def is_archive(self):
        return self.archive.match(self.mimetype)
    

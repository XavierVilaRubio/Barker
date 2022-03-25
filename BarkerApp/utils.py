import re
from django.utils.safestring import mark_safe

def parseLinks(text):
    match = re.search("(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", text)
    if match:
        # print(match.span())
        values = match.span()
        start = values[0]
        end = values[1]
        # print(text[0: start])
        # print(match.group())
        # print(text[end+1: -1])
        return mark_safe("{before_link}<a href='{link}'>{link}</a> {after_link}".format(before_link=text[0: start], link=match.group(), after_link=parseLinks(text[end+1:])))
    return text
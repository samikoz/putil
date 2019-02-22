"""handlers to use with xml.sax module.
have to inherit from ContentHandler, DTDHandler, EntityResolver or ErrorHandler.

to be passed e.g. to xml.sax.parseString method
the outcome will be stored within the handler."""

import xml.sax


class SingleTagHandler(xml.sax.handler.ContentHandler):
    """handler extracting the content from a single xml tag.
    without explicit clearing the content from multiple tags is concatenated."""

    # TODO write new handler based on DOM-tree
    # TODO extend the below one to make parent optional then this one is redundant
    def __init__(self, tagname):
        super().__init__()

        self.__content = ''
        self.__current_tag = None
        self.__tagname = tagname

    def startElement(self, name, attrs):
        self.__current_tag = name

    def endElement(self, name):
        self.__current_tag = None

    def characters(self, content):
        if self.__current_tag == self.__tagname:
            self.__content += content

    def clear_content(self):
        self.__content = ''

    def get_parsed(self):
        return self.__content


class SingleTagChildrenHandler(xml.sax.handler.ContentHandler):
    """handler parsing specified children tags within a given parent tag.
    it allows for execution of callbacks when parsing these.
    without explicit clearing the content from multiple tags is concatenated."""

    def __init__(self, parent_tag, children_tags, callbacks):
        """
        :param callbacks: a dict with the following keys:
            - child_start(handler, tagname, attributes)
            - child_end(handler, tagname)
            - parent_start(handler, tagname, attributes)
            - parent_end(handler, tagname)
        """
        super().__init__()

        self.__parent = parent_tag
        self.__children = children_tags

        # TODO vacuous functions rather than None
        self.__child_start_callback = callbacks.get('child_start', None)
        self.__child_end_callback = callbacks.get('child_end', None)
        self.__parent_start_callback = callbacks.get('parent_start', None)
        self.__parent_end_callback = callbacks.get('parent_end', None)

        self.__current_tag = None
        self.__current_parent_tag = None
        self.__content = {child_tag: '' for child_tag in children_tags}

    def startElement(self, name, attrs):
        self.__current_tag = name

        if name == self.__parent:
            self.__current_parent_tag = name
            if self.__parent_start_callback:
                self.__parent_start_callback(self, attrs)

        elif (name in self.__children and self.__current_parent_tag == self.__parent
              and self.__child_start_callback):
            self.__child_start_callback(self, name, attrs)

    def endElement(self, name):
        self.__current_tag = None

        if name == self.__parent:
            self.__current_parent_tag = None
            if self.__parent_end_callback:
                self.__parent_end_callback(self, name)

        elif (name in self.__children and self.__current_parent_tag == self.__parent
              and self.__child_end_callback):
            self.__child_end_callback(self, name)

    def characters(self, content):
        if self.__current_tag in self.__children:
            self.__content[self.__current_tag] += content

    def get_parsed_child(self, tagname):
        return self.__content[tagname]

    def clear_parsed_child(self, tagname):
        self.__content[tagname] = ''

    def clear_content(self):
        for child in self.__children:
            self.clear_parsed_child(child)

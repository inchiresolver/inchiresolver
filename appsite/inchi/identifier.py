import re
import uuid


class InChI:
    DEFAULT_VERSION = '1'
    DEFAULT_PREFIX = "InChI="
    PATTERN_STRING = '^(?P<version>.{1,2})/(?P<layers>.+$)'
    PATTERN_STRING_WITH_PREFIX = '^(?P<prefix>%s)(?P<version>.{1,2})/(?P<layers>.+$)' % DEFAULT_PREFIX

    def __init__(self, string=None):
        self.element = {'string': string}
        patternList = [InChI.PATTERN_STRING, InChI.PATTERN_STRING_WITH_PREFIX]
        if not bool([self._validate(string, pattern) for pattern in patternList if self._validate(string, pattern)]):
            raise InChIError('string is not resolvable')
        [setattr(self, k, v) for k, v in self.element.items()]

    def _validate(self, string, pattern_string):
        pattern = re.compile(pattern_string)
        match = pattern.search(string)
        if match:
            identifier = match.groupdict()
            self.element = identifier
            self.element['prefix'] = InChI.DEFAULT_PREFIX
            self.element['is_standard'] = self.element['version'][-1:] == 'S'
            self.element['version'] = self.element['version'][:1]
            if self.element['is_standard']:
                self.element['well_formatted'] = '%s%sS/%s' % (
                self.element['prefix'], self.element['version'], self.element['layers'])
            else:
                self.element['well_formatted'] = '%s%s/%s' % (
                self.element['prefix'], self.element['version'], self.element['layers'])
            # self.element['html_formatted'] = self.element['well_formatted'].replace('-','-<wbr>')
            return True
        return False

    def __eq__(self, other):
        selfh = self.element['well_formatted']
        otherh = self.element['well_formatted']
        return selfh == otherh

    def __str__(self):
        return self.element['well_formatted']




class InChIKey:
    DEFAULT_PREFIX = "InChIKey="
    PATTERN_STRING = '(?P<block1>[A-Z]{14})-(?P<block2>[A-Z]{8}(S|N)[A-Z]{1})-(?P<block3>[A-Z]{1}$)'
    PATTERN_STRING_WITH_PREFIX = '(?P<prefix>^%s)(?P<block1>[A-Z]{14})-(?P<block2>[A-Z]{8}(S|N)[A-Z]{1})-(?P<block3>[A-Z]{1}$)' % DEFAULT_PREFIX

    def __init__(self, string=None, block1=None, block2=None, block3=None):
        if string is None and block1 is not False:
            string = block1
            if block2:
                string += "-%s" % block2
            if block2 and block3:
                string += "-%s" % block3

        self.element = {'string': string}
        patternList = [InChIKey.PATTERN_STRING, InChIKey.PATTERN_STRING_WITH_PREFIX]
        if not bool([self._validate(string, pattern) for pattern in patternList if self._validate(string, pattern)]):
            raise InChIKeyError('InChIKey is not resolvable')
        [setattr(self, k, v) for k, v in self.element.items()]

    def _validate(self, string, pattern_string):
        pattern = re.compile(pattern_string)
        match = pattern.search(string)
        if match:
            identifier = match.groupdict()
            self.element = identifier
            self.element['prefix'] = InChIKey.DEFAULT_PREFIX
            self.element['version'] = ord(self.element['block2'][-1:]) - 64
            self.element['is_standard'] = self.element['block2'][-2:-1] == 'S'
            self.element['blocks'] = (self.element['block1'], self.element['block2'], self.element['block3'])
            self.element['well_formatted'] = '%s%s-%s-%s' % (
                self.element['prefix'], self.element['block1'], self.element['block2'], self.element['block3'])
            self.element['well_formatted_no_prefix'] = '%s-%s-%s' % (
                self.element['block1'], self.element['block2'], self.element['block3'])
            return True
        return False

    def __eq__(self, other):
        selfh = self.element['well_formatted_no_prefix']
        otherh = self.element['well_formatted_no_prefix']
        return selfh == otherh


    def __str__(self):
        return self.element['well_formatted_no_prefix']


class InChIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InChIKeyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

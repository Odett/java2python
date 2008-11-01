#!/usr/bin/env python
# -*- coding: utf-8 -*-
from java2python.sourcetypes.block import Block, maybeAttr


class Method(Block):
    """ Method -> specialized block type

    """
    instanceFirstParam = ('object', 'self')
    classFirstParam = ('type', 'cls')

    def __init__(self, parent, name):
        Block.__init__(self, parent=parent, name=name)
        self.parameters = [self.instanceFirstParam, ]
        self.addSource('pass')

    def dump(self, output, indent):
        """ writes the string representation of this block

        @param output any writable file-like object
        @param indent indentation level of this block
        @return None
        """
	config = self.config
        offset = self.I(indent)
        if config.last('writeModifiersComments') and self.modifiers:
            output.write('%s## modifiers: %s\n' % (offset, str.join(', ', self.modifiers)))
        sorter = config.last('methodPreambleSorter')
        if sorter:
            self.preamble.sort(sorter)
        for obj in self.preamble:
            output.write('%s%s\n' % (offset, obj))
        output.write('%s\n' % (self.formatDecl(indent), ))
        writedoc = config.last('writeMethodDocString')
        if writedoc:
            docoffset = self.I(indent+1)
            output.write('%s""" generated source for %s\n\n' % \
                         (docoffset, self.name))
            output.write('%s"""\n' % (docoffset, ))
        Block.dump(self, output, indent+1)
        output.write('\n')

    @property
    def isMethod(self):
        """ True if this instance is a Method

        """
	return True

    def addModifier(self, name):
        """ adds named modifier to method

        If the modifier corresponds to a decorator, that decorator is
        inserted into the method preamble instead.

        @param name modifier as string
        @return None
        """
        try:
            deco = self.config.combined('modifierDecoratorMap')[name]
        except (KeyError, ):
            pass
        else:
            if deco not in self.preamble:
                self.preamble.append(deco)
                if (deco == self.classmethodLiteral) and (self.parameters) \
                       and (self.parameters[0] == self.instanceFirstParam):
                    self.parameters[0] = self.classFirstParam
        Block.addModifier(self, name)

    def addParameter(self, typ, name):
        """ adds named parameter to method

        @param typ parameter type as string
        @param name parameter name as string
        @return None
        """
        name = self.alternateName(name)
        typ = Block.alternateName(self, typ, 'typeTypeMap')
        self.parameters.append((typ, name))
        #self.addVariable(Variable(self, name))
        self.addVariable(name)

    def formatDecl(self, indent):
        """ generates a class statement accounting for base types

        @param indent indentation level of this block
        @return class declaration as string
        """
        name = self.alternateName(self.name)
        parameters = self.parameters
        minparam = self.config.last('minIndentParams', 0)
        if minparam and len(parameters) > minparam:
            first, others = parameters[0], parameters[1:]
            prefix = '%sdef %s(%s, ' % (self.I(indent), name, first[1], )
            offset = '\n' + (' ' * len(prefix))
            decl = '%s%s):' % (prefix, str.join(','+offset, [o[1] for o in others]))
        else:
            params = str.join(', ', [p[1] for p in parameters])
            decl = '%sdef %s(%s):' % (self.I(indent), name, params)
        return decl

    def alternateName(self, name):
        """ returns an alternate for given name

        @param name any string
        @return alternate for name if found; if not found, returns name
        """
        mapping = self.config.combined('renameMethodMap')
        try:
            return mapping[name]
        except (KeyError, ):
            return Block.alternateName(self, name)


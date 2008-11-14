#!/usr/bin/env python
# -*- coding: utf-8 -*-

## number of spaces to indent each block
indent = 4

## prefix for comments
commentPrefix = '## '

## move inner class definitions to the top of their outer class.
## allows the outer class to reference the inner class definition
## later in its definition.
bubbleInnerClasses = True

## minimum parameter count to trigger indentation of parameter names
## in method declarations.  set to 0 to disable.
minIndentParams = 5

commentHandlers = [
    # javadoc2docstring
    # javadoc2pythondoc
    'java2python.modes.simpleComments',
    ]

## this value controls how enums are created, if at all.  the default
## creates enums as classes with minimum support for the interface and
## behavior defined for java classes.  in the modes.enums module, the
## other usable functions are or fullJava, pyInts, pyStrings and
## subClass.
enumConstantHandlers = [
    'java2python.modes.enums.pyInts',
    #'java2python.modes.enums.minJava',
    ]

## the default import statement handler converts them to comment.
importHandlers = [
    'java2python.modes.commentImport',
    ]

## similarly, package statements are also converted to comments.
packageHandlers = [
    'java2python.modes.commentPackage',
    #'java2python.modes.setupToolsPackage',
    #'java2python.modes.setupToolsPackageComment',
    ]

## these functions finish the construction of a class block.
classHandlers = [

    ## with this handler, classes are scanned for duplicate method
    ## names.  matching methods are augmented with the '@overloaded'
    ## decorator.
    'java2python.modes.classes.fixOverloadMethods',

    'java2python.modes.classes.fixCtor',

    ## this function scans the class for methods that look like
    ## accessors.  matching methods are renamed and declared as
    ## properties.
    'java2python.modes.classes.fixPropMethods',

    ## this function sorts sorts class methods by name.
    'java2python.modes.classes.sortClassMethods',

    ## this function inserts a simple docstring at the beginning of
    ## the class definition.
    'java2python.modes.simpleDocString',

    'java2python.modes.classes.insertModifiers',

    'java2python.modes.classes.fixBaseClasses',
    ]

## these functions complete the construction of method blocks.
methodHandlers = [
    ## this function inserts a simple docstring at the beginning of
    ## the class definition.
    'java2python.modes.simpleDocString',

    ## this function adds a comment with the original function's
    ## modifiers.
    'java2python.modes.methods.insertReturn',
    'java2python.modes.methods.insertModifiers',
    ]


## these functions are writers; they're called to write directly to an
## output when a module is dumped.  they use the modulePreamble and
## moduleEpilogue values below.
modulePreambleWriters = [
    'java2python.modes.modules.preamble',
    ]


moduleEpilogueWriters = [
    'java2python.modes.modules.epilogue',
    ## with this function, if the source contains a "public static
    ## void main" method, a block is written to the end of the file to
    ## call the class method with sys.argv.
    'java2python.modes.modules.ifMainScript',
    ]


## Note about modulePreamble and moduleEpilogue:
##
## Items in both of these lists may be strings or callables.  If
## they're callables, they should take a single argument.  The Module
## object will be passed as this single argument in the case of
## callables.

## lines written at the beginning of each generated module.  this value
## is cumulative, so when user-defined configuration modules specify
## this value, those lines are written after these.
modulePreamble = [
    '#!/usr/bin/env python',
    '# -*- coding: utf-8 -*-',
    '',
    ]

## lines written at the end of each generated module.  this value is
## cumulative, so user-defined configuration modules may specify
## additional values.
moduleEpilogue = [
    ]

## regular expression substitutions performed on source after
## generation but before final output.  this value is cumulative, so
## user-defined configuration modules can add augment these with their
## own.  each value in this list is a two-tuple of (pattern, repl).
## see the 're' module docs, specifically the re.sub function.
outputSubs = [
    (r'(\.self\.)', '.'),
    (r'String\.valueOf\((.*?)\)', r'str(\1)'),
    (r'System\.out\.println\((.*)\)', r'print \1'),
    (r'System\.out\.print_\((.*?)\)', r'print \1,'),
    (r'(.*?)\.equals\((.*?)\)', r'\1 == \2'),
    (r'(.*?)\.equalsIgnoreCase\((.*?)\)', r'\1.lower() == \2.lower()'),
    (r'([\w.]+)\.size\(\)', r'len(\1)'),
    (r'(\w+)\.get\((.*?)\)', r'\1[\2]'),
    (r'(\s)(\S*?)(\.toString\(\))', r'\1str(\2)'),

    (r'(\s)(\S*?)(\.toLowerCase\(\))', r'\1\2.lower()'),

    (r'(\s)(\S*?)(\.length\(\))', r'\1len(\2)'),
    (r'(.*?)IndexOutOfBoundsException\((.*?)\)', r'\1IndexError(\2)'),
    ]

## mapping of java type names to python type names.  user-defined
## configuration modules can replace and/or augment this mapping.
typeTypeMap = {
    'String':'str',
    'Integer':'int',
    'Object':'object',
    'int':'int',
    'double':'float',
    'Vector':'list',
    'boolean':'bool',
    'char':'str',
    '[':'list',
}

## mapping of java type values to python type values.  user-defined
## configuration modules can replace and/or augment this mapping.
typeValueMap = {
    'String':'""',
    'int':'0',
    'double':'0.0',
    'Vector':'[]',
    'boolean':'False',
    'str':'""',
    '[':'None',
}

## method name mapping.  user-defined configuration modules can
## replace and/or augment this with their own.
renameMethodMap = {
    'equals':'__eq__',
    'and':'and_',
    'del':'del_',
    'elif':'elif_',
    'from':'from_',
    'in':'in_',
    'is':'is_',
    'not':'not_',
    'or':'or_',
    'print':'print_',
}

## generic name mapping.  user-defined configuration modules can
## replace and/or augment this with their own.
renameAnyMap = {
    'this':'self',
    'null':'None',
    'false':'False',
    'true':'True',
    'and':'and_',
    'del':'del_',
    'elif':'elif_',
    'from':'from_',
    'in':'in_',
    'is':'is_',
    'not':'not_',
    'or':'or_',
    'print':'print_',
    'str':'strval',
}

## method type modifier mapping.  when input methods have modifiers
## with matching names, those names are replaced with their
## corresponding statements from this mapping.  this value can be
## replaced and/or augmented via user-defined configuration modules.
modifierDecoratorMap = {
    'synchronized':'@synchronized(mlock)',
    'static':'@classmethod',
}


baseClassMembers = {
    'Thread':['MAX_PRIORITY', 'MIN_PRIORITY', 'NORM_PRIORITY',
              'activeCount', 'checkAccess', 'countStackFrames',
              'currentThread', 'destroy', 'dumpStack',
              'enumerate', 'getContextClassLoader', 'getName',
              'getPriority', 'getThreadGroup', 'holdsLock',
              'interrupt', 'interrupted', 'isAlive',
              'isDaemon', 'isInterrupted', 'join',
              'resume', 'run', 'setContextClassLoader',
              'setDaemon', 'setName', 'setPriority',
              'sleep', 'start', 'stop', 'suspend', 'toString', 'yield',
              ],
}


def make_variableNameMapping():
    import keyword, __builtin__
    return dict((k, '%s_' % k) for k in keyword.kwlist + __builtin__.__dict__.keys())
variableNameMapping = make_variableNameMapping()


exceptionTypeMapping = {
    'NoSuchFieldError':'AttributeError',
    'NoSuchMethodException':'AttributeError',
    }


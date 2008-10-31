#!/usr/bin/env python
import logging

logging.basicConfig(level=logging.DEBUG)
debug = logging.debug
## yes, one of those
marker = object()


class SimplePythonSourceStack(object):
    def __init__(self, module):
	self.stack = [module]

    def get_current(self):
	return self.stack[-1]
    current = property(get_current)


    def onPackageDecl(self, name):
	self.current.addComment("namespace_packages('%s')" % name)


    def onImportDecl(self, name, isStatic, isStar):
	if isStatic:
	    if isStar:
		c = "from %s import *" % name
	    else:
		names = name.split('.')
		c = "from %s import %s" % (str.join('.', names[:-1]), names[-1])
	else:
	    c = "import %s" % name
	self.current.addComment(c)

    def onBreak(self, label):
        debug("onBreak %s", label)
        self.current.addSource('break' + (' #label:' + label if label else ''))

    def onContinue(self, label):
        debug("onContinue %s", label)
        self.current.addSource('continue' + (' # ' + label if label else ''))

    def onClass(self, name, mods=None, extends=None, implements=None):
	debug("onClass %s %s %s %s", name, mods, extends, implements)
	klass = self.current.newClass()
	klass.name = name

	def annoDecl(v):
	    s = []
	    for d in v:
		for k in d:
		    if len(k) == 2:
			s.append("%s=%s" % tuple(k))
		    else:
			s.append(k)
	    return ", ".join(s)

	for mod in (mods or []):
	    if isinstance(mod, basestring):
                klass.addModifier(mod)
	    elif isinstance(mod, list):
		name, inits = mod
		if inits:
		    suffix = "(" + annoDecl(inits) +  ")"
		else:
		    suffix = ""
		name += suffix
		klass.addModifier("@" + name)

	for base in (extends or []) + (implements or []):
	    klass.addBaseClass(base)
	self.push(klass)
	return klass

    def onForEach(self, typ, ident, exp):
        debug("onForEach %s %s %s", typ, ident, exp)
        blk, stat = self.current.newForEach()
        stat.setExpression("%s in %s" % (ident, exp))
        self.push(stat)
        return blk, stat

    def onFor(self, expressions, condition):
        debug("onFor %s %s", expressions, condition)
        blk, stat = self.current.newFor()
        #for expr in expressions:
        #    self.current.addSource(expr)
        if condition is None:
            condition = 'True'
        stat.setExpression(condition)
        stat.addSource('pass')
        self.push(stat)
        return blk, stat

    def onForFinish(self, stat, updates, pop=False):
        for update in updates:
            stat.addSource(update)
        if pop:
            self.pop()

    def onDo(self):
        debug("onDo")
        stat = self.current.newStatement("while")
        stat.setExpression('True')
        self.push(stat)
        return stat

    def onDoFinish(self, stat, expr, pop=False):
        debug("onDoFinish %s %s %s", stat, expr, pop)
        ifstat = stat.newStatement("if")
        ifstat.newStatement("break")
        ifstat.setExpression("not %s" % expr)
        if pop:
            self.pop()

    def onWhile(self):
        stat = self.current.newStatement("while")
        self.push(stat)
        return stat

    def onWhileFinish(self, stat, expr, pop=False):
        stat.setExpression(expr)
        if pop:
            self.pop()

    def onThrow(self, expr):
        stat = self.current.newStatement("raise")
        stat.setExpression(expr)
        return stat

    def onMethod(self, name, mods=None, params=None, pop=False):
	debug("onMethod %s %s %s", name, mods, params)
	meth = self.current.newMethod()
	meth.name = name
	for mod in (mods or []):
	    meth.addModifier(mod)
	for param in (params or []):
	    #if len(param) == 2:
	    #    param += [None]
	    t, p, a = param.get('type', ''), param.get('id', ''), param.get('array')
	    meth.addParameter(t, p)
	self.push(meth)
        if pop:
            self.pop()
	return meth

    def onAnnotationMethod(self, name, annodecls, default):
	meth = self.onMethod(name)
	for annodecl in (annodecls or []):
            meth.addModifier(annodecl[0])
	if default:
	    src = "return %s" % (default, )
	else:
	    src = "pass"
        meth.addSource(src)
	self.pop()
	return meth


    def makeParamDecl(self, src, typ, isVariadic=False):
        exp = src.copy()
        exp['type']=typ
        if isVariadic:
            exp['id'] = '*' + exp['id']
        return exp

    def makeMethodExpr(self, pex, args):
	debug("makeMethodExpr %s %s", pex, args)
        src = str(pex or "None") + "(" + str.join(", ", [str(a or "") for a in args]) + ")"
	return src
	#self.current.addSource(src)

    def onVariables(self, variables, applyType=marker):
	debug("onVariables %s %s", variables, applyType)
        if applyType is not marker:
            for var in variables:
                var['type'] = applyType
	renames = self.current.config.combined('variableNameMapping')
	for var in variables:
	    name, value = var.get("id", "?"), var.get("init", marker)
	    name = renames.get(name, name)
	    v = self.current.newVariable(name)
	    v.name = name
	    if 'init' in var:
                if isinstance(value, (list, tuple)) and len(value)==2:
                    methname, margs = value
                    value = "%s(%s)" % (methname, str.join(", ", margs))
		src = "%s = %s" % (name, value)
	    else:
		src = "%s = %s()" % (name, var.get('type'))
	    self.current.addSource(src)


    def onAssign(self, op, left, right):
        #self.source.current.fixAssignInExpr(True, ("\%s = \%s", (left, right)), left)
        debug("onAssign %s %s %s", op, left, right)
        self.current.addSource("%s %s %s" % (left, op, right))
	pass

    def onReturn(self, pex):
	debug("onReturn %s", pex)
	src = ("return %s", pex) if pex else "return"
	self.current.addSource(src)

    def push(self, value):
        debug("push %s", (value.name if hasattr(value, 'name') else value))
	self.stack.append(value)

    def pop(self):
        value = self.stack.pop()
        debug("pop %s", (value.name if hasattr(value, 'name') else value))
	return value


    def altName(self, name):
	return self.current.fixDecl(name)


    def onEnumScope(self, enums):
	debug("onEnumScope %s", enums)


    def onEnum(self, name, values):
	klass = self.onClass(name)
	## klass.addBaseClass('EnumValue')
	return klass


    def onAnnoType(self, name, modifiers):
	## lookup base class
	bases = ['object', ]
	klass = self.onClass(name, [], bases)
	return klass

    def fixFloatLiteral(self, value):
        if value.startswith("."):
            value = "0" + value
        if value.endswith(("f", "d")):
            value = value[:-1]
        elif value.endswith(("l", "L")):
            value = value[:-1] + "L"
        return value


    def makeArrayAccess(self, pri, exp):
        return "%s[%s]" % (pri, exp, )


    def onAssert(self, exp, arg=marker):
        debug("onAssert %s %s", exp, arg)
        if arg is not marker:
            src = "assert %s, %s" % (exp, arg, )
            s = self.current.newStatement(src)
        else:
            src = "assert %s" % (exp, )
            s = self.current.newStatement(src)
            #s.setExpression(exp)

    def onTry(self):
        stat = self.current.newStatement("try")
        self.push(stat)
        return stat

    def onExcept(self):
        stat = self.current.newStatement("except")
        self.push(stat)
        return stat

    def onExceptClause(self, stat, clause, pop=False):
        exc = clause.get('type')
        nam = clause.get('id')
        src = '(%s, ), %s' % (exc, nam)
        stat.setExpression(src)
        if pop:
            self.pop()

    def onFinally(self):
        stat = self.current.newStatement("finally")
        self.push(stat)
        return stat

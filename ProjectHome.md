### java2python has moved to github.com ###

Go here instead:    https://github.com/natural/java2python

### Old stuff, will be removed soon ###

Simple but effective tool to translate java source code into python source code.

'Hello, world.' example:

```
$ cat HelloWorldApp.java
class HelloWorldApp {
    public static void main(String[] args) {
        System.out.println('Hello, world.');
        System.out.println(args);
    }
}

$ j2py -i HelloWorldApp.java
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HelloWorldApp(object):
    ''' generated source for HelloWorldApp

    '''
    @classmethod
    def main(cls, args):
        print 'Hello, world.'
        print args

if __name__ == '__main__':
    import sys
    HelloWorldApp.main(sys.argv)

```

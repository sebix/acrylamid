# Copyright 2011 posativ <info@posativ.org>. All rights reserved.
# License: BSD Style, 2 clauses. see lilith.py

import sys, os, re
import yaml
from datetime import datetime
from os.path import join, exists, getmtime, dirname
from time import gmtime
import logging

import extensions, lilith

log = logging.getLogger('lilith.tools')

def run_callback(chain, input, defaultfunc=lambda x: x):
    """Applies defaultfunc to input and additional every function in chain.
    
    Should return neither the modifed or the unmodified output. But
    since we have a lot of cross-references here, this is currently
    NOT possible (but implemented using mapping, though).
    
    You can override the defaultfunc (given in lilith_handler) by adding
    @defaultfunc to your callback. defaultfunc can be imported from tools.
    """
    
    if not callable(defaultfunc):
        raise TypeError('defaultfunc must be callable')
        
    log.debug('running %s ' % ('cb_'+chain))
    chain = extensions.get_callback_chain(chain)
    newdefault = filter(lambda f: f.func_dict.get('defaultfunc', False), chain)
    
    if len(newdefault) > 1:
        newdefault = ', '.join(['%s.%s' % (f.__module__, f.func_name)
                                    for f in newdefault])
        log.critical('more than one defaultfunc specified: %s' % newdefault)
        sys.exit(1)
    elif len(newdefault) == 1:        
        defaultfunc = newdefault[0]
        chain.remove(defaultfunc)
        log.debug('new defaultfunc: %s.%s' % (defaultfunc.__module__,
                                              defaultfunc.func_name) )

    for func in chain:
        log.debug('%s.%s' % (func.__module__, func.func_name))
        input = func(input)
    
    log.debug('%s.%s' % (defaultfunc.__module__, defaultfunc.func_name))
    return defaultfunc(input)

def defaultfunc(func):
        func.func_dict['defaultfunc'] = True
        return func
    
class ColorFormatter(logging.Formatter):
    """Implements basic colored output using ANSI escape codes."""
    
    BLACK = '\033[0;30m%s\033[0m'
    RED = '\033[0;31m%s\033[0m'
    GREY = '\033[0;37m%s\033[0m'
    RED_UNDERLINE = '\033[4;31m%s\033[0m'
    
    def __init__(self, fmt='[%(levelname)s] %(name)s: %(message)s'):
        logging.Formatter.__init__(self, fmt)
        
    def format(self, record):
        if record.levelname == 'DEBUG':
            record.levelname = self.BLACK  % record.levelname
        elif record.levelname == 'INFO':
            record.levelname = self.GREY  % record.levelname
        elif record.levelname in ('WARN', 'WARNING'):
            record.levelname = self.RED  % record.levelname
        elif record.levelname in ('ERROR', 'CRITICAL', 'FATAL'):
            record.levelname = self.RED_UNDERLINE % record.levelname
        return logging.Formatter.format(self, record)

def check_conf(conf):
    """Rudimentary conf checking.  Currently every *_dir except
    `ext_dir` (it's a list of dirs) is checked wether it exists."""
    
    # directories
    
    for key, value in conf.iteritems():
        if key.endswith('_dir') and not key in ['ext_dir', ]:
            if os.path.exists(value):
                if os.path.isdir(value):
                    pass
                else:
                    log.error("'%s' must be a directory" % value)
                    sys.exit(1)
            else:
                os.mkdir(value)
                log.warning('%s created...' % value)
                
    return True
    
def render(tt, *dicts, **kvalue):
    """helper function to merge multiple dicts and additional key=val params
    to a single environment dict used by jinja2 templating. Note, merging will
    first update dicts in given order, then (possible) overwrite single keys
    in kvalue."""
        
    env = {}
    for d in dicts:
        env.update(d)
    for key in kvalue:
        env[key] = kvalue[key]
    
    return tt.render( env )

def mk_file(content, entry, path, force=False):
    """Creates entry in filesystem. Overwrite only if content
    differs.
    
    Arguments:
    content -- rendered html
    entry -- FileEntry object
    path -- path to write
    force -- force overwrite, even nothing has changed (defaults to `False`)
    """
    
    if exists(dirname(path)) and exists(path):
        old = open(path).read()
        if content == old and not force:
            log.debug("'%s' is up to date" % entry['title'])
        else:
            f = open(path, 'w')
            f.write(content)
            f.close()
            log.info("Content of '%s' has changed" % entry['title'])
    else:
        try:
            os.makedirs(dirname(path))
        except OSError:
            # dir already exists (mostly)
            pass
        f = open(path, 'w')
        f.write(content)
        f.close()
        log.info("'%s' written to %s" % (entry['title'], path))
        
def safe_title(title):
    """safe_title returns a safe url string"""
    return re.sub('[\W]+', '-', title, re.U).lower().strip('-')
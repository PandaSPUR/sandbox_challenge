'''
Author: Pawan M Ranganatha Rao
ID: 0487218
Email: prr238@nyu.edu

Description:
Turing Complete Sandbox
Application Security
Fall 2013
'''


#Imports
import sys
import resource
import compiler
from __builtin__ import *
import inspect
import os

#Global Constants to set the resources utilized by the sandbox
MAX_MEM = 4096
MAX_RSS = 8192
MAX_NPROC = 8
MAX_NOFILE = 16
MAX_CPUTIME = 30 
MAX_VMEM = 8192

#Get all the builtin functions
all_functions = []
for (func,obj) in inspect.getmembers(__builtins__):
    if (inspect.isbuiltin(obj)):
        all_functions.append(func)

#List of blacklisted/unsafe functions which are not allowed in the sandbox
disallowed_functions = [
'__import__','apply','bytearray','compile','dir','callable','delattr',
'eval','exec','execfile','file','getattr','globals','hasattr','input','intern','id',
'locals','memoryview','open','reload','setattr','type','vars','zip','raw_input'
]

#Filter all the allowed functions by removing all the blacklisted functions
allowed_functions = []
for item in all_functions:
    if item in disallowed_functions:
        pass
    else:
        allowed_functions.append(item)
allowed_functions = sorted(allowed_functions)

#List of allowed types
allowed_types = [
'True','False','int','float','long','complex','list','buffer','unicode'
]

#List of all allowed functions and builtin types:w
all_allowed = allowed_functions + allowed_types

#Create a dictionary of all allowed list of types and functions
temp_list=[]
for obj in all_allowed:
    temp = (obj,locals().get(obj))
    temp_list.append(temp)

allowed_dict = dict(temp_list)


#List of allowed nodes in the Abstract Syntax Tree(AST).
#While traversing the AST if a node is found which is not in the list, exception is raised 
allowed_ops = [
    'Add', 'And', 'AssAttr', 'AssList', 'AssName', 'AssTuple', 'Assert','Assign', 'AugAssign',
    'Bitand', 'Bitor', 'Bitxor', 'Break',
    'CallFunc', 'Class', 'Compare', 'Const', 'Continue',
    'Decorators', 'Dict', 'Discard', 'Div',
    'Ellipsis', 'Expression', 'FloorDiv', 'For', 'Function',
    'Getattr', 'Global', 'If', 'IfExp', 'Invert', 'Keyword',
    'LeftShift', 'List', 'ListComp', 'ListCompFor', 'ListCompIf',
    'Mod', 'Module', 'Mul', 'Name', 'Not', 
    'Or', 'Pass', 'Power', 'Print', 'Printnl', 
    'Raise', 'Return', 'RightShift',
    'Slice', 'Sliceobj', 'Stmt', 'Sub', 'Subscript',
    'TryExcept', 'TryFinally', 'Tuple', 
    'UnaryAdd', 'UnarySub', 'While', 'Yield'
]

def main():
    #Check if the sandbox has been run correctly
    if(len(sys.argv) < 2):
        print "Insufficient Arguments\n Usage: ",sys.argv[0],"script_to_run.py <arg1> <arg2>"
        sys.exit(1)

    try:
        #Create local copy of allowed dict to ensure no leak of data and safe cleanup
        user_dict = allowed_dict.copy()
        user_dict["__builtins__"] = None
        user_dict["argv"] = sys.argv[1:]
        user_dict["exit"] = sys.exit
        user_dict["__name__"] = __name__

        #Check if all created nodes from user code are allowed
        userNodes = compiler.parseFile(sys.argv[1])
        checkNode(userNodes)

        #Set resource limits using setrlimit() for the execution of user code
        resource.setrlimit(resource.RLIMIT_DATA , (MAX_MEM , MAX_MEM))
        resource.setrlimit(resource.RLIMIT_STACK , (MAX_MEM , MAX_MEM))
        resource.setrlimit(resource.RLIMIT_RSS , (MAX_RSS , MAX_RSS))
        resource.setrlimit(resource.RLIMIT_NPROC , (MAX_NPROC , MAX_NPROC))
        resource.setrlimit(resource.RLIMIT_CPU , (MAX_CPUTIME , MAX_CPUTIME))
        resource.setrlimit(resource.RLIMIT_NOFILE , (MAX_NOFILE , MAX_NOFILE))
	
        #Default user ID of nobody user in Ubuntu
        nobody = 65534
        #Drop user privileges
        os.setuid(nobody)
	
        #Execute the file passed in with lower privileges.
        #The whitelist of functions is being passed here to ensure safe execution
        execfile(sys.argv[1] , user_dict)
    except SystemExit:
        pass
    except NameError,e:
        print "Unknown function found in " + sys.argv[1]
        print str(e)
    except Exception, e:
        print "An error occured while running " + sys.argv[1]
        print str(e)
    finally:
        del(user_dict)

#Receives and AST node and checks if all the nodes are allowed to be used.
#Else an exception is raised.
def checkNode(node):
    if node.__class__.__name__ not in allowed_ops:
        raise Exception (" Error in the user input program. Program will now terminate\n")

    for child in node.getChildNodes():
        checkNode(child)
        
#Are we being executed?
if __name__ == "__main__":
    main()
        

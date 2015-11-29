# Configuration steps #
  * Install Eclipse Ganymede(3.4), Python 2.4, Python 2.6 from Sun Package Manager
  * Install **Pydev** plugin 1.7.0, using Help -> Install Software and filling its update manager link from its download website
  * Install (important)**GEF** Plugin, and then, **Subclipse** Plugin
  * Window -> Preferences -> Pydev -> Interpreter Python -> add -> add python path (maybe /usr/lib/python2.6/python) or Autoconfig to add Python 2.4
  * **Notice**: It seems that JavaHL doesn't work properly, go to Team -> SVN -> SVN Interface -> SVNKit
  * You may also configure code completion, code folding in pydev
  * Import project: File -> Import... -> SVN -> import from svn -> New Location -> Next -> fill in https://devicemanagerofsjtu.googlecode.com/svn
  * When there is a popup, Choose **temporarily**, not "permanently" or "reject" -> Enter your Username and keys -> select "Create a new Project" -> Pydev -> Pydev Project
  * Enter project name and path -> Waiting for SVN checkout
  * You may also install other plugins, such as AnyEdit
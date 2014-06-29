#############################
CherryPy CGI-Server - History
#############################


=============
Version 0.3.5
=============

2014-06-29

- Location of the setup file is now PyPi.


=============
Version 0.3.4
=============

2013-04-21

- In case of a https-request, `request.base` returns bytestring not unicode.


=============
Version 0.3.3
=============

2013-04-13

- Setup separated from CherryPy.


=============
Version 0.3.2
=============

2013-03-30

- File-uploads changed from GoogleCode to GitHub.


=============
Version 0.3.1
=============

2013-03-30

- Timeout thread terminates CGI process if timeout occures


=============
Version 0.2.9
=============

2013-03-30

- Documentation changes


=============
Version 0.2.8
=============

2013-03-30

- The repository is now hosted on GitHub. I changed from GoogleCode to GitHub.

- New documentation structure


=============
Version 0.2.7
=============

2013-02-10

- Workarround für Pound http://www.apsis.ch/pound
  Falls Pound sich um das HTTPS-Handling kümmert, wird jetzt auch CherryPy
  in den HTTPS-Modus versetzt. Dem CGI-Handler wird eine HTTPS-Umgebung
  vorgetäuscht, damit dieses die Vorkehrungen für die Antwort auf einen
  HTTPS-Request durchführen kann.

- Alle noch nicht übernommenen Einträge aus dem Header werden an die
  CGI-Umgebung weitergereicht. Somit werden auch die zusätzlichen X-HTTPS-Header
  von Pound an den CGI-Handler weitergereicht.


=============
Version 0.2.6
=============

2013-02-10

- Ausprobiert ob GitHub besondere Vorteile für mich gegenüber Google Code
  bietet.

- Created documentation with Sphinx


=============
Version 0.2.5
=============

2013-01-23

- Added the *examples* directory to archive file

- Played with *distribute* for setup


===============
Version 0.2.4.a
===============

2013-01-20

- Project registered in the Python Package Index


=============
Version 0.2.3
=============

2013-01-20

- First trial to make a setup with setuptools.


=============
Version 0.2.2
=============

2013-01-19

- Helper function *_determine_script_filename_and_path_info* created to 
  help using of *DirectoryIndex*.

- New parameter *directory_index* allows to append filenames to show if no 
  filename in URL. Like Apache with *DirectoryIndex* does.

- New *lib* package added.

- New module *lib.format_* for additional formating-tools added.

- Examples extended

- Simple Python-CGI example added


=============
Version 0.2.1
=============

2013-01-09

- Get back response (header and body lines) into spooled temporary file

- Determine *script_name* corrected


=============
Version 0.2.0
=============

2013-01-06

- Code from development testdir merged to *cpcgiserver.__init__*

- Extended PHP page example created. Example with image (staticdir tool)

- Handles incorrect header lines, too

- Tests with buffered temporary files


=============
Version 0.1.2
=============

2013-01-06

- Script filename, script name, script extension, ...

- Environment variables filled

- Full functional development example successfuly tested


=============
Version 0.1.1
=============

2013-01-06

- started to fill the environment variables

- REDIRECT_STATUS ist set because of PHP security settings


=============
Version 0.1.0
=============

2013-01-06

- Tests with CherryPy, Tools and PHP-CGI

- Collected informations about Common Gateway Interface

- Descriptions for environment variables written


=============
Version 0.0.1
=============

2013-01-05

- First trials with Git

- Created Google-Code project

- First import into Git repository

- First reflecting about the program structure

- Git helper scripts added

#############################
CherryPy CGI-Server - History
#############################

=============
Version 0.2.2
=============

19.01.2013

- Helper function *_determine_script_filename_and_path_info* created to 
  help using of *DirectoryIndex*.

- New parameter *directory_index* allows to append filenames to show if no 
  filename in URL. Like Apache with *DirectoryIndex* does.

- New *lib* package added.

- New module *lib.format_* for additional formating-tools added.

- Examples extended


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

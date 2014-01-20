About
=====

Mobile String Toolkit is a handy Python 3 script that helps managing
translation texts for mobile applications.

Normally we put our app translations directly to proper resource files. This
is however very challenging when working with non-technical... clients.

Non-technical people are familiar with Excel or Google Docs, but rarely with
any decent development tools. This creates endless trails of e-mails with requests
for updates or fixes and copy-n-paste sessions that are cumbersome and boring.

I found that providing a simple interface, where a client can update application
resources easily, is a huge win four me. No more lost e-mails - I can build my
complete set of resources from CSV file of Google Spreadsheet delivered by
the client.

MST is just for that - it will take CSV or google spreadsheet and generate
XML files with translations.

Features:
 * generate Android string resources
 * loading data from CSV or Google Docs
 * support normal strings, string arrays or quantity strings
 * easily extendable with new output formats (plans for iOS) or data loaders

Installation
============

Currently there is no installation "bundle". Unpack MST somewhere and run:

```shell
python3 /path/to/MST/generate.py
```

You must be running Python 3 to use this script.

Usage
=====

After "installation" the script is ready to use. Type
```shell
python3 /path/to/mst/generate.py --help
```
to obtain usage instructions.

To generate proper resources we must create a configuration file in 
project root. This file contains information about generator (ie. output format)
and list of files we want to write our translations to. Configuration file is in 
JSON format:
```JSON
{
	"generator": "android",
	"paths": {
		"en": "res/values/strings.xml",
		"de": "res/values-de/strings.xml",
}
```

Examples:

In both examples we expect /project/mst.cfg configuration files to be properly written.

1) Generate resources in /project using CSV files. Print operation status.
```shell
python3 generate.py --project-root /project -C /project/strings.csv --verbose
```
2) Generate resources in /project using Google Docs. Print operation status.
```shell
python3 generate.py --project-root /project -G user@gmail.com password spreadsheet worksheet --verbose
```
If running this script becomes cumbersome, I advice you to set a launcher in your IDE. For Eclipse
go to External Tools Configuration and you're set. Enjoy!

Limitations
===========

So far there was no extensive testing by the masses, so if you find any bugs - please report them or fix
them and send me patches. This script worked for me for some time, buy you may find more corner cases.

Wondering why you can't put your google credentials directly into a configuration file?
This is a design decision. Configuration file will probably become part of your repository
contents and I don't want to be responsible for anybody uploading his username/password
to public GitHub repository. :)

This is a feature and I don't plan to change it.

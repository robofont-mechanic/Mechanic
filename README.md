Mechanic
========

Mechanic provides an interface in RoboFont for installing and updating extensions hosted on GitHub.

https://github.com/jackjennings/Mechanic

![mechanic preview](http://ja.ckjennin.gs/public/images/Mechanic-preview.png)

Requirements
------------

Mechanic requires RoboFont 1.3 or greater.

Installation
------------

Double click `Mechanic.roboFontExt`.

Features
--------

* Checks for updates of configured extensions on update (options)
* Ignore individual extensions from being updated
* Manually check for updates of configured extensions

Extension Registry
------------------

The list of installable extensions are (currently) maintained within the extension. Open an [Issue](https://github.com/jackjennings/Mechanic/issues) with the name of your extension and a link to the repository and it will be merged into the next Mechanic update.

Currently, Mechanic manages the following extensions:

* [RoboToDo](https://github.com/jackjennings/RoboToDo)

Mechanic for Developers
-----------------------

If you are already hosting your code on GitHub, support for mechanic is easy to add to your existing extensions. Mechanic will recognize your extension when these two lines are present in your extension's `info.plist` file:

```xml
	<key>repository</key>
	<string>username/Repository</string>
```

`string` should contain your username and the name of the repository that your extension is stored in (e.g. `jackjennings/Mechanic`).

Mechanic makes a few of assumptions about your repository:

1. **Releases are organized by tags**. When checking a local extension's version against a repository, Mechanic will search your repository's tags for the latest version number. When you want to release a new version of your extension, tag the specific commit with a incremented version number. Using tags instead matching the remote `info.plist` version, allows you to continue to commit to your repository, and only release when you are ready.

	From the command line, your first release might look like:

	```
		git tags -a 0.1 -m "Release version 0.1"
		git push origin master --tags
	```
	
	Because Mechanic checks the locally installed extension's plist against your git tags, you'll need to manually ensure that the version in your `info.plist` matches your release's tagged version. Mechanic recognizes major, minor, and patch level versions, `X.Y.Z`. Patch level is optional.

2. **Your extension exists in the root directory**. Mechanic (currently) installs the first RoboFont extension that it finds in the base folder of your repository. This means that it is not possible to store multiple extensions in a single repository, nor can your extension be stored in a sub directory of the repository.

3. **You're working on the master branch**. Mechanic will always download the most up to date version of your software from the master branch.

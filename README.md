Mechanic
========

Mechanic provides an interface in RoboFont for installing and updating extensions hosted on GitHub.

https://github.com/jackjennings/Mechanic

![mechanic preview](http://ja.ckjennin.gs/public/images/Mechanic-preview.png)

Requirements
------------

Mechanic requires RoboFont 1.5 or greater.

Installation
------------

Double click `Mechanic.roboFontExt`.

Features
--------

* Browse and install extensions from a list of publicly available extensions
* Checks for updates of configured extensions on startup (optional)
* Conditionally ignore individual extensions from being updated
* Optionally ignore small updates on startup
* Manually check for updates of configured extensions
* Register extensions to the public extension registry

Extension Registry
------------------

Mechanic has a website that lists all of the [available extensions](http://robofontmechanic.com).

Mechanic for Developers
-----------------------

If you are already hosting your code on GitHub, support for Mechanic is easy to add to your existing extensions. You can version your extension in two ways, depending on how your repository is set up: with git tags, or through `info.plist`.

Either way:
* Mechanic assumes that the release version of your code lives on the `master` branch.
* Mechanic recognizes major, minor, and patch level versions, `X.Y.Z`. Patch level is optional.

Once you have added the required keys to your `info.plist` file, you can register your extension from within the Mechanic interface in RoboFont.

### ~~Versioning with Tags~~

**This versioning system will be deprecated in the near future. Versioning with info.plist (below) is the prefered method at this time.**

~~If you only have a single extension in your repository, using tags is the best way to organize your releases. Tagging allows you to specify a single, authoritative commit for each version of your extension.~~

~~In order for Mechanic to recognize your extension, add a `repository` key to your `info.plist` file:~~

```xml
	<key>repository</key>
	<string>username/Repository</string>
```

* ~~`repository` should contain your username and the name of the repository that your extension is stored in (e.g. `jackjennings/Mechanic`).~~

~~When checking a local extension's version against a repository, Mechanic will search your repository's tags for the latest version number. When you want to release a new version of your extension, tag the specific commit with a incremented version number. From the command line, your first release might look like:~~

```
	git tag -a 0.1 -m "Release version 0.1"
	git push origin master --tags
```

~~Because Mechanic checks the locally installed extension's plist against your git tags, you'll need to manually ensure that the version in your `info.plist` matches your release's tagged version.~~

~~When versioning with tags, Mechanic installs the first RoboFont extension that it finds in your repository. If there's more than one, it will try to guess which is the correct extension based on it's filename. If you need to have more than one extension in your repository, consider versioning with `info.plist`.~~

### Versioning with `info.plist`

You can also version your extension using only the key found in `info.plist`.

Add the standard `repository` key to your `info.plist`, along with an `extensionPath` key.

```xml
	<key>repository</key>
	<string>username/Repository</string>
	<key>extensionPath</key>
	<string>path/to/Extension.roboFontExt</string>
```

* `repository` should contain your username and the name of the repository that your extension is stored in (e.g. `jackjennings/Mechanic`).

* `extensionPath` should contain the path to your extension, relative to the root of your repository (e.g. `ext/myExtension/myExtension.roboFontExt`)

Mechanic will download the `info.plist` file that is contained in the extension specified in `extensionPath` when checking for updates.

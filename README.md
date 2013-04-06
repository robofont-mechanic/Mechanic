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

* Checks for updates of configured extensions on update (optional)
* Conditionally ignore individual extensions from being updated
* Manually check for updates of configured extensions

Extension Registry
------------------

The list of installable extensions are (currently) maintained within the extension. Open an [Issue](https://github.com/jackjennings/Mechanic/issues) with the name of your extension and a link to the repository and it will be merged into the next Mechanic update.

Currently, Mechanic manages the following extensions:

* [Arrange Windows](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Feature Preview](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Glif Viewer](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Groups2Features](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Layer Preview](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Mechanic](https://github.com/jackjennings/Mechanic) by Jack Jennings
* [Outliner](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Pixel Tool](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Ramsay St.](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Replicant](https://github.com/jackjennings/Replicant) by Jack Jennings
* [RoboToDo](https://github.com/jackjennings/RoboToDo) by Jack Jennings
* [send2twitter](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Shape Tool](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [SidebearingsEQ](https://github.com/franzheidl/SidebearingsEQ) by Franz Heidl
* [Tiny Draw Bot](https://github.com/typemytype/RoboFontExtensions) by Frederik Berlaen
* [Type Cooker](https://github.com/typemytype/RoboFontExtensions) by TypeMedia

Mechanic for Developers
-----------------------

If you are already hosting your code on GitHub, support for mechanic is easy to add to your existing extensions. You can version your extension in two ways, depending on how your repository is set up.

Mechanic assumes that you are releasing on the master branch.

Mechanic recognizes major, minor, and patch level versions, `X.Y.Z`. Patch level is optional.

## Versioning with Tags (recommended)

If you only have a single extension in your repository, using tags is the best way to organize your releases. Tagging allows you to specify a single, authoritative commit for each version of your extension.

In order for Mechanic to recognize your extension, add a `repository` key to your `info.plist` file:

```xml
	<key>repository</key>
	<string>username/Repository</string>
```

* `repository` should contain your username and the name of the repository that your extension is stored in (e.g. `jackjennings/Mechanic`).

When checking a local extension's version against a repository, Mechanic will search your repository's tags for the latest version number. When you want to release a new version of your extension, tag the specific commit with a incremented version number. From the command line, your first release might look like:

```
	git tag -a 0.1 -m "Release version 0.1"
	git push origin master --tags
```

Because Mechanic checks the locally installed extension's plist against your git tags, you'll need to manually ensure that the version in your `info.plist` matches your release's tagged version. 

When versioning with tags, Mechanic installs the first RoboFont extension that it finds in your repository. If there's more than one, it will try to guess which is the correct extension based on it's filename. If you need to have more than one extension in your repository, consider versioning with `info.plist`.

## Versioning with `info.plist`

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

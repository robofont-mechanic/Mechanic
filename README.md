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

If you are already hosting your code on GitHub, support for Mechanic is easy to add to your existing extensions.

* Mechanic assumes that you are releasing on the master branch.
* Mechanic recognizes major, minor, and patch level versions, `X.Y.Z`. Patch level is optional.

Add the standard `repository` key to your `info.plist`, along with an `extensionPath` key.

```xml
  <key>repository</key>
  <string>username/Repository</string>
```

`repository` should contain your username and the name of the repository that your extension is stored in (e.g. `jackjennings/Mechanic`).

Once you have added the required keys to your `info.plist` file, you can register your extension from within the Mechanic interface in RoboFont.

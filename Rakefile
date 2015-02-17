require 'rake'
require 'rake/clean'
require 'active_support'

SRC = "src"
BUNDLE = "Mechanic.roboFontExt"
STARTUP = BUNDLE + "/lib/_startup.py"

SOURCE_FILES = FileList[
  "src/html/**/*.*",
  "src/lib/**/*.*",
  "src/Resources/**/*.*"
]

SOURCE_FILES.exclude('*.pyc')
CLEAN.include(FileList['**/*.pyc'])

directory "Mechanic.roboFontExt"
CLOBBER.include('Mechanic.roboFontExt/**/*')
CLOBBER.exclude('Mechanic.roboFontExt/.env')

SOURCE_FILES.each do |src|
  target = src.pathmap("%{^src/,Mechanic.roboFontExt/}p")
  file target => src do
    mkdir_p target.pathmap("%d")
    cp src, target
  end
  task :source => target
end

file "Mechanic.roboFontExt/info.plist" => "src/info.yml" do |t|
  require_relative 'tasks/menu_item'
  require 'plist'
  require 'yaml'

  menu_scripts = FileList["Mechanic.roboFontExt/lib/*.py"].exclude(STARTUP)

  data = YAML.load_file t.source
  data['html'] = Dir.exists? "Mechanic.roboFontExt/html"
  data['launchAtStartUp'] = File.exists? STARTUP
  data['mainScript'] = data['launchAtStartUp'] ? STARTUP.pathmap("%f") : ''
  data['timeStamp'] = Time.now.to_f
  data['addToMenu'] = menu_scripts.to_a.collect {|i| MenuItem.new(i).to_hash}
  data.save_plist t.name
end
CLOBBER.include("Mechanic.roboFontExt/info.plist")

task plist: %W[Mechanic.roboFontExt Mechanic.roboFontExt/info.plist]

desc "Compiles an extension from src"
task build: [:clean, :clobber, :source, :plist]

desc "Compiles and installs an extension from src"
task :install => :build do
  sh "open Mechanic.roboFontExt"
end

desc "Blindly uninstalls an installed Mechanic extension"
task :uninstall do
  sh "rm -rf ~/Library/Application\\ Support/RoboFont/plugins/Mechanic.roboFontExt"
end

desc "Runs the bin/demo.py script in RoboFont for capturing screenshots"
task :demo do
  sh "robofont -p '#{File.expand_path('./bin/demo.py')}'"
end

desc "Compiles screenshots into a single image"
task :screenshot do
  require 'chunky_png'
  cd 'screenshots'
  install = ChunkyPNG::Image.from_file "install.png"
  updates = ChunkyPNG::Image.from_file "updates.png"
  width = install.width + 100
  height = install.width + 25
  composite = ChunkyPNG::Image.new width, height, ChunkyPNG::Color::TRANSPARENT
  composite.compose! install, 0, 0
  composite.compose! updates, width - updates.width, height - updates.height
  composite.save 'mechanic.png'
end

task default: :build

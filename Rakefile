require 'rake'
require 'rake/clean'
require 'active_support'

SRC = "src"
BUNDLE = "Mechanic.roboFontExt"
STARTUP = BUNDLE + "/lib/_startup.py"

SOURCE_FILES = FileList[
  "src/html/**/*",
  "src/lib/**/*.py",
  "src/Resources/**/*"
]

CLOBBER.include(SOURCE_FILES.pathmap("%{^src/,Mechanic.roboFontExt/}p"))
CLEAN.include(FileList['**/*.pyc'])

SOURCE_FILES.each do |src|
  target = src.pathmap("%{^src/,Mechanic.roboFontExt/}p")
  file target => src do
    mkdir_p target.pathmap("%d")
    cp src, target
  end
  task :source => target
end

file "Mechanic.roboFontExt/info.plist" => "src/info.yml" do |t|
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

directory "Mechanic.roboFontExt"

task plist: %W[Mechanic.roboFontExt Mechanic.roboFontExt/info.plist]

task build: [:clobber, :source, :plist]

task :install => :build do
  sh "open Mechanic.roboFontExt"
end

task :uninstall do
  sh "rm -rf ~/Library/Application\\ Support/RoboFont/plugins/Mechanic.roboFontExt"
end

task default: :build

task :demo do
  sh "robofont -p '#{File.expand_path('./bin/demo.py')}'"
end

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

class MenuItem

  attr_accessor :item

  def initialize item
    @item = item
  end

  def key
    m = name.match('_([A-Z])$')
    m ? m[1] : ''
  end

  def name
    item.pathmap("%n")
  end

  def sanitized_name
    name.gsub(/_#{key}/, '')
  end

  def title
    ActiveSupport::Inflector.titleize(sanitized_name)
  end

  def path
    item.pathmap("%f")
  end

  def to_hash
    {
      path: path,
      preferredName: title,
      shortKey: key
    }
  end

end

require 'rake'
require 'active_support'

SRC = "src"
BUNDLE = "Mechanic.roboFontExt"
STARTUP = BUNDLE + "/lib/_startup.py"

SOURCE_FILES = FileList[
  "src/html/**/*",
  "src/lib/**/*.py",
  "src/Resources/**/*"
]

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
  data = YAML.load_file t.source
  data['html'] = Dir.exists? "Mechanic.roboFontExt/html"
  data['launchAtStartup'] = File.exists? STARTUP
  data['mainScript'] = data['launchAtStartup'] ? STARTUP.pathmap("%f") : ''
  data['timeStamp'] = Time.now.to_f
  data['addToMenu'] = FileList.new("Mechanic.roboFontExt/lib/*.py") do |fl|
    fl.exclude(/^_/)
  end.to_a.collect {|i| MenuItem.new(i).to_hash}
  data.save_plist t.name
end

directory "Mechanic.roboFontExt"

task source: "Mechanic.roboFontExt"

task plist: %W[Mechanic.roboFontExt/info.plist]

task build: [:source, :plist]

task default: :build

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

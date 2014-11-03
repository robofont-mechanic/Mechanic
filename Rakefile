require 'rake'
require 'plist'
require 'yaml'
require 'active_support'

SRC = "src"
BUNDLE = "Mechanic.roboFontExt"
STARTUP = BUNDLE + "/lib/_startup.py"
MENU_SCRIPTS = Rake::FileList.new(BUNDLE + "/lib/*.py")
MENU_SCRIPTS.reject! {|s| s.pathmap("%f")[0] == "_"}

rule BUNDLE + "/info.plist" => SRC + "/info.yml" do |t|
  data = YAML.load_file t.source
  data['html'] = Dir.exists? BUNDLE + "/html"
  data['launchAtStartup'] = File.exists? STARTUP
  data['mainScript'] = data['launchAtStartup'] ? STARTUP.pathmap("%f") : ''
  data['timeStamp'] = Time.now.to_f
  data['addToMenu'] = MENU_SCRIPTS.to_a.collect {|i| MenuItem.new(i).to_hash}
  data.save_plist t.name
end

directory BUNDLE

task plist: %W[Mechanic.roboFontExt/info.plist]

task build: [:plist]

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

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
  data['addToMenu'] = MENU_SCRIPTS.pathmap("%f").to_a.collect do |item|
    MenuItem.new(item).to_hash
  end
  data.save_plist t.name
end

directory BUNDLE

task plist: %W[Mechanic.roboFontExt/info.plist]

task default: [:plist]

class MenuItem
  
  def initialize item
    @item = item
    @name = item.pathmap("%n")
    @key = ''
    
    @name.match('_([A-Z])$') do |m|
      @key = m[1]
      @name.gsub!(/#{m[0]}$/, '')
    end
  end
  
  def preferred_name
    ActiveSupport::Inflector.titleize(@name)
  end
  
  def to_hash
    {
      path: @item,
      preferredName: self.preferred_name,
      shortKey: @key
    }
  end
  
end

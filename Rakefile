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
  data['addToMenu'] = MENU_SCRIPTS.pathmap("%f").reduce([]) do |a, item|
    a << MenuItem.new(item)
  end
  data.save_plist t.name
end

directory BUNDLE

task plist: %W[Mechanic.roboFontExt/info.plist]

task default: [:plist]

class MenuItem < Hash
  
  def initialize item
    name = item.pathmap("%n")
    
    if key_match = name.match('_([A-Z])$')
      key = key_match[1]
      name.gsub!(/#{key_match[0]}$/, '')
    else
      key = nil
    end
    
    self['path'] = item
    self['preferredName'] = ActiveSupport::Inflector.titleize(name)
    self['shortKey'] = key.to_s
  end
  
end

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

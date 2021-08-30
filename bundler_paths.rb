# frozen_string_literal: true

require "bundler/setup" if ENV["BUNDLE_GEMFILE"]
require "pathname"

requires = []

$LOAD_PATH.each do |load_path|
  Dir["#{load_path}/**/*.rb"].each do |entry|
    path = Pathname.new(entry)
    relative_path = path.relative_path_from(load_path)

    requires << {
      load_path: load_path,
      path: path,
      relative_path: relative_path,
      require_path: relative_path.to_s[/^(.+)\.rb$/, 1]
    }
  end
end

puts requires.map {|r| r[:require_path] }.sort.uniq.join("\n")

import sublime
import sublime_plugin
import os
import hashlib
import re

class BundlerAutocompleteListener(sublime_plugin.EventListener):
  def on_query_completions(self, view, prefix, locations):
    # Make sure we're in Ruby context.
    if not view.match_selector(locations[0], "source.ruby"):
      return []

    # Also, let's ensure we're inside quotes.
    if not view.score_selector(locations[0], "string.quoted"):
      return []

    sel = view.sel()[0]
    line = view.substr(view.full_line(sel)).rstrip()
    cursor = sel.begin()
    (_, col) = view.rowcol(cursor)
    pattern = r"""^\s*(require|load)\s*\(?(['"]).*?\2\)?"""
    matches = re.match(pattern, line)

    # Make sure we are inside a require/load statement.
    if not matches:
      return []

    quote = matches.group(2)
    start_quote = line.index(quote)
    end_quote = line.index(quote, start_quote + 1)

    # Make sure we are inside quotes.
    if col < start_quote and col > end_quote:
      return []

    gems = self.get_gems(view.window().folders())
    completions = []

    for gem in gems:
      if gem.startswith(prefix):
        completions.append(["%s\tgem" % gem, gem])

    return (
      completions,
      sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
    )

  def get_gems(self, folders):
    gemfiles = (os.path.join(folder, "Gemfile") for folder in folders)
    gemfiles = (file for file in gemfiles if os.path.exists(file))
    gems = []

    for gemfile in gemfiles:
      gems = gems + self.parse_gemfile(gemfile)

    gems.sort()

    return gems

  def parse_gemfile(self, gemfile):
    pattern = r"""^\s*gem\s+(['"])(.*?)\1"""
    file = open(gemfile, "r")
    contents = file.read()
    matches = re.findall(pattern, contents, re.MULTILINE)
    gems = []

    for match in matches:
      if not match[1] in gems:
        gems.append(match[1])

    return gems

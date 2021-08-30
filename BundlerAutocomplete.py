import sublime
import sublime_plugin
import os
import hashlib
import re
import subprocess
import tempfile


def write_file(path, contents):
  try:
    file = open(path, "w", encoding="utf-8")
    file.write(contents)
    file.close()
  except Exception as e:
    raise e


def read_file(path):
  try:
    file = open(path, "r", encoding="utf-8")
    return file.read()
  except Exception as e:
    raise e


def is_file(path):
  try:
    return os.path.isfile(path)
  except Exception as e:
    return False


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
    pattern = r"""^\s*(require|load)\s*\(?(['"])(.*?)\2\)?"""
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

    ruby_file_path = os.path.join(os.path.dirname(__file__),
                                  "bundler_paths.rb")

    file_name = view.file_name() or ""

    folder = next((folder for folder in sublime.active_window().folders()
                   if file_name.startswith(folder + "/")), None)

    gemfile = os.path.join(folder, "Gemfile")
    gemfile_lock = gemfile + ".lock"

    if not is_file(gemfile) or not is_file(gemfile_lock):
      return []

    hash = hashlib.new("md5")
    hash.update(read_file(gemfile_lock).encode("utf-8"))

    cache_file = os.path.join(tempfile.gettempdir(),
                              "bundler-autocomplete-" + hash.hexdigest())

    if is_file(cache_file):
      contents = read_file(cache_file)
    else:
      env = os.environ.copy()
      env["BUNDLE_GEMFILE"] = gemfile
      result = subprocess.run(["ruby", ruby_file_path],
                              capture_output=True,
                              env=env)

      if result.returncode != 0:
        return []

      contents = result.stdout.decode()
      write_file(cache_file, contents)

    requires = list(
        filter(lambda path: path.startswith(prefix),
               contents.strip().split("\n")))

    return list(map(lambda path: (["%s\trequire" % path, path]), requires))

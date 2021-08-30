import sublime_plugin
import tempfile
from glob import glob
import os


class BundlerAutocompleteClearCache(sublime_plugin.WindowCommand):
  def run(self):
    entries = glob(
        os.path.join(tempfile.gettempdir(), "bundler-autocomplete-*"))

    for entry in entries:
      try:
        os.unlink(entry)
      except Exception as e:
        continue

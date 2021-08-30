# Bundler Autocomplete

Autocomplete `require`s using your project's `Gemfile` as the source.

Notice that the autocompletion is only triggered for instructions like
`require "cursor_here"` and `require 'cursor_here'`. Also, this plugin requires
your root directory to have a `Gemfile` and `Gemfile.lock` files.

![Sublime Text: Bundler Autocomplete](https://github.com/fnando/sublime-bundler-autocomplete/raw/main/bundler-autocomplete.gif)

Results are cached until `Gemfile.lock`'s content changes; if you notice any
inconsistent results, you may clear the cache using the command
`Bundler Autocomplete: Clear Cache`, triggered from the Command Palette.

## License

Copyright (c) 2019 Nando Vieira

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

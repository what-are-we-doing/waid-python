# What Am I Doing?

What Am I Doing (`waid`) is a Python package for reporting job progress and
status. It integrates the Python logging API with sensible configuration for a
variety of environments and a progress-reporting API that can write periodically
to the logs or control progress bars on the console or a Jupyter notebook. Think
of it as a combination of logging and tqdm, with some extra features.

`waid` is designed to be backend-agnostic, so library code can freely depend on
it to report progress without making any assumptions about how the application
code is configured.  Its logging support also reuses Python logging, so library
code only needs to interact with `waid` if it needs the progress reporting APIs.
It is also designed to solve some of the problems with Python logging in
multiprocessing environments, so your multiprocessing code can focus on the work
it's supposed to be doing.

## Alternatives

[Rich]: https://pypi.org/project/rich/
[enlighten]: https://pypi.org/project/enlighten/
[tqdm]: https://pypi.org/project/tqdm/

Why not use [Rich][], [enlighten][], [tqdm][], or any of the other fine Python
progress libraries, or just use stdlib logging directly?  Why do we need `waid`?

First, if all you need is to log messages, then using the Python logging API is
absolutely the right call, and that's what you do with `waid` — it doesn't replace
Python logging calls at all.

Second, if you are writing a *library*, then making it depend on one of these
packages ties you to particular output channels.  Many of them do provide some
flexibility in this regard, supporting outputs such as Jupyter notebooks, but
if you use Rich in a library that someone wants to use in an Enlighten program
(or vice versa), then additional adaptation work is needed.  There is not, to
my knowledge, a backend-agnostic *progress* API.

`waid` is designed around the idea that progress updates are a structured log
event, just like other log messages, and should be routed to handlers. Libraries
can therefore report progress to waid with abandon, and application code can
handle those progress events however they want; when dedicated progress displays
aren't available, it can also write periodic log messages with the current
status.  Progress is also attached to the logger hierarchy, so that progress
bars can be filtered if desired.

On top of all of this, `waid` provides basic functionality for logging to log
files and the console, along with console progress bar displays, and convenient
APIs for configuring logging output in common command-line application designs.
It also provides facilities for routing logging messages from child processes.
Future plans include a separate high-performance log aggregation and display
package that allows reconnecting to headless runs (e.g. in a batch computing
environment).

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

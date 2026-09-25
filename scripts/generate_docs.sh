uv run pydoc-markdown -p koyeb/api >docs/api.md
uv run pydoc-markdown -p koyeb/api_async >docs/api_async.md
# Explicit module list so test modules and fakes stay out of the docs.
# PYTHONPATH is required: the module loader imports instead of walking paths.
PYTHONPATH=. uv run pydoc-markdown \
  -m koyeb.sandbox \
  -m koyeb.sandbox.sandbox \
  -m koyeb.sandbox.exec \
  -m koyeb.sandbox.executor_client \
  -m koyeb.sandbox.filesystem \
  -m koyeb.sandbox.pool \
  -m koyeb.sandbox.snapshot \
  -m koyeb.sandbox.utils \
  >docs/sandbox.md

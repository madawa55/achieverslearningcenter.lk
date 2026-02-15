# Gunicorn configuration file for Achievers Learning Center

import multiprocessing

# Server socket
bind = "unix:/run/gunicorn/achievers.sock"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
worker_connections = 1000

# Timeout
timeout = 120
graceful_timeout = 30
keepalive = 5

# Max requests (auto-restart workers to prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/achievers_access.log"
errorlog = "/var/log/gunicorn/achievers_error.log"
loglevel = "info"

# Process naming
proc_name = "achievers_gunicorn"

# Server mechanics
daemon = False
pidfile = "/run/gunicorn/achievers.pid"
umask = 0o007
tmp_upload_dir = None

# SSL (handled by Nginx, not Gunicorn)
# keyfile = None
# certfile = None

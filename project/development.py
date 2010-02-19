from project.settings import *

DEBUG=False
TEMPLATE_DEBUG=DEBUG

if os.path.exists(os.path.join(os.path.dirname(__file__), "local_development.py")):
    from local_development import *

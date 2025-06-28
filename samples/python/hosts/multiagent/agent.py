from .host_agent import HostAgent


root_agent = HostAgent([
    'http://localhost:10000',  # Currency Agent
    'http://localhost:10003'   # Facts Agent
]).create_agent()

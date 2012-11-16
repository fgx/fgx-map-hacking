"""Setup the fgx application"""
import logging

from fgx.config.environment import load_environment
from fgx.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup fgx here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)

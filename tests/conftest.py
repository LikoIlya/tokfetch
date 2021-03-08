"""Test fixtures to test out security token activities."""
import logging
import os

import pytest
from click.testing import CliRunner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from web3 import Web3, EthereumTesterProvider

from tokfetch.models.implementation import Base


@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / 'db_file.sql')


@pytest.fixture
def dbsession(db_path):
    """We use sqlite in-memory for testing."""
    # https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
    url = "sqlite+pysqlite:///" + db_path

    engine = create_engine(url, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@pytest.fixture
def monkey_patch_py_evm_gas_limit():
    from eth_tester.backends.pyevm import main
    main.GENESIS_GAS_LIMIT = 9999999999


@pytest.fixture
def web3_test_provider(monkey_patch_py_evm_gas_limit):
    return EthereumTesterProvider()


@pytest.fixture
def web3(web3_test_provider):
    return Web3(web3_test_provider)


@pytest.fixture
def network(web3_test_provider):
    """Network name to be used in database when run against in-memory test chain."""
    return "testing"


@pytest.fixture()
def logger(caplog):
    # caplog is pytest built in fixtur
    # https://docs.pytest.org/en/latest/logging.html
    caplog.set_level(logging.DEBUG)
    logger = logging.getLogger()
    return logger


@pytest.fixture
def sample_csv_file():
    """Sample distribution file for tokens."""
    return os.path.join(os.path.dirname(__file__), "..", "docs", "source", "example-distribution.csv")

@pytest.fixture
def click_runner():
    return CliRunner()


@pytest.fixture
def monkeypatch_create_web3(monkeypatch, web3):
    from tokfetch.ethereum import (
        utils
    )
    monkeypatch.setattr(utils, 'create_web3', lambda _: web3)



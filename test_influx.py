import pytest
from influxdb_client_3 import InfluxDBClient3
from influx import influx_connection 


@pytest.fixture
def influx_client():
    """Fixture to create an InfluxDB client for testing."""
    return influx_connection()


def test_influx_connection_success(influx_client):
    """Test case for successful connection to InfluxDB."""
    assert isinstance(influx_client, InfluxDBClient3)

"""
def test_influx_connection_failure():
    #Test case for failure to connect to InfluxDB.
    with pytest.raises(Exception):
        # Modify token, org, or host to intentionally cause a connection error
        influx_connection()
"""
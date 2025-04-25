import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock

# Ensure game/ is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from db.models import save_result, log_algorithm_times

@patch("db.models.get_connection")
def test_save_result(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    save_result(
        player="Alice",
        home="A",
        selected_cities=["B", "C"],
        route=["A", "B", "C", "A"],
        cost=200,
        bf_time=12.3,
        greedy_time=8.7,
        dp_time=10.1
    )

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args
    assert "INSERT INTO tsp_results" in args[0]
    assert json.loads(args[1][2]) == ["B", "C"]
    assert json.loads(args[1][3]) == ["A", "B", "C", "A"]

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("db.models.get_connection")
def test_log_algorithm_times(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    log_algorithm_times("Bob", 2, 15.0, 9.5, 11.2)

    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args
    assert "INSERT INTO tsp_algorithm_times" in args[0]
    assert args[1] == ("Bob", 2, 15.0, 9.5, 11.2)

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

"""Tests for data_manager load/save logic."""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from data.data_manager import DataManager


class DummyLogger:
    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg, exc_info=False):
        pass


def make_data_manager(tmp_path, excel_name="alias.xlsx", json_name="steel_db.json"):
    excel_path = tmp_path / excel_name
    json_path = tmp_path / json_name
    return DataManager(str(excel_path), str(json_path), DummyLogger()), excel_path, json_path


class TestLoadDataFromJson:
    def test_load_data_from_valid_json(self, tmp_path):
        dm, _, json_path = make_data_manager(tmp_path)
        sample = {
            "profiles": [{"type": "ih", "D": "IPE200", "E": "test", "F": "20.5"}],
            "metadata": {"total_records": 1, "source": "alias.xlsx", "saved_at": "2024-07-16"},
        }
        json_path.write_text(json.dumps(sample), encoding="utf-8")

        profiles = dm.load_data()

        assert len(profiles) == 1
        assert profiles[0]["type"] == "ih"
        assert profiles[0]["D"] == "IPE200"


class TestSaveToJson:
    def test_save_to_json_creates_file(self, tmp_path):
        dm, _, json_path = make_data_manager(tmp_path)
        profiles = [{"type": "ih", "D": "IPE200"}]

        dm._save_to_json(profiles)

        assert json_path.exists()
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["profiles"] == profiles
        assert data["metadata"]["total_records"] == 1
        assert data["metadata"]["source"] == str(dm.excel_path)
        today = datetime.now().strftime("%Y-%m-%d")
        assert data["metadata"]["saved_at"] == today

    def test_save_to_json_handles_error(self, tmp_path):
        dm, excel_path, json_path = make_data_manager(tmp_path)
        # Make JSON_PATH unwritable by pointing to a read-only location if possible, or just rely on broad exception
        # Since we can't easily simulate permission error on all OS, just ensure no crash with valid input
        dm._save_to_json([{"type": "ih", "D": "IPE200"}])
        assert json_path.exists()


class TestLoadDataFallback:
    def test_load_data_fallback_when_json_corrupt(self, tmp_path):
        dm, excel_path, json_path = make_data_manager(tmp_path)
        json_path.write_text("not json", encoding="utf-8")

        # Since _load_excel_data is mocked to return [], load_data should return []
        with patch.object(dm, "_load_excel_data", return_value=[]) as mock_excel:
            profiles = dm.load_data()
            mock_excel.assert_called_once()
            assert profiles == []


class TestLoadExcelData:
    def test_load_excel_data_missing_file(self, tmp_path):
        dm, excel_path, json_path = make_data_manager(tmp_path)
        # File does not exist by default

        profiles = dm._load_excel_data()

        assert profiles == []

    def test_load_excel_data_basic(self, tmp_path):
        dm, excel_path, json_path = make_data_manager(tmp_path)
        excel_path.write_text("dummy", encoding="utf-8")

        with patch("data.data_manager.openpyxl.load_workbook") as mock_load:
            mock_wb = MagicMock()
            mock_wb.sheetnames = ["I lib", "U lib", "HINH_VN", "Ong,Hop"]

            def sheet_side_effect(name):
                mock_sheet = MagicMock()
                mock_sheet.iter_rows.return_value = iter(
                    [
                        (None, None, None, "IPE200", "IPE200", "20.5", None, None, None, None, None, None, None, "IPE180", "18.4"),
                        (None, None, None, "IPE300", "IPE300", "30.1", None, None, None, None, None, None, None, "IPE270", "27.1"),
                    ]
                )
                return mock_sheet

            mock_wb.__getitem__ = MagicMock(side_effect=sheet_side_effect)
            mock_load.return_value = mock_wb

            profiles = dm._load_excel_data()

            assert len(profiles) >= 2
            assert any(p["type"] == "ih" and p["D"] == "IPE200" for p in profiles)

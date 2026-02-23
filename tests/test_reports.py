import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from reports import average_gdp
from main import main


def create_csv(tmp_path, name, content):
    file = tmp_path / name
    file.write_text(content, encoding="utf-8")
    return str(file)


def test_average_gdp_single_file(tmp_path):
    file = create_csv(
        tmp_path,
        "test.csv",
        "country,year,gdp\n"
        "USA,2021,20000\n"
        "USA,2022,22000\n"
        "China,2021,15000\n"
        "China,2022,17000\n",
    )

    result = average_gdp([file])

    usa = next(r for r in result if r[0] == "USA")
    china = next(r for r in result if r[0] == "China")

    assert usa[1] == 21000.0
    assert china[1] == 16000.0


def test_average_gdp_multiple_files(tmp_path):
    file1 = create_csv(
        tmp_path,
        "file1.csv",
        "country,year,gdp\nUSA,2021,100\n",
    )

    file2 = create_csv(
        tmp_path,
        "file2.csv",
        "country,year,gdp\nUSA,2022,300\n",
    )

    result = average_gdp([file1, file2])
    assert result[0][1] == 200.0


def test_sorting(tmp_path):
    file = create_csv(
        tmp_path,
        "test.csv",
        "country,year,gdp\nA,2021,100\nB,2021,200\n",
    )

    result = average_gdp([file])
    assert result[0][0] == "B"


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        average_gdp(["no_file.csv"])


def test_main_success(monkeypatch, tmp_path, capsys):
    file = tmp_path / "test.csv"
    file.write_text(
        "country,year,gdp\n"
        "A,2021,100\n"
        "B,2021,200\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--files", str(file), "--report", "average-gdp"],
    )

    main()

    captured = capsys.readouterr()
    assert "B" in captured.out
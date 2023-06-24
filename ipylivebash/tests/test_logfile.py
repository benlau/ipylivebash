from ..logfile import LogFile
from unittest.mock import patch
from datetime import datetime


def test_gen_filename():
    assert LogFile.gen_filename("output.log") == "output.log"

    assert LogFile.gen_filename("output.log", 1) == "output-1.log"
    assert LogFile.gen_filename("output.log", 2) == "output-2.log"

    assert LogFile.gen_filename("output", 3) == "output-3"


def test_gen_filename_with_timestamp():
    mock_date = datetime(2000, 1, 1, 1, 0)
    with patch("datetime.datetime") as mock:
        mock.now.return_value = mock_date
        mock.side_effect = lambda *args, **kw: datetime(*args, **kw)
        assert (
            LogFile.gen_filename("output.log", use_timestamp=True)
            == "output-20000101-010000.log"
        )

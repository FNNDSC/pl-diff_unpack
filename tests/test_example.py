import sys
from pathlib import Path
from unittest.mock import call

from diff_unpack import parser, inputDir2File_do, main, DISPLAY_TITLE


options         = parser.parse_args(['--inputFilter', 'dcm'])


def test_inputDir2File_do_skips_dirs_without_hits(tmp_path: Path):
    inputdir    = tmp_path / 'inputdir'
    outputdir   = tmp_path / 'outputdir'
    inputdir.mkdir()
    outputdir.mkdir()

    file        = inputdir / 'file.txt'
    file.write_text('I am not a DICOM file.')

    assert inputDir2File_do(options, (inputdir, outputdir)) is None


def test_inputDir2File_do_returns_a_dicom(tmp_path: Path):
    inputdir    = tmp_path / 'inputdir'
    outputdir   = tmp_path / 'outputdir'
    inputdir.mkdir()
    outputdir.mkdir()

    # create example data
    dicoms = {
        inputdir / 'file1.dcm',
        inputdir / 'file2.dcm',
        inputdir / 'file3.dcm'
    }

    for dicom in dicoms:
        dicom.touch()

    actual = inputDir2File_do(options, (inputdir, outputdir))
    assert actual is not None
    actual_dicom, actual_outputdir = actual
    assert actual_dicom in dicoms
    assert actual_outputdir == outputdir

def test_main(mocker, tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir    = tmp_path / 'incoming'
    outputdir   = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options     = parser.parse_args(['--example', 'bar'])

    mock_print  = mocker.patch('builtins.print')
    main(options, inputdir, outputdir)
    mock_print.assert_has_calls([call(DISPLAY_TITLE), call("Option: bar")])

    expected_output_file = outputdir / 'success.txt'
    assert expected_output_file.exists()
    assert expected_output_file.read_text() == 'did nothing successfully!'

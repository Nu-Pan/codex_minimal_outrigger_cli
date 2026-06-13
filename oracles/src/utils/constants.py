from enum import Enum


class CmocFileType(Enum):
    """
    cmoc 上のファイル種別
    """

    ORACLES_FILES = "oracles files"

    REALIZATION_FILES = "realization files"
    REALIZATION_CODE = "realization code"
    REALIZATION_IMPLEMENTATION = "realization implementation"
    REALIZATION_TEST = "realization test"
    REALIZATION_ANCILLARY = "realization ancillary"

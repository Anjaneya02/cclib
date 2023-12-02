# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Unit tests for the CJSON reader."""

import os
import unittest
import tempfile

import numpy as np

import cclib


__filedir__ = os.path.dirname(__file__)
__filepath__ = os.path.realpath(__filedir__)
__datadir__ = os.path.join(__filepath__, "..", "..")


class CJSONReaderTest(unittest.TestCase):
    """Unit tests for the CJSON reader."""

    def test_cjson_read(self):
        """File->ccData->CJSON->attribute_dict, the attributes within ccData and attribute_dict
        should be the same."""
        fpath = os.path.join(__datadir__, "data/ADF/basicADF2007.01/dvb_gopt.adfout")
        data = cclib.io.ccread(fpath)
        assert data is not None, "The logfileparser failed to parse the output file"

        cjson_obj = cclib.io.cjsonwriter.CJSON(data, terse=True)
        assert (
            cjson_obj.ccdata == data
        ), "The ccData instance within the CJSON class should be the same as the one generated by the logfileparsers"

        # Generate the CJSON object to be written into a file.
        cjson_data = cjson_obj.generate_repr()

        with tempfile.NamedTemporaryFile(mode="w") as fp:
            fp.write(cjson_data)
            fp.flush()
            read_cjson_data = cclib.io.ccread(fp.name, cjson=True)
        assert read_cjson_data is not None, "The CJSON reader failed to read attributes"

        # The attribute values read by the CJSON reader will be a subset of the
        # total attributes stored by the logfileparser in the ccData object.
        ccdata_dict = data.getattributes()

        # Check if each 'key:value' pair read by the CJSON reader is equal to
        # the corresponding 'key:value' pair present in the ccData object.
        for key in read_cjson_data:
            ccdata_value = ccdata_dict[key]
            cjson_value = read_cjson_data[key]

            # The values in the ccData object might be of numpy types whereas
            # the values obtained by the CJSON reader are of the inbuilt python
            # types.  Conversion of numpy types into python types happens here:
            if isinstance(ccdata_value, (np.ndarray, list)):
                ccdata_value = np.asarray(ccdata_value).tolist()
            if isinstance(ccdata_value, dict):
                temp_dict = {}
                for ccdata_key in ccdata_value:
                    dict_value = ccdata_value[ccdata_key]
                    if isinstance(dict_value, np.ndarray):
                        dict_value = np.asarray(dict_value).tolist()
                        temp_dict[ccdata_key] = dict_value
                ccdata_value = temp_dict

            # The 'moments' attribute present in the CJSON is a post processed
            # value obtained from the moments key within ccData. Hence the
            # values for moments will be always different.  TODO: Create a
            # naming convention for post processed attributes within the CJSON
            # structure.
            if key != "moments":
                assert ccdata_value == cjson_value


if __name__ == "__main__":
    unittest.main()

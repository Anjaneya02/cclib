# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Unit tests for XYZ writer."""

import os
import unittest

import cclib


__filedir__ = os.path.dirname(__file__)
__filepath__ = os.path.realpath(__filedir__)
__datadir__ = os.path.join(__filepath__, "..", "..")


class XYZWriterTest(unittest.TestCase):

    def test_init(self):
        """Does the class initialize correctly?"""
        fpath = os.path.join(__datadir__, "data/ADF/basicADF2007.01/dvb_gopt.adfout")
        data = cclib.io.ccread(fpath)
        xyz = cclib.io.xyzwriter.XYZ(data)

        # The object should keep the ccData instance passed to its constructor.
        self.assertEqual(xyz.ccdata, data)

    def test_subclass(self):
        """Is the writer a subclass of the abstract file writer?"""
        fpath = os.path.join(__datadir__, "data/ADF/basicADF2007.01/dvb_gopt.adfout")
        self.assertTrue(os.path.exists(fpath))
        data = cclib.io.ccread(fpath)
        writer = cclib.io.xyzwriter.XYZ(data)
        self.assertTrue(isinstance(writer, cclib.io.filewriter.Writer))
        self.assertTrue(issubclass(type(writer), cclib.io.filewriter.Writer))

    def test_roundtrip_one(self):
        """Does a written XYZ file with a single structure match a reference
        output?

        Perform a roundtrip test, reading an XYZ file into a ccData
        instance then writing it out again.
        """
        orig_fpath = os.path.join(__datadir__, "test/bridge/uracil.xyz")
        reader = cclib.io.xyzreader.XYZ(orig_fpath)
        data = reader.parse()
        orig_repr = reader.filecontents

        writer = cclib.io.xyzwriter.XYZ(data)
        new_repr = writer.generate_repr()

        ref_fpath = os.path.join(__filedir__, "data/uracil_one_ref.xyz")
        with open(ref_fpath) as ref:
            # Compare the contents of the reference file (left) with
            # the string representation generated by the writer
            # (right).
            assert ref.read() == new_repr

    def test_roundtrip_two(self):
        """Does a written XYZ file with two structures match a reference
        output?

        Perform a roundtrip test, reading an XYZ file into a ccData
        instance then writing it out again.
        """
        orig_fpath = os.path.join(__filedir__, "data/uracil_two.xyz")
        reader = cclib.io.xyzreader.XYZ(orig_fpath)
        data = reader.parse()
        orig_repr = reader.filecontents

        # If not `allgeom`, only the last structure present in a
        # `ccData` will be written out.
        writer = cclib.io.xyzwriter.XYZ(data, allgeom=True)
        new_repr = writer.generate_repr()

        ref_fpath = os.path.join(__filedir__, "data/uracil_two_ref.xyz")
        with open(ref_fpath) as ref:
            # Compare the contents of the reference file (left) with
            # the string representation generated by the writer
            # (right).
            assert ref.read() == new_repr


if __name__ == "__main__":
    unittest.main()

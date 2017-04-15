# -*- coding: utf-8 -*-
# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

import os
import re

import pytest

from tests.conftest import FIXTURE_DIR

from viper.modules import apk
from viper.modules.apk import HAVE_ANDROGUARD
from viper.common.abstracts import Module
from viper.common.abstracts import ArgumentErrorCallback

from viper.core.session import __sessions__


class TestAPK:
    def teardown_method(self):
        __sessions__.close()

    def test_init(self):
        instance = apk.AndroidPackage()
        assert isinstance(instance, apk.AndroidPackage)
        assert isinstance(instance, Module)

    def test_androguard_installed(self):
        assert HAVE_ANDROGUARD is True

    # def test_androguard_not_installed(self):
    #     # assert HAVE_ANDROGUARD is True
    #     HAVE_ANDROGUARD = False
    #     instance = apk.AndroidPackage()
    #     assert isinstance(instance, apk.AndroidPackage)
    #     assert isinstance(instance, Module)

    def test_args_exception(self):
        instance = apk.AndroidPackage()
        with pytest.raises(ArgumentErrorCallback) as excinfo:
            instance.parser.parse_args(["-h"])
        excinfo.match(r".*Parse Android Applications.*")

    def test_no_session(self, capsys):
        instance = apk.AndroidPackage()
        instance.command_line = ["-i"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*No open session*", out)
        # assert out == ""

    @pytest.mark.parametrize("filename", ["hello-world.apk"])
    def test_info(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-i"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*Package Name: de.rhab.helloworld*", out)

    @pytest.mark.parametrize("filename", ["hello-world.apk"])
    def test_perm(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-p"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*APK Permissions*", out)

    @pytest.mark.parametrize("filename", ["hello-world.apk"])
    def test_file(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-f"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*APK Contents*", out)

    @pytest.mark.parametrize("filename,pkg_name", [("hello-world.apk", "de.rhab.helloworld")])
    def test_all(self, capsys, filename, pkg_name):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-a"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*Package Name: {}*".format(pkg_name), out)

    @pytest.mark.parametrize("filename", ["hello-world.apk"])
    def test_dump_no_parameter(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-d"]

        instance.run()
        out, err = capsys.readouterr()

        assert re.search(r".*argument -d/--dump: expected one argument*", out)

    @pytest.mark.usefixtures("cleandir_keep")
    @pytest.mark.parametrize("filename", ["hello-world.apk"])
    def test_dump(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = apk.AndroidPackage()
        instance.command_line = ["-d hello-world.dump"]

        # TODO(frennkie) this test fails (Can't convert 'bytes' object to str implicitly)
        # instance.run()
        # out, err = capsys.readouterr()
        #
        # assert 0

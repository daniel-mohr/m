"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu common_json_format
"""

import json
import jsonschema
import os.path
import subprocess


class mixin_common_json_format():
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_common_json_format(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-19

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu common_json_format'.
        """
        # data bubble 04
        test_dir_path = self.test_dir_path[4]
        cps = []  # completed process instances
        cp = subprocess.run(
            'pydabu common_json_format -f .dabu.json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
        instance = json.loads(cp.stdout)
        with open(os.path.join(test_dir_path, '.dabu.schema'), mode='r') as fd:
            schema = json.load(fd)
        jsonschema.validate(instance, schema)

# Owner(s): ["oncall: jit"]

import io
import os
import sys

import torch
from torch.testing import FileCheck

# Make the helper files in test/ importable
pytorch_test_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(pytorch_test_dir)
from torch.testing._internal.jit_utils import JitTestCase

if __name__ == '__main__':
    raise RuntimeError("This test file is not meant to be run directly, use:\n\n"
                       "\tpython test/test_jit.py TESTNAME\n\n"
                       "instead.")

class TestUpgraders(JitTestCase):
    def test_aten_div_tensor_at_3(self):
        model_path = pytorch_test_dir + "/cpp/jit/div_at_version_3.pt"
        loaded_model = torch.jit.load(model_path)
        FileCheck().check("prim::If").run(loaded_model.graph)
        FileCheck().check_count("aten::div", 2).run(loaded_model.graph)

        buffer = io.BytesIO()
        torch.jit.save(loaded_model, buffer)
        buffer.seek(0)
        loaded_model_twice = torch.jit.load(buffer)
        # we check by its' code because graph variable names
        # can be different every time
        self.assertEqual(loaded_model.code, loaded_model_twice.code)

    def test_aten_test_serialization(self):
        model_path = pytorch_test_dir + "/jit/fixtures/_test_serialization_subcmul_v2.pt"
        loaded_model = torch.jit.load(model_path)
        FileCheck().check_count("aten::mul", 2).run(loaded_model.graph)
        FileCheck().check_count("aten::sub", 2).run(loaded_model.graph)

        buffer = io.BytesIO()
        torch.jit.save(loaded_model, buffer)
        buffer.seek(0)
        loaded_model_twice = torch.jit.load(buffer)
        # we check by its' code because graph variable names
        # can be different every time
        self.assertEqual(loaded_model.code, loaded_model_twice.code)

    def test_aten_div_scalar_at_3(self):
        model_path = pytorch_test_dir + "/jit/fixtures/test_versioned_div_scalar_float_v3.pt"
        loaded_model = torch.jit.load(model_path)
        FileCheck().check("prim::If").run(loaded_model.graph)
        FileCheck().check_count("aten::div", 2).run(loaded_model.graph)

        buffer = io.BytesIO()
        torch.jit.save(loaded_model, buffer)
        buffer.seek(0)
        loaded_model_twice = torch.jit.load(buffer)

        self.assertEqual(loaded_model(torch.Tensor([5.0, 3.0]), 2.0),
                         loaded_model_twice(torch.Tensor([5.0, 3.0]), 2.0))

    def test_aten_div_tensor_out_at_3(self):
        model_path = pytorch_test_dir + "/jit/fixtures/test_versioned_div_tensor_out_v3.pt"
        loaded_model = torch.jit.load(model_path)
        FileCheck().check("prim::If").run(loaded_model.graph)
        FileCheck().check_count("aten::div", 2).run(loaded_model.graph)

        buffer = io.BytesIO()
        torch.jit.save(loaded_model, buffer)
        buffer.seek(0)
        loaded_model_twice = torch.jit.load(buffer)
        # we check by its' code because graph variable names
        # can be different every time
        self.assertEqual(loaded_model.code, loaded_model_twice.code)

    def test_aten_full_at_4(self):
        model_path = pytorch_test_dir + "/jit/fixtures/test_versioned_full_integer_value_v4.pt"
        loaded_model = torch.jit.load(model_path)
        FileCheck().check_count("aten::Float", 1).run(loaded_model.graph)
        FileCheck().check_count("aten::full", 2).run(loaded_model.graph)

        buffer = io.BytesIO()
        torch.jit.save(loaded_model, buffer)
        buffer.seek(0)
        loaded_model_twice = torch.jit.load(buffer)
        # we check by its' code because graph variable names
        # can be different every time
        self.assertEqual(loaded_model.code, loaded_model_twice.code)

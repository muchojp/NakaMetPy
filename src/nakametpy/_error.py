# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
import numpy as np


class MyException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class MyException2(Exception):
    def __init__(self, arg='', array1=None, array2=None):
        self.arg = arg
        self.array1 = array1
        self.array2 = array2

class NotHaveEnoughDimsError(MyException):
    def __str__(self):
        # print(f"NotHaveEnoughDimsError: 変数 {self.arg} は1次元配列です。この変数は最低でも2次元である必要があります。")
        return (
            f"変数 {self.arg} は1次元配列です。この変数は最低でも2次元である必要があります。"
        )

class NotValidDxShapeError(MyException2):
    def __str__(self):
        return (
            f"配列 dx の形が適切ではありません。\n{self.arg} の経度緯度方向は({self.array1.shape[-2]}, {self.array1.shape[-1]}), dx の緯度経度方向は({self.array1.shape[-2]}, {self.array1.shape[-1]-1})またはintかfloatの一定値である必要があります。しかし実際には({self.array2.shape[-2]}, {self.array2.shape[-1]})となっています。"
        )

class NotValidDyShapeError(MyException2):
    def __str__(self):
        return (
            f"配列 dx の形が適切ではありません。\n{self.arg} の経度緯度方向は({self.array1.shape[-2]}, {self.array1.shape[-1]}), dy の緯度経度方向は({self.array1.shape[-2]-1}, {self.array1.shape[-1]})またはintかfloatの一定値である必要があります。しかし実際には({self.array2.shape[-2]}, {self.array2.shape[-1]})となっています。"
        )

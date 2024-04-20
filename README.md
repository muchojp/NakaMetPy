# NakaMetPy

[![PyPI version][pypi-image]][pypi-link]
[![Anaconda version][anaconda-v-image]][anaconda-v-link]
[![pytest][github-actions-image]][github-actions-link]

[pypi-image]: https://badge.fury.io/py/nakametpy.svg
[pypi-link]: https://pypi.org/project/nakametpy
[anaconda-v-image]: https://anaconda.org/muchiwo/nakametpy/badges/version.svg
[anaconda-v-link]: https://anaconda.org/muchiwo/nakametpy
[github-actions-image]: https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml/badge.svg
[github-actions-link]: https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml

## 概要
このモジュールはMetPyの関数をNumPyで動作するように書き換えた関数のほか、
観測データを扱う上で便利な関数が含まれています。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。

そのため変数単位はMetPyとは異なり自分で気をつけて関数に与えなければなりません。
また、関数の鉛直層数および時間のサイズは適当に与えています。利用される際にデータに合わせて引数を関数に渡してください。
さらに、WRFの計算結果を入力する場合は`wrfon`のオプションを1にする必要があります。
なお`wrfon`オプションは使い勝手が悪いため、今後廃止を検討中です。

皆さまのContributionもお待ちしています。

## Abstract
`nakametpy` is a rewrited package of `MetPy` based on `NumPy`.
I appreciate your contribution.

## Documentation
ドキュメンテーションは[こちら](https://muchojp.github.io/NakaMetPy/ "Docs")のページにあります。
Documentation is [HERE](https://muchojp.github.io/NakaMetPy/).

## How to Install
### via Anaconda

```
conda install muchiwo::nakametpy
```

### via PyPI

```
pip3 install nakametpy
```

## Licence
`BSD-3-Clause`

## Citation
```
Nakamura, Y. (2024). NakaMety (Version xxxx.x.x) [Software]. Chiba, Japan. https://github.com/muchojp/NakaMetPy
```
Note: The version number xxxx.x.x should be set to the version of NakaMetPy that you are using.

## Update plans
Next(`2024.x.0` or later):
 - テストケースの追加

To Do: 
 - `wrfon`オプションの廃止
 - MetPyの関数の移植 \[Further addition of MetPy function\]
 - NCLに実装されている関数の移植 \[adding the NCL's function\]
 - 方位角平均を取る関数の作成 \[Add function of Azimuthal Mean\]


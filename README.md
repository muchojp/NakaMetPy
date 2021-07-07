# NakaMetPy

[![PyPI version][pypi-image]][pypi-link]
[![Anaconda version][anaconda-v-image]][anaconda-v-link]
[![pytest](https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml/badge.svg)](https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml)
<!-- [![Travis][travis-image]][travis-link] -->

[pypi-image]: https://badge.fury.io/py/nakametpy.svg
[pypi-link]: https://pypi.org/project/nakametpy
[anaconda-v-image]: https://anaconda.org/muchiwo/nakametpy/badges/version.svg
[anaconda-v-link]: https://anaconda.org/muchiwo/nakametpy
<!-- [travis-image]: https://travis-ci.org/muchojp/NakaMetPy.svg?branch=main
[travis-link]: https://travis-ci.org/github/muchojp/NakaMetPy -->
[github-actions-image]: https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml/badge.svg
[github-actions-link]: https://github.com/muchojp/NakaMetPy/actions/workflows/ci.yml

## 概要
このモジュールはMetPyの関数をNumPyで動作するように書き換えたものです。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。

そのため変数単位はMetPyとは異なり自分で気をつけて関数に与えなければなりません。
また、関数の鉛直層数および時間のサイズは適当に与えています。利用される際にデータに合わせて引数を関数に渡してください。
さらに、WRFの計算結果を入力する場合は`wrfon`のオプションを1にする必要があります。

NakaMetPyは少なくとも2023年1月あたりまでは開発が継続される予定です。
皆さんのContributionもお待ちしています。

## Abstract
`nakametpy` is a rewrited package of `MetPy` based on `NumPy`.
I appreciate your contribution.

## Documentation
ドキュメンテーションは[こちら](https://muchojp.github.io/NakaMetPy/ "Docs")のページにあります。
Documentation is [HERE](https://muchojp.github.io/NakaMetPy/).

## How to Install
### via Anaconda

```
conda install -c muchiwo nakametpy
```

### via PyPI

```
pip install nakametpy
```

## Licence
`BSD-3-Clause`

## New Feature
Latest: `2021.7.x` 

気象庁が解析雨量をプロットする際に用いるカラーマップや
GrADSのcolormaps.gsに搭載されているカラーマップを追加しました。

added colormaps in GrADS (colormaps.gs)

## Update plans
Next(`2021.x.0`): 
 - ~GPU(cupy)対応 \[GPU(cupy) compatible\]~
 
 軽い負荷の作業では GPU を利用するとかえって CPU only より遅くなることが多いため、ひとまず保留する。

To Do: 
 - MetPyの関数の移植 \[Further addition of MetPy function\]
 - NCLに実装されている関数の移植 \[adding the NCL's function\]
 - 方位角平均を取る関数の作成 \[Add function of Azimuthal Mean\]

 

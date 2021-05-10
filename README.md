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
このモジュールはMetPyをNumPyのみで動作するように書き換えたものです。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。

そのため、変数単位はMetPyとは異なり自分で気をつけて関数に与えなければなりません。
また、関数の鉛直層数および時間のサイズはERA5の気圧面の次元のサイズをデフォルトで与えています。そのため、JRA-55やNCEP FNLで使用する際にはlev_lenやt_lenの値を毎回与える必要があります。

NakaMetPyは今後はもっと拡充していく予定です。
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
````

### via PyPI

```
pip install nakametpy
````

Licence: `BSD-3-Clause`

Next(`1.0.0`): 
 - ドキュメンテーションの公開(`dev`には公開済み)
 - Colormapの実装(add colormaps)
 - JMAのデータを読む時に便利な関数の実装


To Do: 
 - MetPyの関数の移植(Further addition of MetPy function)
 - NCLに実装されている関数の移植(adding the NCL's function)
 - 方位角平均を取る関数の作成(Add function of Azimuthal Mean)
 - ~~ドキュメンテーションの作成(Create docummentation webpage)~~

Future:
 - ~~Matplotlibの気象でよく使うであろうカラーマップを返す関数の実装(0.3.0)(Add colormap function which is used often in Meteorology)~~
 - 計算部分のGPU対応(1.x or 2.x)(GPU compatible)

 

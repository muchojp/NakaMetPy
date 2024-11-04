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

## Documentation
ドキュメンテーションは[こちら](https://muchojp.github.io/NakaMetPy/ "Docs")のページにあります。Documentation is [HERE](https://muchojp.github.io/NakaMetPy/).

## 概要
**POINT1**：気象庁のレーダーエコー強度・エコー頂高度・解析雨量を読む関数があります(`util`)。
- 2.5kmメッシュエコー強度/5kmエコー頂高度
- 1kmメッシュエコー強度/2.5kmエコー頂高度
- 1kmエコー頂高度
- 250mメッシュエコー強度

また簡単な単位変換や配列の結合、文字列<>日付の変換を行う関数などがあります(`util`)。

**POINT2**：BUFRファイルを読む関数があります(`bufr`)。

**POINT3**：GrADSや気象庁が利用しているカラーマップがあります(`cmap`)。

**POINT4**：GrADSバイナリを読む関数があります(`grads`)。

**POINT5**：MetPyの関数がNumPyで動作するように書き換えた関数があります

まだMetPyのバージョンが0.xだったときに作成したものです。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。
そのためMetPyとは異なり単位に気をつけてる必要があります。
また関数の鉛直層数および時間のサイズは適当に与えています。利用時にデータに合わせて引数で指定する必要があります。
さらにWRFの計算結果を入力する場合は`wrfon`のオプションを1にする必要があります。
なお`wrfon`オプションは使い勝手が悪いため、今後廃止を検討中です。

皆さまのContributionもお待ちしています。

## Abstract
NakaMetPy provide function
- to read JMA (Japan Meteorological Agency) Radar Echo Intensity/ Echo Top-height/ Radar/Raingauge-analyzed precipitation data (`util`)
- to convert unit, concat array and convert string into datetime, ... etc (`util`)
- to read BUFR data (`bufr`)
- Colormap of **GrADS** and **JMA** (`cmap`)
- to read GrADS binary (`grads`)
- rewrited function of `MetPy` using `NumPy`(`kinematics` and `thermo`)

I appreciate your contribution.

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
**Note**: The version number xxxx.x.x should be set to the version of NakaMetPy that you are using.

## Update plans
Next(`2024.x.0` or later):
 - No planned

To Do: 
 - `wrfon`オプションの廃止
 - MetPyの関数の移植 \[Further addition of MetPy function\]
 - NCLに実装されている関数の移植 \[adding the NCL's function\]
 - 方位角平均を取る関数の作成 \[Add function of Azimuthal Mean\]


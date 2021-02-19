このモジュールはMetPyをNumPyのみで動作するように書き換えたものです。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。

そのため、変数単位はMetPyとは異なり自分で気をつけて関数に与えなければなりません。
また、関数の鉛直層数および時間のサイズはERA5の気圧面の次元のサイズをデフォルトで与えています。そのため、JRA-55やNCEP FNLで使用する際にはlev_lenやt_lenの値を毎回与える必用がある。

NakaMetPyは今後はもっと拡充していく予定です。
皆さんのContributionもお待ちしています。
GitHubで公開することでバージョンの管理を楽にすることも考えています。

Licence: BSD-3-Clause

To Do: 
 - MetPyの関数の移植
 - 方位角平均を取る関数の作成

Future:
 - Matplotlibの気象でよく使うであろうカラーマップを返す関数の実装(0.3.0)
 - 計算部分のGPU対応(1.0.0)

---
[![PyPI version][pypi-image]][pypi-link]
[![Travis][travis-image]][travis-link]

[pypi-image]: https://badge.fury.io/py/nakametpy.svg
[pypi-link]: https://pypi.org/project/nakametpy/
[travis-image]: https://travis-ci.org/muchojp/NakaMetPy.svg?branch=main
[travis-link]: https://travis-ci.org/github/muchojp/NakaMetPy
 

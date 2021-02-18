このモジュールはMetPyをNumPyのみで動作するように書き換えたものです。
気象データをNumPyでベクトル(配列)として扱うことを想定しています。

そのため、変数単位はMetPyとは異なり自分で気をつけて関数に与えなければなりません。
また、関数の鉛直層数および時間のサイズはERA5の気圧面の次元のサイズをデフォルトで与えています。そのため、JRA-55やNCEP FNLで使用する際にはlev_lenやt_lenの値を毎回与える必用がある。

NakaMetPyは今後はもっと拡充していく予定です。
皆さんのContributionもお待ちしています。
GitHubで公開することでバージョンの管理を楽にすることも考えています。

Licence: BSD-3-Clause

To Do: 
・パッケージの名前の決定。NumMetPyがわかりやすい気がするが、nummと打たないと予測変換が一発で行かない。
・MetPyの関数の移植
・方位角平均を取る関数の作成。

---
[![PyPI version][pypi-image]][pypi-link]
[![Travis][travis-image]][travis-link]

[pypi-image]: https://badge.fury.io/py/takuhai.svg
[pypi-link]: https://pypi.org/project/nakametpy/
[travis-image]: https://travis-ci.org/daizutabi/takuhai.svg?branch=master
[travis-link]: https://travis-ci.org/github/muchojp/NakaMetPy

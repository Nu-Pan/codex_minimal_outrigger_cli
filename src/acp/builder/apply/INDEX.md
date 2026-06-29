# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- `cmoc apply fork` で使う agent call parameter builder 群の realization 側パッケージ。変更要約、ファイル単位所見列挙、所見適用の各 parameter 構築入口と、それらが共有する repo root 解決、oracle 側実装の import 準備、oracle parameter の realization 側型への適合処理を収める。
- 各 builder は prompt や parameter 内容の正本を自前で定義せず、対応する oracle 側 builder へ委譲する薄い層として位置づけられる。

## Read this when
- `cmoc apply fork` の agent 呼び出し用 parameter が realization 側からどの入口で構築されるかを探すとき。
- 変更要約、ファイル単位の所見列挙、所見適用のいずれかについて、realization 側 builder が oracle 側 builder を呼び出して戻り値を扱う経路を確認したいとき。
- apply fork 向け builder 全体で共有される repo root 解決、oracle 側 import 経路補正、ACP 型境界の扱いを確認したいとき。

## Do not read this when
- agent call parameter の prompt 内容、出力条件、正本仕様そのものを確認したいとき。この領域は委譲実装なので、対応する oracle 側の本文を読む。
- `cmoc apply fork` コマンド全体の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。この領域は agent call parameter 構築入口に限られる。
- apply fork 以外の ACP builder、CLI 挙動、path model、ACP 型定義そのものを調べたいとき。より直接の実装または正本仕様へ進む。

## hash
- b61afcbe59a8921889d4655a9d05a907c43f8ec6b2d43238acc56489c3b9cb2d

# `__init__.py`

## Summary
- realization apply 向け builder adapter パッケージの位置づけを示す。ファイル自体は説明文のみで、具体的な parameter builder の再公開は下位の adapter が担う。

## Read this when
- realization apply 用 builder adapter の範囲を把握し、具体的な subcommand 用 builder を探すとき。
- realization 系 builder の apply と refactor の担当範囲を区別するとき。

## Do not read this when
- 特定 subcommand の parameter 構築方法や builder の公開 API を調べる場合は、その subcommand の adapter と正本 builder を直接読む。
- CLI の実行手順、差分検査、commit などの runtime 動作を調べる場合は、コマンド処理の実装や関連する仕様を読む。

## hash
- f826a5bac8bd998fa3b25c1e1a4faaebe0a1a1fe62de19e3062e0f78c2b14d60

# `fork`

## Summary
- realization apply fork 用の builder adapter。正本の AgentCallParameter 構築関数を、既存の import 経路から再公開する。

## Read this when
- realization apply fork builder の既存 import 経路や、adapter の互換性を確認するとき。

## Do not read this when
- prompt の内容、差分の扱い、起動パラメータの構築仕様を確認・変更するときは、正本側の builder 定義を読む。
- CLI からの fork 起動や実行フローを調べるときは、呼び出し元の subcommand を読む。

## hash
- 50ede43ea9ebe4ad326e44a9439129cf912b4334bdaf9fd13113119c6b1840eb

# `__init__.py`

## Summary
- 旧来の `acp.builder.indexing.*` 参照を支える互換名前空間について、その維持理由と削除条件を示す。
- 個別の処理ではなく、パッケージ全体の互換入口を残す判断の手掛かりとなる。

## Read this when
- `acp.builder.indexing.*` の利用が残っているか調べ、互換入口を維持または削除する判断をするとき。
- 個別サブモジュールの転送処理と、パッケージ全体の互換性の責務を区別するとき。

## Do not read this when
- 目次エントリー生成の処理や起動パラメータを変更・調査するときは、正本側の indexing 実装を直接読む。
- 個別の `index_entry` 関数の再公開方法を調べるときは、そのサブモジュールの互換ラッパーを直接読む。

## hash
- fd4b0dd11238195b4ce76273d3ffc692eb9e441764952be0b436ba20f60452bf

# `index_entry.py`

## Summary
- 既存の realization 側 import 経路を保つ互換入口です。関数の定義と agent call の組み立ては oracle 側へ委譲します。

## Read this when
- 既存の realization 側参照や公開経路との互換性を確認・変更するとき。

## Do not read this when
- prompt 文面、起動パラメータ、関数の動作を変更するときは、実際の builder 定義へ進んでください。
- コマンド全体の処理手順や目次情報の要件を確認するときは、それぞれの処理の所有元や正本仕様を直接読んでください。

## hash
- 6250929e8aef3d4fa7e09a0b2b69e1cecb8c2ee1b53aa26c9604fbc5fc86d631

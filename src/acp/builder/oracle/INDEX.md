# `__init__.py`

## Summary
- oracle command builder の realization package。oracle command builder 関連のパッケージ入口として機能する。

## Read this when
- oracle command builder の realization package の責務や構成を確認するとき。

## Do not read this when
- oracle command builder 以外の処理を確認するとき。

## hash
- 04f29448a0f9d675976d8cda22279a162a5e8e89a169554a4926766bf0f88d6b

# `edit`

## Summary
- `cmoc oracle edit` builder の realization adapter パッケージ。oracle edit 用 TUI 起動パラメータの生成入口と関連する配置領域を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や、TUI 起動パラメータ生成の実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な prompt 構築仕様や編集処理を確認したいとき。対応する oracle builder または対象実装を直接読む。
- 他の ACP builder や TUI 以外の起動処理を調査するとき。

## hash
- 8eaf93e4d854bf31694349ea8dfbf72a6819a47a09b0f8a42cf7d62f10e377ad

# `investigation`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能への参照先。
- oracle investigation 用の完全な AgentCallParameter を正本 builder に委譲する realization adapter。実行前のリポジトリ解決と editor input 用ディレクトリ準備を担い、investigation launch TUI のパラメータ生成処理への入口となる。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき
- oracle investigation の launch TUI 用 builder や AgentCallParameter 生成の呼び出し経路を確認するとき
- editor input ディレクトリの準備を含む investigation 起動処理を変更・調査するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいときは、パッケージ内の実装ファイルを直接読む
- 正本 builder の prompt 内容や investigation 起動仕様そのものを確認したいとき
- investigation 以外の builder、TUI 実装、または共通パス解決処理だけを調査するとき

## hash
- ebdb0eded51c4843b36edad877803b1b0e31f6fcff21c28327631abb2cecfc39

# `review`

## Summary
- `cmoc oracle review` builder の realization adapter 群を収めるディレクトリ。finding の列挙・判定・統合・妥当性検証に関する canonical builder の再公開と、prompt fence 保護や oracle path 補正などの互換処理への入口を提供する。

## Read this when
- `cmoc oracle review` の finding 関連 parameter builder の caller、互換 adapter、移行状況を確認するとき
- finding や既知理由などの動的内容を prompt に埋め込む際の fence 保護を変更するとき
- symlink 使用時の oracle path 表現や oracle root placeholder の補正処理を確認するとき

## Do not read this when
- canonical builder の正本仕様・実装や prompt 本文を確認したいとき
- oracle review 以外の builder、CLI 実装、共通 prompt fence 処理だけを調査するとき

## hash
- ebbfebc8f1c704d1aee6e19b9d5d066142e68616f551f1ad1bb471ab94ca9714

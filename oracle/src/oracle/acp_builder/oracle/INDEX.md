# `edit`

## Summary
- `cmoc oracle edit` における本命 agent call と、成功後の仕様削減 agent call の起動パラメータ構築を扱うディレクトリです。ユーザー指示の prompt 組み込み、oracle-only の書き込み範囲、モデル・推論設定、作業ディレクトリ、Structured Output、索引付け前処理など、oracle 編集起動の具体的な設定を確認する入口になります。配下には現時点で本文ファイルを含まない空の領域もあります。

## Read this when
- `cmoc oracle edit` の本命または仕様削減 agent call の起動パラメータを変更・確認するとき
- oracle 編集用 prompt の構成、ユーザー指示の埋め込み、ファイルアクセスモード、起動前索引付け設定を確認するとき
- 本命成功後の仕様削減 call に渡す参照境界や、既存未コミット差分の扱いを確認するとき

## Do not read this when
- oracle file の編集ルールや仕様削減そのものの正本規範を確認する場合
- 一般的な agent call パラメータや共通 prompt 構築の挙動だけを確認する場合
- `cmoc oracle edit` 以外のコマンドの起動パラメータを確認する場合

## hash
- d545d4ae86932f4ac05a41e1a58013be44e8fc203295e054dc7b66e027481ac6

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータと、oracle file 調査用の完全プロンプトを構築する実装。
- ユーザー指示を完全プロンプトへ組み込み、oracle 専用の読み取り専用アクセス、作業パス、モデル・推論設定、構造化出力設定、インデックス事前処理を起動パラメータとしてまとめる。
- oracle investigation の起動設定と、調査用 prompt builder の結果を TUI 起動へ渡す処理の入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に使うモデル、推論強度、ファイルアクセスモード、作業ディレクトリを変更・確認するとき。
- oracle file 調査向け完全プロンプトへのユーザー指示の組み込みと、oracle 調査用の固定プロンプト設定を変更・確認するとき。
- 完全プロンプトの構築結果、構造化出力設定、インデックス事前処理を TUI 起動パラメータへ渡す処理を確認するとき。

## Do not read this when
- oracle file の内容、正本仕様、または調査結果そのものを確認するときは、対象の oracle file を直接読む。
- 完全プロンプトの共通構造やレンダリング処理だけを確認するときは、prompt builder や構造文書の実装を直接読む。
- oracle investigation 以外の agent call や一般的な TUI 起動設定を確認するときは、それぞれの起動パラメータ実装を読む。

## hash
- 8083637f83fd63d289681271d31265f2300f2dd810fb6d22965833ce9d81721c

# `review`

## Summary
- このディレクトリは、oracle review における所見の列挙、妥当性理由・反証理由の検証、採否判定、所見の統合に使う Structured Output schema と agent call 定義をまとめた領域です。各ファイルは、所見処理の契約確認と、その契約に対応する prompt・実行条件の調査への入口になります。

## Read this when
- oracle review の所見を生成・検証・判定・統合する処理の入出力契約を確認するとき
- 所見処理用 agent call の prompt、読み取り範囲、worktree、モデル設定、実行条件を確認または変更するとき
- 所見の妥当性を支持・反証する理由や、重複・矛盾を整理する処理の構造を調査するとき

## Do not read this when
- oracle review の所見処理以外の agent call やサブコマンドを調査するとき
- レビュー対象の oracle file や実装そのものの仕様を確認するときは、対象の仕様・実装ファイルを直接読むとき
- 個別の Structured Output schema や prompt 定義だけを確認すれば足りる場合は、対応するファイルへ直接進むとき

## hash
- c12f226d38c2018bd916db5f72029ff4c27c95e5c4c5da145e936965cb0b3327

# `edit`

## Summary
- 空のディレクトリで、現時点では固有の本文や用途を提供していない。配下にファイルが追加された場合の確認入口となる。
- `cmoc oracle edit` の本命 agent call と仕様削減 agent call に関する起動パラメータを構築する。共通 prompt、oracle file 専用の編集境界、モデル・推論強度、作業ディレクトリ、indexing preflight の実行条件を定義する。

## Read this when
- 空ディレクトリへのファイル追加後に、その内容や用途を確認するとき。
- `cmoc oracle edit` の agent call 起動条件、prompt 構築、編集境界、リポジトリルート、indexing preflight の設定を変更または確認するとき。

## Do not read this when
- 空ディレクトリ配下の具体的なファイルを直接確認できるとき。
- 一般的な ACP のパラメータ型・列挙値を確認するとき。
- 共通 prompt 構築規則を確認するとき。
- oracle file の編集内容や仕様そのものを確認するとき。

## hash
- 4476126591f269b9328875515cb36a4ea428c53fdfc031d458c49130bf377a4d

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータと完全プロンプトを構築する定義を含むディレクトリ。oracle 限定・読み取り専用の調査範囲、作業ディレクトリ、モデル品質設定、indexing preflight を固定する起動経路への入口。
- 調査対象のユーザー指示を完全プロンプトへ組み込み、oracle file を根拠とする調査結果と未定義事項の扱いを指定する。具体的な起動パラメータ構築を確認する場合は `launch_tui.py` を読む。

## Read this when
- `cmoc oracle investigation` の TUI 起動動作、oracle 限定のファイルアクセス範囲、完全プロンプトの構築方針を調査または変更するとき。
- oracle 調査起動時の agent call の作業ディレクトリ、モデル・推論設定、構造化出力設定、indexing preflight を確認するとき。

## Do not read this when
- 共通の完全プロンプト生成規則や構造化文書のレンダリングだけを確認したいときは、`build_complete_prompt` や構造化文書関連の定義を直接読む。
- oracle 調査以外の agent call や TUI 起動パラメータを扱うときは、その用途に対応する起動定義を直接読む。

## hash
- 6035ad21afa6a8765d5c21149f2ee0fc9115178d2878b12a1ceb6cf8b3dd4e15

# `review`

## Summary
- oracle review の所見列挙・妥当性検証・採否判定・統合に関する Structured Output schema と、各 agent call の prompt／起動条件をまとめたディレクトリ。レビュー段階ごとの入出力契約や呼び出し設定を確認する入口となる。

## Read this when
- oracle review の所見処理フローを変更・調査するとき
- 所見の列挙、妥当性の擁護・反証、採否判定、重複整理の入出力形式や agent call 設定を確認するとき

## Do not read this when
- レビュー対象 oracle file の仕様本文や個々の所見内容を確認したいとき
- oracle review 共通の prompt 生成規則だけを確認したいとき
- 所見処理以外の oracle 機能を調査するとき

## hash
- 1d729238d7333a307946314115ce4e50f7814a7466880937dace9a901a013b4c

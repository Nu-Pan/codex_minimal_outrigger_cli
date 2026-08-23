# `fork`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- `cmoc oracle edit` が起動する2回の `codex exec` に渡す固定パラメータを構築する実装。
- 本命編集 call では、ユーザー指示を含む完全 prompt、oracle file のみを書き込む境界、最高品質のモデル設定、起動前 indexing を指定する。
- 本命成功後の仕様削減 call では、現在の oracle file と未コミット差分を根拠に仕様を簡素化・整合させる prompt と、同じ編集境界・品質設定・indexing 無効化を指定する。
- 両経路でリポジトリルートを作業ディレクトリとし、oracle 編集用の `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle edit` の本命または仕様削減 agent call の起動パラメータ、prompt、モデル品質設定、ファイルアクセス境界を変更・確認するとき。
- oracle 編集処理で、ユーザー指示を prompt にどう埋め込み、2回の call 間でどの情報を共有するかを確認するとき。
- oracle 編集用 call の作業ディレクトリ、indexing preflight、未コミット差分の扱いを確認するとき。

## Do not read this when
- `cmoc oracle edit` の実際の編集処理や call 実行制御を変更・確認する場合は、対応する実行側実装を直接読む。
- 一般的な prompt の構築規則や SD ノードの Markdown 化だけを確認する場合は、`complete_prompt` や `struct_doc` の定義を直接読む。
- oracle file 自体の編集規約・設計・テスト要件を確認する場合は、関連する oracle の規定ファイルを直接読む。

## hash
- 3c2e46d734d8655e19f6318b59bfd7a2342300a64a289fdd45b27acbcd01bb0e

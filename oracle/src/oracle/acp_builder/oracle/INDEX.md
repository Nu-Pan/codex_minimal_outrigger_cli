# `edit`

## Summary
- `cmoc oracle edit` のメイン編集呼び出しに使う共通パラメータを構築する実装と、その下位の fork サブディレクトリへの入口。ユーザー指示、oracle の未コミット差分、編集境界、実行コンテキストを組み立て、編集 agent 用の `AgentCallParameter` を生成する。

## Read this when
- `cmoc oracle edit` が編集 agent を起動する際の prompt 構築、oracle 専用の書き込みモード、作業ディレクトリ、差分参照、preflight 設定を確認したいとき。
- oracle edit のメイン呼び出しで、ユーザー指示から目標状態・編集範囲・完了条件をどのように固定するか調べるとき。

## Do not read this when
- 編集 agent の実際の編集結果や oracle file の個別仕様本文を確認したいとき。
- `cmoc oracle investigation` など別サブコマンドの起動処理を調べるとき。
- このディレクトリ内の下位 fork 専用の内容だけを直接確認したいとき。

## hash
- 5fd9c45a203ac50811632c5ec6e89806353ef57d841dc8bf123a51b7aa7ba2e4

# `investigation`

## Summary
- oracle file を調査する `cmoc oracle investigation` の TUI 起動パラメータを構築する実装です。
- ユーザー指示、oracle 限定のスコープ、回答要件、関連ポリシーを完全プロンプトへ組み込み、oracle 読み取り専用・エディタ入力引き継ぎ・索引事前確認付きの起動設定を返します。

## Read this when
- `cmoc oracle investigation` の調査プロンプト構成、oracle file の読み取り範囲、または TUI 起動時の固定パラメータを確認・変更するとき。
- 調査結果に根拠ファイルの特定を要求するプロンプト設計や、oracle 専用のファイルアクセス設定を追跡するとき。

## Do not read this when
- 実際の oracle 仕様本文を調査したい場合は、`oracle` 配下の対象仕様ファイルを直接読むべきです。
- 一般的な ACP Builder の共通パラメータ生成や prompt の共通構築規則を確認したい場合は、対応する `basic` または `prompt_builder` の実装へ直接進むべきです。
- realization 側の実装動作やテストを確認したい場合は、この oracle 実装ではなく `src` または `test` 配下を読むべきです。

## hash
- 179a429a524ca7ce54b47924b20858759faf740f69bf282b21d81bfc41fc09d8

# `review`

## Summary
- 対象ディレクトリ本文が提示されておらず、責務を根拠付きで判断できません。

## Read this when
- 対象ディレクトリの本文が追加され、担当範囲を確認したいとき

## Do not read this when
- 本文がない現状では、このエントリーから具体的なレビュー作業へ進む必要があるとき

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

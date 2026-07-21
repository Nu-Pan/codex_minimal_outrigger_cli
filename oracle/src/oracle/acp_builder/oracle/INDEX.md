# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動関連を扱うディレクトリです。現時点では空の `fork` と、TUI 起動パラメータを構築する `launch_tui.py` を含みます。

## Read this when
- `cmoc oracle edit` の TUI 起動方法、編集 prompt、モデル・権限・作業ディレクトリなどの起動設定を確認または変更するとき。
- このディレクトリに追加されたファイルの内容や用途を確認するとき。

## Do not read this when
- oracle file の編集処理そのものを確認または変更するとき。
- prompt 共通生成規則、パス解決、構造化文書のレンダリングを確認または変更するとき。
- `launch_tui.py` など対象ファイルを直接確認できるとき。

## hash
- c2d7be308c0da03ba02dc172c32c84646643a7b7356b27d85318fccd6beb2462

# `investigation`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築し、oracle file 調査向けの完全プロンプトと editor_input ログ保存を扱う実装。固定モデル、推論設定、oracle 読み取り権限、インデックス事前処理を指定した起動情報を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件を変更・確認するとき
- 調査プロンプトの構成や editor_input ログ保存を変更・確認するとき

## Do not read this when
- oracle 調査プロンプトの共通生成規則を変更するときは、まず共通 prompt builder を読む
- TUI 起動後の agent 実行処理や oracle file の内容を調査するときは、対応する実行処理または oracle file を直接読む

## hash
- 7f380ea9b83f602cfad5fcf5e4fdcc220fc6968b7ee974a4b056845a14440eef

# `review`

## Summary
- `cmoc oracle review` の所見生成・判定・統合・擁護・反証に関する AgentCallParameter 実装と Structured Output schema をまとめた領域です。各ファイルは、レビュー用プロンプト、oracle file の読み取り制約、関連所見や理由の受け渡し、出力契約を担います。

## Read this when
- `cmoc oracle review` の所見列挙、採否判定、重複・矛盾の統合、擁護理由や反証理由の生成を変更・調査するとき。
- レビュー用 AgentCall のモデル設定、推論強度、Structured Output schema、oracle-only のアクセス制約を確認するとき。
- 所見や判定結果の JSON 入出力契約を確認するとき。

## Do not read this when
- 通常の ACP builder 実装、一般的な prompt 生成基盤、CLI の通常サブコマンドを調査するとき。
- oracle review の判定基準や仕様文書そのものを確認するときは、対応する oracle review 文書を直接読む。
- INDEX.md のルーティング情報だけを確認するとき。

## hash
- e7392e500943f545331ada0aa4b8457d3310bf8d52b4a0839d543f7e6e715f60

# `basic.py`

## Summary
- AIエージェント呼び出しに必要な論理モデル、推論強度、ファイルアクセスモード、プロンプト、Structured Output schema、作業ディレクトリなどを表す型定義を提供する。
- 呼び出し種別ごとのパラメータ構築処理で使う、モデルクラス・推論強度・アクセスモードの選択肢と、呼び出し設定を確認する入口となる。

## Read this when
- Agent Call のパラメータ項目や列挙値の意味を確認するとき
- モデル、推論強度、ファイルアクセスモード、Structured Output、cwd、indexing preflight の設定を扱う実装を変更・調査するとき

## Do not read this when
- 個別の builder 関数がどの値を選択し、どの prompt を構築するかを確認したいとき
- 列挙値のバックエンドへの具体的な解決やファイルアクセス制約の正本を確認したいとき

## hash
- b5523c17bc962f4c459af2727bdbeacd44b387bf83a7c6f1c5e63675d04dbe10

# `feedback`

## Summary
- フィードバック issue の同一性判定と、report cut 時点での issue candidate 検証に用いる Structured Output schema および agent 起動定義を扱うディレクトリ。既存・新規 issue の判定、候補の現在状態の verdict、各処理の入力閉鎖・参照範囲・実行条件を確認する入口。

## Read this when
- feedback observation が既存 issue candidate と同一か新規かを判定する出力契約や prompt・起動条件を確認するとき
- issue candidate を report cut 時点の evidence に基づいて検証する verdict、human action、参照制約を確認するとき
- feedback issue の同一性判定または現在状態検証の agent call を変更・調査するとき

## Do not read this when
- issue candidate の生成、候補の絞り込み、observation の構造化、report cut や feedback state の管理を確認するとき
- 検証結果や同一性判定結果の具体的な issue 内容だけを確認するとき
- 一般的な JSON Schema の仕様や、実際の検証実装・テストの挙動だけを確認するとき

## hash
- d007b11db6e7fb41488a5721080819f004fe47e0aa0d788053acd4a692db54a9

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成に使う prompt と agent call パラメータの定義を扱うディレクトリ。対象本文を含む完全 prompt、読み取り専用設定、モデル・推論コスト、Structured Output schema、cwd、preflight 設定を確認する入口である。
- `index_entry.py` は indexing 用の呼び出し設定を構築し、`index_entry.json` は生成結果の出力形式を定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt の内容や対象本文の組み込み方を変更・確認するとき
- indexing 用 agent call のアクセスモード、モデル、推論コスト、cwd、preflight 設定を変更・確認するとき

## Do not read this when
- 一般的な `cmoc indexing` サブコマンドの処理や CLI 引数解析を調べるとき
- Structured Output schema の項目や JSON 形式だけを確認するときは `index_entry.json` を直接読むとき
- indexing 以外の agent call パラメータ構築を調べるとき

## hash
- 6bf46e4213cd912b79abb68e49e381af8012976937cfa33708dd69988fee7b44

# `oracle`

## Summary
- oracle 関連の agent call 起動定義を用途別に整理するディレクトリ。`edit` は oracle file 編集・仕様削減、`investigation` は oracle 限定の読み取り調査、`review` は所見処理の入出力契約と判定フローの入口となる。

## Read this when
- `cmoc oracle edit` の起動条件、編集境界、prompt、モデル設定、indexing preflight を確認・変更するとき。
- `cmoc oracle investigation` の TUI 起動動作、oracle 限定の調査範囲、完全 prompt、agent call 設定を確認・変更するとき。
- oracle review の所見列挙、妥当性検証、採否判定、重複整理の入出力契約や起動設定を確認・変更するとき。

## Do not read this when
- 共通の完全 prompt 生成規則や構造化文書のレンダリングだけを確認するとき。
- 特定の oracle file の仕様本文、編集内容、調査結果、個々のレビュー所見を直接確認するとき。
- 一般的な ACP パラメータの型・列挙値や、oracle 以外の agent call の起動定義を確認するとき。

## hash
- 5bf3cefe8e20aeabe9ee869fcf5165fcd963a94e5a179483dc43b6a00dfd618d

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call の prompt と起動パラメータを構築する関数。利用可否だけを観測する最小コスト・読み取り専用の probe を定義し、routing や indexing preflight を無効化した呼び出し設定を返す。

## Read this when
- Codex CLI の quota 回復・利用可能性確認用 agent call の prompt、モデル、推論強度、アクセス権限、実行コンテキストなどの起動設定を変更・確認するとき。

## Do not read this when
- 通常の agent call 構築や prompt の内容を確認する場合は、用途別の agent call 定義を直接読むとよい。
- quota の利用可能性確認ではなく、routing、domain policy、indexing preflight の挙動を調査する場合は、この定義ではなく各機能の実装を読むとよい。

## hash
- 2aa9112142fa4751fad6e3e515939e8215f617048a5959a9bf8901efbed01b9d

# `realization`

## Summary
- `apply` は、`cmoc realization apply fork` が使用する realization 追従用 AgentCallParameter の定義を扱う入口。追従対象の commit 範囲、oracle file の差分、prompt、worktree、権限、モデル、preflight などの起動条件を確認できる。
- `refactor` は、refactor fork 向け agent call の構築定義を扱うディレクトリ。変更要約、および oracle／realization file のレビュー・修正に関する prompt、アクセス方針、実行設定、結果契約の確認入口となる。

## Read this when
- `cmoc realization apply fork` の agent call における prompt 構成や起動パラメータを変更・確認するとき
- oracle file の差分を realization file に追従させる agent call の作業範囲、権限、worktree、モデル、preflight 設定を調査するとき
- refactor fork の変更差分を要約する agent call の責務や実行条件を確認・変更するとき
- refactor fork の oracle／realization file をレビュー・修正する agent call の調査範囲、修正条件、検証条件を確認・変更するとき
- 変更要約またはファイルレビュー・修正の Structured Output schema と、それに対応する prompt 構築定義を確認・変更するとき

## Do not read this when
- realization file 個別の実装やテストの挙動を変更するとき
- apply fork の実行処理そのもの、または別種の agent call の prompt・起動条件を調査するとき
- 実際の refactor 差分、oracle file、realization file の実装内容を調査するとき
- 変更要約やファイルレビュー・修正の処理本体ではなく、別の realization 領域の agent call 構築定義を直接調査するとき
- refactor fork の agent call 実行後の個別の変更内容やレビュー所見だけを確認したいとき

## hash
- ad19cd9ecf009839cf0841ed81fa0773c0613cadb4d67db13dd94e3a7b35f23b

# `session`

## Summary
- `cmoc session join` の git merge conflict marker 解消エージェント向け起動パラメータを構築するディレクトリ。
- 対象ファイルの実パス解決、conflict 解消専用 prompt、リポジトリ書き込み権限、作業ディレクトリ、モデル・推論設定を扱う下位実装への入口。

## Read this when
- `session join` の conflict marker 解消用 prompt やエージェント起動パラメータを確認・変更するとき。
- conflicted_paths の実パス解決、対象ファイル一覧の prompt への埋め込み、conflict 解消用のアクセス方針を確認するとき。

## Do not read this when
- merge conflict marker の解消処理そのものや git 操作を確認するとき。
- 一般的な prompt 構築や通常の agent call パラメータを確認するとき。

## hash
- 2595dfbceb1ba619897f346a990cb2ecb7abe09451a3d610b74688574c447497

# `tui`

## Summary
- `cmoc tui` の対話起動に必要な固定設定と、入力プロンプトから完全プロンプトを構築する処理を定義する。TUI 起動時のモデル、推論、ファイルアクセス、作業ディレクトリ、インデックス事前処理などのパラメータをまとめる入口。

## Read this when
- `cmoc tui` が AI Agent CLI/TUI に渡すプロンプトや起動パラメータを調査・変更するとき
- TUI 起動時のモデル設定、推論設定、ファイルアクセスモード、作業ディレクトリ、インデックス事前処理を確認するとき
- 完全プロンプトの skeleton と実行時構築で共有される構築経路を確認するとき

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータを調査するとき
- 完全プロンプトの共通生成規則そのものを確認・変更するとき
- TUI の画面表示や入力編集の実装を調査するとき

## hash
- 5133c8b55eb7b6c0772f87589f9d4fa441eab184c4c5af8391b162bde3a42f3a

# `acp_builder`

## Summary
- AI エージェント呼び出しの prompt、Structured Output schema、モデル・推論強度・ファイルアクセスモード・cwd・preflight などの起動パラメータを、cmoc の各処理単位ごとに定義する領域。
- 共通の呼び出しデータモデルは直下の基礎定義、用途別の起動定義は indexing、feedback、oracle、realization、session、tui、quota probe の各配下へ進む。oracle review では所見列挙・理由検証・採否判定・統合の個別契約を確認できる。

## Read this when
- 特定の cmoc 機能が起動する AI エージェント呼び出しについて、prompt と Structured Output schema の対応、またはモデル・推論強度・アクセスモード・作業ディレクトリ・indexing preflight を調べるとき
- 共通の AgentCallParameter と、用途別の agent call builder の責務分担を把握してから下位の処理定義へ進むとき
- oracle review の所見処理、feedback issue 判定、realization の apply/refactor、session join の conflict 解消、または TUI・quota probe の呼び出し定義を探すとき

## Do not read this when
- AI エージェント呼び出し自体の実行処理、共通 prompt 生成規則、パス解決、または ACP 基本型の実装だけを確認するときは、それぞれの実装入口を直接読む
- レビュー対象の oracle file、realization file、feedback issue の具体的内容、または INDEX.md のルーティング内容を判断するときは、対象本文を直接読む
- Structured Output schema の一般仕様や、個別の所見・issue の原因と重要度だけを調べるとき

## hash
- 607fa760d48659d4aae0cd3b330c42c9db6bb1c5da9a34993456c5da7d7a72b8

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の設定、パス解決、標準定義、構造化 Markdown 生成という、oracle 実装を支える共通モデル群の入口。設定値や agent call の root context、instruction 標準の合成、StructDoc のレンダリングを扱う対象へ進む際に読む。

## Read this when
- cmoc のリポジトリ固有設定、Codex CLI 設定、oracle review のループ設定を確認・変更するとき。
- agent call の work root・repository root、root placeholder、実パスとの相互変換や Git worktree 探索を調査するとき。
- agent 向け標準の検証・合成・決定的順序・instruction 文面化を確認するとき。
- 構造化文書を Markdown に変換する見出し、cmoc_block／cmoc_ref、コードブロック、参照検証の挙動を確認するとき。

## Do not read this when
- 永続化された設定ファイルの生成・同期・編集処理だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。
- ModelClass、ReasoningEffort、その他の参照元型の具体的な列挙値だけを確認するときは、その型定義を直接読む。
- 個別機能における設定・パスモデル・標準・構造化文書の利用方法だけを確認するときは、利用元を直接読む。
- oracle や realization の仕様、通常の Markdown 記法、構造化文書を利用しない文書生成を確認するときは、この共通モデル群を読まない。

## hash
- 4c5b20c8577c323ed7c92e402386e4484cc0bb06bdd7bc756378e57a67568e16

# `prompt_builder`

## Summary
- cmoc の agent call 向けプロンプトを構成する部品群と、完全プロンプト・エディタ入力・プレースホルダ定義の入口を提供する。oracle／realization の標準、ファイルアクセス、routing、feedback、レビュー、handoff などを用途別に選択・統合する経路を確認したいときに読む。

## Read this when
- agent call に渡す完全プロンプトの構成や、依頼概要・完了条件・補助プロンプト・プレースホルダの統合を調査・変更するとき。
- oracle／realization の扱い、標準の依存関係と統合、レビュー・conflict 解消・editor handoff などの規範選択を確認するとき。
- agent call のファイルアクセス制約、INDEX.md routing、feedback reporting、realization から oracle への参照規則を確認するとき。
- エディタ経由の入力ファイル初期文面や、完全プロンプトへの入力埋め込みを確認するとき。
- プレースホルダ名と文字列・Path の置換先を扱う共通型を確認するとき。

## Do not read this when
- 個別の oracle file や realization file の本文・実装を調査するときは、対象の正本または実装を直接読む。
- 特定の Standard の文面だけを確認したいときは、対応する standard definition を直接読む。
- StructDoc、StandardCollection、FileAccessMode、AgentCallPathContext などのデータ構造や利用側の実際のファイル操作を調査するときは、それぞれの定義元・利用側を直接読む。
- INDEX.md の内容自体や、routing 対象の本文を確認するときは、このプロンプト構築部品群ではなく該当する INDEX.md または本文を読む。

## hash
- 8d257488b3d4217399d292f34109777dfa4b8c252391963d93d6548afc9b8e70

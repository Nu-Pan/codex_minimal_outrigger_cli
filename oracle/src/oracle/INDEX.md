# `acp_builder`

## Summary
- Agent Call Parameter の呼び出し種別、ファイルアクセスモード、prompt、Structured Output schema、cwd、indexing preflight の設定をまとめるデータクラスです。
- feedback issue の同一性判断と現在状態の検証に使う agent call の prompt、参照範囲、出力契約を扱う下位領域です。
- INDEX.md エントリー生成用の Structured Output schema と、対象本文を埋め込んだ読み取り専用 agent call の構築を扱う下位領域です。
- oracle file の編集・調査・レビューに使う agent call の prompt、専用アクセス権限、出力契約を扱う下位領域です。
- Codex CLI の quota 回復確認用に、短い応答を返す読み取り専用 agent call の構築を定義します。
- oracle file の変更を realization file へ反映する処理と、realization refactor の変更要約・レビュー・修正に使う agent call の構築を扱う下位領域です。
- `cmoc session join` の git merge conflict 解消を依頼する agent call の対象ファイル、アクセス権限、preflight 設定を扱う下位領域です。
- `cmoc tui` のユーザープロンプトを完全 prompt に組み込み、リポジトリ書き込み用 agent call の起動設定を構築する下位領域です。

## Read this when
- Agent call の共通パラメータ構造や、呼び出し時のアクセスモード・実行設定を確認するとき。
- feedback issue の同一性判定または候補の現在状態検証に使う agent call の構成を確認するとき。
- `cmoc indexing` の出力形式、prompt、対象本文の埋め込み、読み取り専用の起動条件を確認するとき。
- oracle edit、investigation、review の agent call の調査範囲、書き込み範囲、Structured Output 契約を確認するとき。
- quota の利用可能性を確認する probe の prompt と起動条件を確認するとき。
- oracle と realization の差分追従、realization refactor の要約・レビュー・修正に使う agent call の構成を確認するとき。
- `session join` における conflict marker 解消 agent call の対象指定と起動条件を確認するとき。
- `cmoc tui` のオリジナルプロンプトの受け渡し、完全 prompt の構築、リポジトリルートでの起動条件を確認するとき。

## Do not read this when
- ファイルアクセスモード各値の正本上の意味や Codex CLI sandbox との対応だけを確認したいとき。
- feedback observation の送信、候補の収集・絞り込み、issue 内容の生成や評価を確認したいとき。
- 既存 INDEX.md のルーティング内容や、indexing サブコマンドの実行処理を確認したいとき。
- 具体的な oracle file の要求、調査対象、レビュー基準、または共通 prompt 構築規則だけを確認したいとき。
- 通常の quota 判定ロジックや、probe 以外の実作業を確認したいとき。
- 通常の realization file の実装・テスト・設計規則や、一般的な agent call パラメータ定義を確認したいとき。
- merge conflict marker の検出・解消処理そのものや、`session join` の別処理を確認したいとき。
- 完全 prompt の共通構造、TUI 起動後の実行処理、または `cmoc tui` 以外のパラメータ生成を確認したいとき。

## hash
- 4d7762341b1ced6ca569e19a87d6d8ec5e0ced2e05eb259847819de6e4573bc4

# `editor_input_handoff`

## Summary
- エディター入力を特定の対象へ上書きするための入力契約。スキーマ版、対象ID、書き込む本文を指定する。

## Read this when
- エディター入力の上書き処理が受け取る入力条件や、スキーマ版・対象ID・上書き本文の指定方法を確認したいとき。

## Do not read this when
- エディター入力を上書きする処理の実装を確認したいとき。対象IDの発行規則を確認したいとき。

## hash
- 0546c6e94155e6a00152e113604db89f5fb69242fa92b38b677a68a1e2ef8969

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
- 日本語技術文書のルーティングエントリーを、対象ディレクトリ内の構造化文書・設定モデル・パスモデルの責務に基づいて整理します。

## Read this when
- cmoc の設定集約、パスコンテキストやプレースホルダ解決、構造化文書の Markdown レンダリングを調査・変更するとき。
- これらの実装対象のどれを入口にすべきか、またはディレクトリ内の関連モジュールの責務の境界を確認したいとき。

## Do not read this when
- 個別モジュールのフィールド定義、既定値、具体的な変換規則を確認したいときは、ルーティング情報ではなく該当ファイルを直接読むべきです。
- agent call の生成規則や index エントリー生成処理そのもの、または一般的な CLI 機能を調査するときは、別の仕様・実装対象を直接読むべきです。

## hash
- 01da7b21d4a4bb34d4188332c0c76f0719fcce78b2fcb31d8220c81697804620

# `prompt_builder`

## Summary
- プロンプト生成に共通するプレースホルダ型、完全な agent 向け prompt の構築、エディタ入力の初期文面生成、oracle・realization 概念の組み込み、各種 policy の構築を担う prompt builder の入口。
- プレースホルダ統合、prompt 全体の構成、エディタ入力への埋め込み、oracle・realization の分類、アクセス制限や routing などの policy 反映を確認するための下位要素への入口。

## Read this when
- agent call 用の prompt がどのように構築され、規定・policy・objective・placeholder・補助文面が統合されるかを確認するとき。
- エディタ入力の初期テキストや完全 prompt の埋め込み形式を確認するとき。
- oracle・realization の概念や分類、agent call 共通 policy、ファイルアクセス制限、INDEX routing policy を prompt に組み込む処理を追うとき。
- prompt builder 配下の共通型、prompt 構築、エディタ入力、parts、policy のどの担当へ進むべきか判断するとき。

## Do not read this when
- 個別 policy の意味仕様、oracle・realization の正本仕様、CLI の責務、INDEX.md の具体的な既存エントリーを直接確認したいときは、それぞれの正本仕様や対象ファイルを読む。
- プレースホルダ対応表の型定義だけを確認したいときは basic.py を読む。
- 具体的なテンプレート内容や置換規則だけを確認したいときは complete_prompt.py などの担当モジュールを直接読む。
- プロンプト生成や入力初期化と無関係な struct_doc の構造定義・Markdown レンダリング仕様を確認するとき。

## hash
- 1e742fdbb7b3182cbf49f57010c1946fbaf88d99d702658840670258fb476025

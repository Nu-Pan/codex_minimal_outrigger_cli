# `acp_builder`

## Summary
- AI エージェント呼び出しの論理パラメータ定義と、用途別の agent call 構築定義をまとめる領域。共通の呼び出しモデルを確認する `basic.py`、feedback・indexing・quota probe・oracle・realization・session・tui などの用途別定義への入口を提供する。

## Read this when
- AI エージェント呼び出しの用途別設定や、各フローの prompt・モデル・推論強度・実行権限・cwd・Structured Output schema の対応を調査・変更するとき。
- 用途に応じた agent call 定義の下位対象を選び、呼び出し条件の全体構成を把握するとき。

## Do not read this when
- 個別の oracle file、realization implementation、realization test、CLI 実行処理など、agent call 構築以外の具体的な仕様や実装を確認するとき。
- 共通 prompt 構築、ACP の型定義、パス解決など、用途別 agent call 定義に固有でない仕組みだけを調べるとき。

## hash
- 9a5fe7bfaac3187cbc4b0d3b707dc3d2de4e003b6afecbc13eec0f3014866856

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
- cmoc の oracle 実装における、設定・パスモデル・標準定義・構造化文書生成を扱うモジュール群への入口。設定値や agent call のパス解決、instruction 標準の合成、StructDoc による Markdown レンダリングを調査・変更するときに、該当する下位モジュールへ進むためのルーティング対象。

## Read this when
- cmoc のリポジトリ固有設定、root placeholder と agent call のパスコンテキスト、agent 向け標準、または構造化 Markdown 文書生成の実装入口を探すとき。
- 複数の oracle 共通モデルや文書生成ヘルパーの責務を確認し、該当する下位モジュールを選ぶとき。

## Do not read this when
- 特定の CLI 機能や realization の挙動だけを調査する場合は、その機能の実装・仕様を直接読む。
- 永続化された設定ファイルの同期や doctor の実装、列挙型の定義、標準値の個別利用箇所だけを確認する場合は、それぞれの直接の定義元・利用元へ進む。
- INDEX.md のルーティング情報だけを確認する場合。

## hash
- 018c0fde9b3993302e7a717cde4029175e2f662e0e9d3d77a80f4014c6d39f35

# `prompt_builder`

## Summary
- プレースホルダ名と文字列または Path の置換先を対応付ける型を定義する。プロンプト内のパス・値置換の表現を確認するときの入口。
- 依頼概要・完了条件・各種規則や Standard を統合して agent 向け完全プロンプトを構築する中心処理。プロンプトの構成、注入順序、依存関係、複数 builder の統合を調査するときに読む。
- エディタ経由で後続 agent に渡す入力ファイルの初期表示文面を構築する。案内文、記入欄、完全プロンプトの配置を変更・確認するときに読む。
- agent call 向けプロンプトを構成する個別部品群。oracle・realization、Standard、アクセス制約、routing、feedback などの特定の instruction 構築経路を調査するとき、該当部品への入口として読む。
- realization のレビュー結果を適用する際に、oracle との不適合や致命的な実装問題を修正対象とし、調査開始時点で解消済みの問題を除外する Standard を構築する。
- 複数用途で共有する oracle authority と finding basis の StandardGroup を定義する。oracle／realization の正本関係や所見根拠の共通構成を確認するときに読む。
- session join の conflict marker 解消時に、両 branch と oracle の意味を保ち、推測による破棄や不要な変更を避ける Standard を構築する。
- agent call から editor work file へ handoff する際に、file access・sandbox と正式成果物を維持する Standard を構築する。
- 全 agent call に共通する human feedback reporting の文面を構築する。workload 外の人間対応が必要な問題だけを報告する規則と feedback tool の扱いを確認するときに読む。
- FileAccessMode と call context に応じて、読み書き可能範囲、oracle／realization の編集可否、禁止対象を含む file access rule を生成する。
- INDEX.md 用エントリー生成時に、routing 情報としての意味、本文根拠、必要最小限の意味情報を求める Standard を構築する。
- oracle と realization の分類、責務、配置、正本関係を説明する共通基礎文面を構築する。両者の境界や扱いを前提として確認するときに読む。
- oracle review で所見を成立させるため、fatal・minor の区別と oracle file だけで成立する判定条件を含む Standard を構築する。
- oracle file の作成・変更・レビューに必要な正本性、意図と未定義部分、逆算禁止、実装制約、整合性・検索性の Standard を構築する。
- realization code から対応する oracle file を参照するコメント規則を構築する。realization 実装の作成・変更時に oracle path の記載条件を確認するときに読む。
- realization file の作成・変更・リファクタ・レビューに必要な oracle 適合、現行仕様への限定、repository 固有手順による検証の Standard を構築する。
- INDEX.md を使って対象に近い文書へ絞り込み、本文へ進むための routing rule 文面を生成する。対象選定や INDEX.md の位置付けを確認するときに読む。
- 全用途で利用する Standard 定義を集約する。各 Standard の識別子、適用条件、要求・禁止・許容事項の正本を確認するときに読む。

## Read this when
- agent call 向けプロンプトの構成や、特定の prompt builder 部品・規則・Standard の生成方法を調査または変更するとき
- oracle／realization の扱い、file access、routing、feedback、review、handoff などの instruction がどこで構成されるかを確認するとき

## Do not read this when
- 生成済みプロンプトの利用側や CLI の実際のファイル操作を調査するとき
- 個別の oracle file・realization file の本文や、prompt builder が参照するデータ構造そのものを直接確認したいときは、対応する定義元へ進む

## hash
- 28bcc2bd76a5ca8bbe1a747efa49b9a33b6589dd0ac24dba6e446ef8e57c6492

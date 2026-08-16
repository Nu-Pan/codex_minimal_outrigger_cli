# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの AgentCallParameter を構築する定義を集約する領域です。共通パラメータ契約に加え、indexing、feedback、realization、session、tui、oracle の各処理向けに、prompt、ファイルアクセスモード、モデル・推論設定、Structured Output、作業ディレクトリ、indexing preflight の構成を定義します。
- 個別処理の agent call 設定を調査・変更するときの入口であり、共通のパラメータ型は直下の定義、処理別の prompt と schema は対応する下位ディレクトリへ進んで確認します。

## Read this when
- 特定の cmoc 処理がどのような agent call パラメータと完全 prompt を構築するかを調査・変更するとき
- agent call のモデルクラス、推論強度、ファイルアクセス制御、Structured Output、cwd、indexing preflight の設定箇所を特定するとき
- 処理別の agent call builder を横断して、oracle・realization・feedback などの設定責務の分割を確認するとき

## Do not read this when
- agent call の実行制御や終了結果の処理を調査するときは、呼び出し側または実行処理を直接読む
- モデル名や Codex CLI sandbox の具体的な解決仕様を確認するときは、realization 実装または指定された oracle 文書を読む
- 個別の Structured Output schema、prompt の詳細、または対象処理の通常フローだけを調査するときは、対応する下位要素を直接読む

## hash
- e6e88ad08d1c68b9f12d7ce007246a19da65ae8c10753ac1d6ccfa748b645c9a

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
- cmoc の共通基盤モデルと文書生成ヘルパーをまとめた領域。設定モデル、agent call のパスコンテキストと root placeholder 解決、構造化 Markdown のレンダリングを扱い、それぞれの実装を確認する入口になる。

## Read this when
- cmoc のリポジトリ固有設定、パス表記・root 解決、または構造化 Markdown 文書生成の共通実装を調査・変更するとき
- これらの共通モデルを利用する機能の前提規則を確認するとき

## Do not read this when
- 個別 CLI 機能の実装や oracle review の具体的な処理を調査するとき
- 設定ファイルの実際の保存内容や、特定機能に固有のプロンプト・仕様だけを確認するとき

## hash
- be9a8350716a216f9b6e92ef5c313d0f4e7b4bf77608a7ad536dfbc1f1d3b09b

# `prompt_builder`

## Summary
- agent 向けの完全 prompt を構築する実装群。summary・goal、placeholder 定義、選択式の共通 policy、oracle／realization の基本説明、補助 prompt を所定の順序で統合し、構造化された prompt 要素として返す。
- `parts` は oracle／realization の分類や基本概念など、複数の prompt builder で共有する文面部品への入口。
- `policy` は file access、routing、INDEX エントリー生成、oracle／realization の扱い、レビュー、conflict 解消、editor handoff、feedback reporting など、特定の作業条件で注入する規則への入口。
- エディタ経由のユーザー入力用初期テキストと、placeholder 名から文字列または `Path` への対応付けを扱う定義も含む。

## Read this when
- agent call に渡す完全 prompt の構成、policy の注入条件・順序、summary・goal の配置、または placeholder 定義の統合を変更・調査するとき。
- oracle／realization の基本説明や分類文面を共通 prompt に組み込む経路を確認するとき。
- 特定の作業向け policy、routing 規則、INDEX エントリー生成規則、feedback reporting 規則などを完全 prompt に追加・変更するときは、まずここから該当する下位要素へ進む。
- エディタ入力ファイルの初期表示文面や、完全 prompt へのユーザー入力差し込み位置を確認するとき。

## Do not read this when
- 個別 policy の本文や規則だけを確認する場合は、`policy` 配下の該当対象を直接読む。
- 共有文面部品の具体的な内容だけを確認する場合は、`parts` 配下の該当対象を直接読む。
- StructDoc・StructBlock の仕様、FileAccessMode、または agent call の path context 自体を確認する場合は、それぞれの定義元を直接読む。
- prompt builder を利用する CLI の実装挙動や、INDEX.md のルーティング文書そのものを確認する場合は、利用側の実装または対象文書を読む。

## hash
- 7ef3a025c0ead283f9d75b641078a0d940c103aa87d5f364ee5c79e624928b32

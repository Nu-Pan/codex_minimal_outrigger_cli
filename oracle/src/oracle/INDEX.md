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
- cmoc の共通モデルと文書生成ヘルパーをまとめるディレクトリ。設定モデル、agent call のルートパス・placeholder 解決、構造化文章の Markdown／cmoc_block／コードブロック変換を扱い、それぞれの実装を確認する入口となる。

## Read this when
- cmoc のリポジトリ固有設定や Codex CLI・oracle review の設定構造を変更するとき
- agent call の work root・repository root・run root、または root placeholder の解決規則を確認・変更するとき
- 構造化文書を Markdown に変換する処理、cmoc_ref の検証、cmoc_block やコードブロックの出力を確認・変更するとき

## Do not read this when
- 個別の CLI サブコマンドや oracle review の実処理そのものを確認したいとき
- 設定ファイルに保存された実際の値や人間による調整結果だけを確認したいとき
- このディレクトリのヘルパーを利用する個別機能の挙動を調べる場合に、その利用側の実装を直接確認すべきとき

## hash
- 5329eb514d8df585fe895d9179108f6b28a94bc10c6994d56d1ab5e3b462fcd0

# `prompt_builder`

## Summary
- agent call 向けの完全な構造化プロンプトを組み立てる prompt_builder の構成要素を扱うディレクトリ。placeholder 型、完全 prompt の統合、エディタ入力、oracle／realization の説明文、共通 policy を確認するための入口であり、個別の実装や policy 本文へ進む前のルーティングに使う。

## Read this when
- agent call の prompt 構築全体、構成要素の統合順、placeholder、エディタ入力、oracle／realization の説明、共通 policy のいずれかを変更または確認するとき
- prompt_builder 配下の特定要素を読むべき入口や、関連する policy・定義元を特定したいとき

## Do not read this when
- 特定の policy 本文、placeholder 型、StructDoc などの定義、具体的な prompt 生成ロジックだけを確認したいときは、該当する下位対象を直接読む
- prompt_builder と無関係な CLI 実装、テスト、文書の仕様や挙動を調べるとき

## hash
- 6a30eee20dedb7dffae138f5722f1f8724611fda0eb24586d4b73ab6a6be820d

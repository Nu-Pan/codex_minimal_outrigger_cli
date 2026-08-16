# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの prompt、アクセス権限、モデル・推論設定、作業ディレクトリ、Structured Output を構築する定義群。共通パラメータ契約は直下で確認し、用途別の呼び出し設定は feedback、indexing、oracle、realization、session、tui の各下位対象へ進むための入口となる。

## Read this when
- agent call builder の共通パラメータ契約や論理モデル・推論強度・ファイルアクセスモードを確認するとき
- 用途別 agent call の prompt、起動設定、Structured Output、indexing preflight の扱いを調査するとき
- 複数の agent call 定義にまたがる構成を確認し、対象用途の下位ディレクトリへ進む入口を探すとき

## Do not read this when
- 実際の agent call の実行処理やサブコマンド全体の制御フローを確認するとき
- 個別の oracle file、realization file、feedback state、session の Git 操作そのものを確認するとき
- 共通 prompt の生成規則や Codex CLI sandbox の正本仕様を確認するときは、それぞれの定義元や指定された oracle 文書を直接読む

## hash
- 9b0497f362228612efc2908874f2167b4817e359d5c98a76deb92b5c75ca55ca

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
- cmoc の agent 向け完全プロンプトを構築する prompt_builder の主要要素をまとめたディレクトリ。プレースホルダ型、完全プロンプト生成、エディタ入力の初期内容、oracle／realization の基本説明、用途別 policy collection の定義を扱う。
- 完全プロンプトの構成や policy の合成・依存関係・プレースホルダ統合を調べる場合は中核の prompt builder 実装へ進み、個別の規範や判定内容を調べる場合は対応する policy 定義へ進む入口となる。

## Read this when
- agent 向け完全プロンプトの構築経路、構成要素、動的な policy 注入を調査・変更するとき
- oracle と realization の分類・責務、仕様レビュー、conflict 解消、editor handoff、INDEX.md ルーティングなどの共通方針を確認するとき
- エディタ経由のユーザー入力テンプレートや、プレースホルダ置換対象の共通表現を確認するとき
- 用途別 policy collection の選択規則や、PolicyGroup の合成入口を特定するとき

## Do not read this when
- 個別の oracle／realization file の具体的な仕様や、単一のテスト・実装ケースだけを調べるとき
- 個別 policy の具体的な判定規則だけを確認したいときは、対応する policy 定義へ直接進む
- PolicyCollection や PolicyGroup のデータ構造・衝突検査・render 動作だけを確認したいときは、基本実装を直接読む
- プロンプト生成、oracle／realization、policy と無関係な CLI 処理や設定値を調査するとき

## hash
- cff12cf64ad97325a5998e13ef91aa9f75bb8f8d17cfe6b806aa72b91588f6c5

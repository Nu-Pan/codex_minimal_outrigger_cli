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
- cmoc の設定モデル、agent call のパス解決、instruction policy の合成、構造化 Markdown の生成を担う共通実装群。設定・パス表記・規定の統合・Markdown レンダリングに関する変更や挙動確認の入口となる。

## Read this when
- cmoc の設定項目や既定値、Codex CLI・oracle review の設定を確認または変更するとき
- root placeholder、Git worktree、agent call の作業ルートやリポジトリルートの解決規則を確認または変更するとき
- agent 向け policy の検証・合成・決定的な並び順・instruction 文面への変換を確認または変更するとき
- StructDoc、cmoc_block、cmoc_ref、コードブロック、Markdown の見出しや空行のレンダリング規則を確認または変更するとき

## Do not read this when
- 個別の CLI サブコマンドや realization の業務処理そのものを確認するとき
- 具体的な prompt の構成や policy の宣言内容を確認するときは、それを定義・利用する上位対象へ直接進むべきとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認するとき

## hash
- 2743f9ad44a4ed5a25be857eff2897e86bcdf85708f0b87599bf5ec859951864

# `prompt_builder`

## Summary
- agent call に渡す完全 prompt の構築入口。担当概要・完了条件、共通 feedback 規定、oracle／realization 関連 policy、ファイルアクセス制約、routing 規定、補助 prompt、placeholder 定義を選択・統合し、構造化 prompt として返す。
- placeholder 名と実値の対応を型で表す定義。文字列または Path を置換先として扱う共通表現を確認したい場合に参照する。
- エディタ経由で後続 agent に渡すユーザー入力ファイルの初期文面を構築する定義。記入案内、制約、prompt template の配置、HTML コメント除去の扱いを確認できる。
- oracle／realization の権威関係、実装適合、レビュー、conflict 解消、editor handoff、feedback 報告、ファイルアクセス、INDEX.md routing など、用途別 policy collection と policy group の構成を提供する。個別 policy の具体的な規則ではなく、prompt builder がどの規定群を選択するかを確認するための入口である。

## Read this when
- agent call に渡される完全 prompt の構成、固定部分と動的部分、注入順序を調査・変更するとき
- oracle／realization 関連 policy の依存関係、適用範囲、policy collection の統合を確認するとき
- placeholder 定義の初期化・統合や、エディタ入力テンプレートの生成を調査するとき
- feedback reporting、ファイルアクセス、INDEX.md routing などの共通規定が prompt に入る経路を確認するとき

## Do not read this when
- 個別 policy の要求・禁止・許可事項そのものを確認したいときは、parts 配下の policy 定義を直接読む
- oracle file や realization file の正本仕様、実装、テストの内容を確認したいときは、それぞれの対象を直接読む
- 完全 prompt を利用する CLI や agent 実行側の挙動だけを調査するときは、呼び出し元または実行側を直接読む
- StructDoc、PolicyCollection、FileAccessMode、path context など共通基盤の仕様だけを確認したいときは、それぞれの定義を直接読む

## hash
- 6a23f8afac5681315799ed966ba165276c5871a867043e176576a4ba8d1fdc60

# `acp_builder`

## Summary
- AIコーディングエージェント呼び出しの用途別定義をまとめるディレクトリ。基本パラメータ契約、feedback issue 判定、INDEX.md エントリー生成、oracle 操作、quota probe、realization、session conflict 解消、TUI の各 agent call の起動設定・prompt・Structured Output 契約を確認できる。

## Read this when
- 特定の cmoc 機能が構築する agent call の prompt、モデル、reasoning effort、ファイルアクセス、cwd、preflight、Structured Output 設定を調査・変更するとき
- 用途別の agent call 定義の責務や入口を確認するとき
- agent call の出力契約や JSON schema と、その起動定義の対応を確認するとき

## Do not read this when
- agent call の共通型、共通 prompt 生成、パス解決など、配下の用途別定義に固有でない処理を調査するとき
- realization の具体的な実装・テストや oracle file 自体の仕様内容を確認するとき
- 既存の INDEX.md のルーティング内容だけを確認するとき

## hash
- d424fce50a5610b399f5606c716a2457153b4180e2378e5c0abe4ed0a5ec275b

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
- oracle/src/oracle/other は、cmoc の複数機能が共有する補助モデルと文書化ヘルパーを扱うディレクトリである。
- cmoc_config.py はリポジトリ固有設定、Codex CLI 設定、oracle review のループ上限とシリアライズ対象を確認する入口である。
- path_model.py は root placeholder、Git worktree からの root 解決、agent call のパスコンテキストを確認する入口である。
- struct_doc.py は構造化文書ノードを Markdown に変換し、見出し階層、cmoc_block/cmoc_ref、コードフェンス、規定文章を扱う処理の入口である。

## Read this when
- 複数の機能から共有される cmoc 設定モデル、パスモデル、または構造化 Markdown 生成ヘルパーの責務を確認するとき
- 設定項目や既定値、JSON/TOML 化の対象を確認するときは cmoc_config.py を読むとき
- root placeholder や worktree root、repository root、agent call のパスコンテキストの解決規則を確認するときは path_model.py を読むとき
- 構造化文書のノード型や Markdown レンダリング規則を確認するときは struct_doc.py を読むとき

## Do not read this when
- 特定の CLI サブコマンドや realization の処理フローだけを確認したいとき
- Codex CLI の呼び出し実装や oracle review の所見生成ロジックを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき
- 構造化文書ヘルパーの利用側が定める仕様や呼び出し元の責務だけを確認したいとき
- INDEX.md のルーティング規則や文書全体のナビゲーションだけを確認したいとき

## hash
- 2d59e9705d8be1d2d0f6cc2db9ef0a6098a3f509f1a086fa4122680ad8668565

# `prompt_builder`

## Summary
- agent call 向け完全プロンプトを構成する実装と、その構成部品・policy 定義をまとめたディレクトリ。完全 prompt の組み立て、placeholder の統合、エディタ入力初期文面、共通規範や用途別 policy の生成経路を調べる入口であり、個別 policy や構造化文書の詳細は配下の対応対象へ進む。

## Read this when
- agent call に渡す prompt の構成や挿入順序、placeholder の扱いを確認・変更するとき
- prompt builder の共通部品、policy、oracle・realization の規範、routing などの組み込み経路を調査するとき
- エディタ入力の初期文面や、prompt policy の適用条件を確認するとき

## Do not read this when
- 特定の policy の本文や規則だけを確認したいときは、配下の対応する policy 定義を直接読む
- oracle・realization の正本仕様や実装、構造化文書要素の定義を確認したいときは、それぞれの担当ファイルを直接読む
- 生成済み prompt の結果や CLI の実行処理だけを調査する場合

## hash
- 6d587e938c82bbab5a6755af24c93ad0461eaa0001e7263fc798830e3a0033ee

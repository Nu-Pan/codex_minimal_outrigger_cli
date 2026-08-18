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
- cmoc の共通基盤となる補助モデル群を収録するディレクトリ。リポジトリ固有設定のデータモデル、root placeholder と agent call のパス解決、構造化文書の Markdown レンダリングを扱う。これらの共通モデルや変換規則を確認・変更する際の入口であり、個別 CLI 機能の実装や正本仕様の入口ではない。

## Read this when
- cmoc の設定モデル、パス表記・root 解決、または構造化 Markdown 生成の共通処理を確認・変更するとき
- agent call の作業コンテキスト、repository/worktree root、root placeholder の相互変換規則を調べるとき
- 見出し、参照タグブロック、コードブロック、規定文を Markdown へ変換する処理を調べるとき

## Do not read this when
- 特定の CLI サブコマンドや realization の責務・処理フローだけを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき
- 共通モデルを利用する個別機能の挙動を確認する場合で、その機能の実装や仕様を直接読むべきとき

## hash
- aa9999b696095a0c527081e3ef8637690ae32d429f61441abaa66730afff6a60

# `prompt_builder`

## Summary
- agent 向け完全プロンプトの構成部品を実装するディレクトリ。placeholder 型、完全 prompt の組み立て、エディタ入力の初期文面、共通 prompt parts、用途別 policy を扱い、prompt builder の仕様や変更箇所を確認する入口となる。配下には prompt 全体の構成、共通規範、個別 policy へ段階的に進める構造がある。

## Read this when
- agent call に渡す完全 prompt の構成・挿入順序・policy 選択・placeholder 統合を確認または変更するとき
- エディタ入力用の初期文面やテンプレート埋め込みを確認または変更するとき
- oracle・realization の責務境界、ファイル分類、アクセス規則、handoff や conflict resolution などの prompt 部品を確認するとき
- 特定の prompt policy の適用条件や instruction 文面の構成を確認するとき

## Do not read this when
- oracle や realization の正本仕様・実装・テスト本文を直接確認したいとき
- CLI のファイルアクセス処理や、生成済み prompt の利用側の挙動だけを確認したいとき
- 特定 policy の本文だけを確認したい場合は、ディレクトリ全体ではなく対応する個別 policy へ直接進むとき
- SDHeader・SDTagBlock など構造化文書の定義自体を確認したいとき

## hash
- cb347dd251d03b9b61eda66115f98d433777503ca89d4f3f05005b76d9bed057

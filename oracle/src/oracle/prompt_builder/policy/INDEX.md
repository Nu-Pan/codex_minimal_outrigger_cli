# `conflict_resolution.py`

## Summary
- session_join の merge conflict 解消結果に適用する instruction 文面を構築する。両方のマージ元ブランチの oracle file の意図・挙動を維持し、両立不能な事項は未解消として報告する規定を扱う。

## Read this when
- session_join の conflict 解消方針や、解消結果に求める規定を確認するとき。
- conflict resolution policy の prompt 構築を変更・実装するとき。

## Do not read this when
- session_join の意味仕様や oracle file 規定の優先順位そのものを確認したいときは、指定された app_spec の仕様を直接読む。
- merge conflict 解消処理の realization 実装や、個別 oracle file の内容を確認するとき。

## hash
- 4c773c45dc489eb3054ff5d7a6b9ee91ea8bcb8f4a5e8a49f08d501ed41a3dcc

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定をプロンプトへ組み込むポリシー構築関数。人間へ報告する対象の範囲、必須の MCP tool、報告禁止条件を定める。

## Read this when
- agent call 共通の human feedback reporting ポリシーを確認・変更するとき。
- セッション内の規定だけでは解決できない問題を人間へ報告するためのプロンプト構成を確認するとき。
- feedback 報告時の必須事項や禁止事項が、生成されるポリシーへどう反映されるかを確認するとき。

## Do not read this when
- feedback 報告以外のプロンプトポリシーを確認するとき。
- 報告基準の意味仕様そのものを確認するときは、対象関数ではなく指定された意味仕様を直接読むとき。

## hash
- 750c9d861d2b59fb0f1a15407cb82cf56492afbddfce03347dc49bf1e6e1b499

# `file_access.py`

## Summary
- ファイルアクセスモードごとのエージェント向け読み書き制限文面を構築する実装。リポジトリ外、管理用ディレクトリ、AGENTS.md・INDEX.md・memo、oracle file・realization file などの禁止範囲を共通規則として組み立て、READONLY／PURE_ORACLE_READ／REPO_WRITE／PURE_ORACLE_WRITE／REALIZATION_WRITE のモード差分を反映した SDHeader とプレースホルダー定義を返す。NO_POLICY では空の規定を返す。

## Read this when
- エージェントに提示するファイルアクセス制限の文面を追加・変更・確認するとき
- FileAccessMode と AgentCallPathContext に応じた oracle file／realization file のアクセス境界を確認するとき
- アクセス規定を表す SDHeader、SDPolicy、プレースホルダー定義の生成経路を追うとき

## Do not read this when
- ファイルアクセス制限の文面やモード別の禁止規則に関係しない、他のプロンプト生成処理だけを調べるとき
- 実際の oracle file や realization file の内容・実装適合性を直接確認することが目的のときは、それぞれの対象を直接読む

## hash
- 7f86abe5154975843f5eb3111a5d35f75b840b7267295a7974b4f9050e223fb6

# `index_entry.py`

## Summary
- INDEX.md エントリーを生成する agent 向けの構築定義。ルーティング情報に含めるべき判断材料と、避けるべき記述を SDPolicy として定める。INDEX.md のエントリー生成方針を組み立てる処理の入口である。

## Read this when
- INDEX.md エントリー生成用のプロンプト方針を確認・変更するとき。
- ルーティング情報に記載する責務、読む条件、境界、禁止事項の定義を確認するとき。

## Do not read this when
- 個別の対象を案内する既存 INDEX.md エントリーを確認するとき。
- INDEX.md エントリー生成方針の根拠となる関連仕様を直接確認するとき。

## hash
- d1308402ec3ede69802fd23f408bc77c7ecb7e3723d5bac8cbc5cb67319a2a92

# `oracle.py`

## Summary
- oracle file を扱う agent call 向け instruction 文面の構築定義。oracle file に適用する規定を SDPolicy として組み立て、プロンプト生成処理へ渡す。
- oracle と realization の基本要件、指示の優先順位、関連 oracle file の特定方法、goal・non-goal・実装差の許容境界・定義済み事項と未定義事項の明示を扱う。
- 正本仕様を実装や一般論から逆算しないこと、仕様の矛盾・重複・誤りを残さないこと、oracle file を認知負荷の低い仕様断片として保つことを規定する。

## Read this when
- oracle file に関する agent call 向け指示やポリシーの構築内容を確認・変更するとき
- oracle と realization の要件、仕様の優先順位、関連 oracle file の参照方法を確認するとき
- 正本仕様の記述方針や、仕様と実装の許容境界を確認するとき

## Do not read this when
- realization file の具体的な実装責務や配置を確認するとき
- oracle file 以外の agent call instruction の構築内容だけを確認するとき
- 通常のプロンプト生成処理や PlaceholderMap の一般的な扱いを確認するとき

## hash
- b3d29a776d27379dd26e1a7479ca2f1f0aa82261d0058aebafc603758d68d123

# `oracle_findings.py`

## Summary
- 対象は oracle file に対する所見（findings）が満たすべき判定規定を共通定義するポリシー構築関数。所見の成立条件、fatal/minor の扱い、根拠の範囲、重複禁止を扱い、oracle review の各ステップで共有される規定への入口となる。

## Read this when
- oracle file のレビューで所見の列挙・統合・擁護・反証・採否判定の基準を確認するとき
- fatal または minor 所見として成立する条件や、許容される根拠の範囲を確認するとき
- oracle review の各ステップに共通する findings policy の定義を調べるとき

## Do not read this when
- oracle review の意味仕様そのものを確認したいときは、本文が参照する oracle_review.md を直接読む
- 所見の具体的な内容や個別 oracle file の適合性を確認したいときは、対象の oracle file とレビュー手順を直接読む
- 所見ポリシー以外の prompt builder の構築規定を確認したいときは、該当する各 policy 定義へ直接進む

## hash
- 0cf6fed0cef226884a34b2daa94bc35e4f192d737bacbca9afd0f8bcf9da38e3

# `realization.py`

## Summary
- realization file を扱う agent call 向けの instruction 文面を構築するポリシー定義。関連する oracle file の確認、仕様の最小限の補完、正本の一元化、必要な実装・テスト・設定の維持、責務境界の整理、追跡手順に基づく検証を要求事項として組み立てる。
- realization file の既存挙動から仕様を逆算すること、oracle file の仕様を重複して正本化すること、旧仕様や将来用途だけの公開面・抽象化を残すこと、簡潔化で必要な意味や検証を損なうことを禁止事項として組み立てる。
- パスコンテキストからルートのプレースホルダー定義を取得し、realization policy という構造化ヘッダーとポリシーを返す。

## Read this when
- realization file に関する agent call の instruction 生成規則を確認・変更するとき
- realization file の実装、テスト、設定、責務境界、正本参照、または検証方針を扱うとき

## Do not read this when
- oracle file 自体の正本仕様や realization file の意味仕様を確認したいとき
- 特定の realization 実装やテストの内容を直接確認したいとき

## hash
- 2bf3d550c58636f38b82cfcbbe687547927e2c0b368e13190de85a910f614e4b

# `realization_findings.py`

## Summary
- Oracle file と realization file の適合性レビューに用いる所見ポリシーを構築する関数を定義する。具体的な不整合や realization file 単独で説明できる致命的問題を修正対象とし、根拠の特定と修正後の仕様適合を要求する。
- realization findings policy の内容は、oracle file の明示要求に基づく適合性判断のプロンプト構築に使われる。

## Read this when
- oracle file に対する realization file の適合性をレビューする agent 向けポリシーを確認・変更するとき
- 所見の修正対象、根拠の提示、禁止事項をプロンプトへ組み込む処理を調べるとき

## Do not read this when
- oracle と realization の意味仕様そのものを確認したいときは、参照先として示された oracle_and_realization.md を直接読む
- プロンプト構築の共通型や PlaceholderMap の仕様だけを確認したいときは、SDHeader・SDPolicy または PlaceholderMap の定義を直接読む

## hash
- 24eb473ad3d380cecac9a49215e1e67a46f815e4b017daf6df7c184d63a09c05

# `routing.py`

## Summary
- `INDEX.md` によるファイル・ディレクトリの routing policy を構築する関数を定義する。
- 作業対象に近い階層の `INDEX.md` を起点とし、対象領域を推定できない場合はリポジトリルートの `INDEX.md` を起点にする規定や、本文を優先する規定を prompt 用の定義として組み立てる。
- routing policy の意味仕様を確認しながら、エージェント呼び出しのパス情報から必要な定義を取得して利用する。

## Read this when
- `INDEX.md` の routing policy を prompt に組み込む処理を変更・調査するとき。
- `AgentCallPathContext` から routing policy 用の定義を構築する処理を確認するとき。
- routing policy の規定文面や、その参照先である indexing 仕様との対応を確認するとき。

## Do not read this when
- 個別の `INDEX.md` の内容や routing policy の利用先だけを確認したいとき。
- `AgentCallPathContext` 自体の一般的なパスモデルを調査する場合に、routing policy の構築処理が関係しないとき。

## hash
- c52d4a79a646fb878182d66fd89d070f7b6a95c254e3fed99a4070cbd6f57d56

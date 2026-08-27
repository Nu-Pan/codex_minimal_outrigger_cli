# `conflict_resolution.py`

## Summary
- session join の merge conflict 解消結果に適用する instruction 文面を構築する policy 定義。両マージ元の oracle file の意図・挙動を維持し、両立不能な事項は未解消として報告する規定を扱う。conflict 解消の優先順位を確認する際の入口となる。

## Read this when
- session join の merge conflict 解消結果が満たすべき規定を確認するとき
- 両マージ元の oracle file の意図・挙動の維持や、両立不能な事項の報告方針を確認するとき
- realization file を根拠とした oracle file の意味変更や、不必要な conflict marker 解消変更を避ける条件を確認するとき

## Do not read this when
- session join 以外の conflict 解消方針を確認するとき
- merge conflict の具体的な解消手順や oracle file の意味仕様そのものを確認するときは、対応する session join の仕様を直接読む場合
- prompt builder の共通構造や別の policy の内容だけを確認するとき

## hash
- 95553e9e957f669b55c88aceaed58f6fa83392a0f6d331a32fafcee9f9cf78ab

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
- oracle file を扱う agent call 向け instruction 文面の構築定義。oracle file に求める規定を、SDHeader と SDPolicy を用いて返す。
- oracle と realization の基本要件、指示の優先順位、goal・non-goal、実装差の許容境界、関連 oracle file の参照、仕様上の定義事項と未定義事項の区別を扱う。
- oracle file の問題を調査する場合に限り実装上の制約を判断材料にできる一方、realization から仕様を逆算することや、未定義事項・一般論を正本仕様として補うことを制限する。

## Read this when
- oracle file に関する agent call 向け instruction の構築規定を確認するとき
- oracle file と realization file の責務境界、指示の優先順位、仕様断片の記述方針を確認するとき
- oracle policy の必須・禁止・許容事項を変更または参照するとき

## Do not read this when
- oracle file の具体的な仕様内容そのものを確認したいときは、対象となる oracle file を直接読む
- プロンプト構築の基本的な placeholder 処理だけを確認したいときは、PlaceholderMap や oracle.prompt_builder.basic の定義を直接読む
- oracle と realization の意味仕様を確認したいときは、doc/app_spec/oracle_and_realization.md など参照先の正本仕様を直接読む

## hash
- 0bf5df893085c20d1d9e462c4a96c6075b27083fe7d1842ea6eb97e7059a3254

# `oracle_findings.py`

## Summary
- oracle file に対する所見の判定規定を構築する関数を定義する。所見が根拠とすべき対象、fatal／minor の分類基準、基準の一貫性、禁止事項を SDPolicy としてまとめ、レビュー手順で共通利用するための入口となる。

## Read this when
- oracle file の所見に対する判定基準や分類規則を確認・変更するとき
- レビュー手順で共通利用する oracle findings policy の構築方法を確認するとき

## Do not read this when
- 所見の意味仕様そのものを確認する場合は、本文が参照する oracle_review.md の所見定義を直接読むとき
- 所見規定以外の prompt builder policy の内容を確認するとき

## hash
- e67a15ed534f4e44df25e8815f3ac717b53ac6964e34c56662cb563f5cb9fd0a

# `realization.py`

## Summary
- realization file を扱う agent call 向けに、realization file の実装・テストが従うべき規定を、パス文脈のプレースホルダー定義と構造化ポリシーとして構築する関数。oracle file を正本仕様として扱うこと、明示要求を満たす範囲での補完、既存実装の優先利用、YAGNI、重複実装の整理、検証要件、禁止事項および限定的な代替実装許可を instruction 文面に反映する。realization policy の生成ロジックや、その policy が agent call に渡す規定を変更・確認するときの入口となる。

## Read this when
- realization file を扱う agent call の instruction 文面や policy 構築を変更・確認するとき
- realization file と oracle file の関係、実装者裁量、YAGNI、検証・テスト要件を agent 向け規定に反映するとき
- realization policy の構造化ヘッダーや path context 由来の placeholder 定義を調査するとき

## Do not read this when
- realization file 自体の実装内容や個別仕様を確認する場合は、対象の realization file または関連する oracle file を直接読むとき
- 一般的な prompt builder の共通処理を確認する場合は、共通の prompt builder 実装へ直接進むとき
- oracle と realization の意味仕様そのものを確認する場合は、doc/app_spec/oracle_and_realization.md を直接読むとき

## hash
- 2faaaf10cbb978a7f996620811948214e7c70590798671ad80ddc760bf236c2d

# `realization_findings.py`

## Summary
- このモジュールは、oracle file と realization file の適合性を判定する agent 向けの「realization findings policy」を構築する。所見の根拠、修正対象となる不整合・致命的問題、一貫した判定基準、および禁止事項を定義するポリシー生成の入口である。

## Read this when
- oracle file に対する realization file の適合性レビューや、その所見に適用する必須・禁止事項を確認するとき
- realization findings policy をプロンプトへ組み込む処理を調査・変更するとき

## Do not read this when
- プロンプトポリシーの共通データ構造そのものを確認する場合は、SDHeader・SDPolicy の定義を直接読むとよい
- realization file の具体的な実装挙動や oracle file の適合性仕様を確認する場合は、各 realization file または参照先の oracle 仕様を直接読むとよい

## hash
- c3df89df2279c1ad05bba92e0a644d4589f9e7c789892fca8025f5df5a565055

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

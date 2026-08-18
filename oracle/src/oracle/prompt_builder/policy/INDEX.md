# `apply_review.py`

## Summary
- oracle file に対する realization file の適合性を判断する規定を定義する。oracle を正本仕様として扱い、明示要求と realization の挙動が不整合な場合や、realization 単独で実行不能・明白な致命的バグがある場合の修正対象を判断するための入口となる。

## Read this when
- oracle file と realization file の具体的な記述・挙動を比較して、追従要否、所見、修正対象を判断するとき
- realization の修正後に、関連する oracle file の明示要求を満たしているか確認するとき
- oracle を根拠にした適合性判断の扱いと、所見・修正対象の判断基準を確認するとき

## Do not read this when
- oracle file の内容を変更する必要があるとき
- oracle file や realization file の適合性、実行不能性、明白な致命的バグを判断しないとき
- 一般的なコード品質、好み、仕様の隙間、複数の妥当解、推測だけに基づく改善を検討するとき

## hash
- f39acb3c93fcef3a46c7c74c8fa0fb8f73fa8437bf6f8249b0fa842d058d9e97

# `basic.py`

## Summary
- 現在のファイルは空で、定義・処理・設定を担っていません。内容を確認する必要がある場合の最小限の入口です。

## Read this when
- 対象ファイルが空であることや、内容が存在しないことを確認するとき

## Do not read this when
- prompt_builder のポリシー挙動を調査・変更するとき
- 実装や仕様を確認するときは、内容を持つ該当ファイルを直接読む

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `conflict_resolution.py`

## Summary
- `cmoc session join` の conflict marker 解消時に使う instruction 文面を構築する policy 定義。oracle file を人間所有の正本仕様として扱い、conflict 両側と関連 oracle file を確認して意図・挙動を両立させるための入口。両立不能時の未解消報告や、realization 起因の oracle 意味変更禁止など、conflict 解消時の判断境界を扱う。

## Read this when
- `cmoc session join` の conflict marker 解消に関する prompt policy を確認・変更するとき
- oracle file と realization file の conflict 解消規則、または conflict 解消時の変更範囲を確認するとき

## Do not read this when
- conflict marker の解消を扱わない prompt policy を確認するとき
- `SDHeader` や `PlaceholderMap` の共通実装・型定義を確認するとき
- oracle file や realization file 自体の仕様・実装内容を確認するとき

## hash
- e649d68daa4eb44e5665399d742a8eb211324cfa7f8644a458c52d62a46fdd7d

# `editor_handoff.py`

## Summary
- agent call から editor work file へ handoff する際に、file access mode と Codex CLI sandbox を維持しつつ、正式な成果物も満たすための instruction 文面を構築する。handoff file への書き込みが必要な場合に限定的な sandbox escalation を許容するポリシーの入口。

## Read this when
- agent call から editor work file への handoff ルールを定義・変更するとき
- handoff 時のアクセス権限、sandbox 維持、成果物要件、限定的な escalation の扱いを確認するとき

## Do not read this when
- editor work file 以外への handoff や、一般的な agent call の prompt 構築規則を確認するとき
- handoff policy の利用条件が確定しており、対象の具体的な instruction 文面だけを確認すればよいとき

## hash
- c759bb8a9338d833bdc82a965390d569292ba132a0966183732ce657602112ab

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告ポリシーを構築する関数を定義する。
- `AgentCallPathContext` を受け取り、追加の placeholder なしで、未解決問題の報告方法と報告不要な情報を記載した `SDHeader` を返す。

## Read this when
- agent call 共通の feedback 報告規定を生成・変更するとき
- prompt builder の policy 構築処理や `SDHeader` の内容を確認するとき

## Do not read this when
- feedback 報告ポリシーの利用箇所や、生成されたプロンプト全体を確認したいとき
- prompt builder の他の policy や placeholder 定義だけを調べるとき

## hash
- 5b10c1121b37d308293b3c8bf95cec2858e5601aa01372d585b65ce19f26460a

# `file_access.py`

## Summary
- 各 FileAccessMode に応じた agent 向けファイル読み書き制限文面を構築する関数を定義する。リポジトリ境界、共通禁止領域、oracle/realization file のアクセス制限を組み合わせ、PlaceholderMap と SDHeader として返す。
- ファイルアクセス方針のプロンプト生成ロジックを確認・変更するときの入口であり、実際の oracle/realization の内容や CLI 実装そのものを読むための対象ではない。NO_POLICY では空の方針を返し、不正な mode はエラーとする。

## Read this when
- FileAccessMode ごとの読み書き禁止規則を確認または変更するとき
- agent 向けアクセス制限文面のプレースホルダー展開や SDHeader 生成を調査するとき
- READONLY、PURE_ORACLE_READ、REPO_WRITE、PURE_ORACLE_WRITE、REALIZATION_WRITE、NO_POLICY の挙動差を確認するとき

## Do not read this when
- oracle file や realization file の具体的な仕様・実装内容を確認したいとき
- Codex CLI の sandbox やパス単位のアクセス設定そのものを確認したいとき
- prompt builder の別のプロンプト生成処理だけを調査する場合

## hash
- b7597e2c137cbc131247d061f90f20eecbcffb99b77cacd32cfc86ef6010f917

# `index_entry.py`

## Summary
- 対象ファイルは、INDEX.md 用エントリー生成エージェントに適用するルーティング記述の必須事項と禁止事項を構築する定義を担う。対象を読むべき条件は、INDEX.md エントリーの生成・検討時に、ルーティング情報の責務、入口、適用範囲、境界を確認する必要がある場合である。
- 対象は、同階層の他ファイルではなく、INDEX.md エントリーの内容上の制約や、対象を読むべき・読まなくてよい条件を判断するための入口となる。

## Read this when
- INDEX.md 用エントリーの生成やレビューで、ルーティング情報に何を書くべきかを確認するとき
- 対象の責務、読む条件、対象外の境界、禁止される記述を確認するとき

## Do not read this when
- INDEX.md 用エントリーではなく、通常のプロンプト構築や一般的な構造化文書の実装を確認するとき
- エントリーの具体的な出力内容や対象ファイルの本文説明を直接確認すべきとき

## hash
- fe18d68673ec26573b9d4f319d06722beb70709ad4143a61349f66c56b537a58

# `oracle.py`

## Summary
- `build_oracle_policy` と `build_oracle_investigation_policy` を通じて、oracle file の作成・変更・レビューおよび読み取り専用調査に適用する instruction 文面を構築するモジュール。正本仕様としての oracle file の扱い、判断根拠、優先関係、goal/non-goal、整合性・検索性、未定義事項の扱いを定め、oracle authority policy と investigation policy の入口になる。

## Read this when
- oracle file の作成・変更・レビューに必要な共通規定や、oracle file を読み取り専用で調査する際の必須・禁止事項を確認するとき
- prompt builder の policy 定義から oracle authority または investigation 向けの instruction を構築・変更するとき

## Do not read this when
- realization の配置や CLI 実装の責務境界を確認するときは design_rule を読む
- realization test の要件や実行方法を確認するときは test_rule または test_execution を直接読む
- oracle file の具体的な仕様内容を確認するだけの場合は、対象の個別 oracle file を直接読む

## hash
- b9fa938745555aa7406fe05742e1581dbb548a89a558e8cc1516be7456fe592a

# `oracle_review.py`

## Summary
- oracle review の全段階で共有する、所見の成立条件・重大度判定・採否判断の基準を構築する定義。finding basis policy に基づく根拠提示、明確な仕様矛盾や解消不能な問題の fatal 判定、表記上の問題の minor 判定、および oracle file のみで成立する所見の一貫した扱いを定める。oracle review の所見列挙・統合・擁護／反証・採否判定に関する方針を確認するときの入口となる。

## Read this when
- oracle review の所見や修正対象が成立する条件、fatal／minor の判定基準を確認するとき
- oracle file だけを根拠とする所見の列挙・統合・検証・採否判断の一貫性を確認するとき
- 仕様の明確な矛盾や、実装者の裁量で解消できない問題を重大所見として扱うとき

## Do not read this when
- 具体的な oracle file や realization file の内容自体を確認する必要があるとき
- 所見判定ではなく、プロンプト構築の一般的なプレースホルダー定義や SDHeader の実装を調べるとき

## hash
- 0f8335360a8e2270d28c679d1b4689ff8990a320f4257e111522fd6a1ada9e14

# `realization.py`

## Summary
- realization file の作成・変更・リファクタ・レビュー時に agent call へ適用する規定文面を構築する。oracle を正本として扱い、関連仕様との整合、責務に必要な実装・test・設定・補助ファイルの限定、関連手順の特定と検証を要求する。realization 側の都合による oracle の意味変更や、正本情報・旧仕様・不要な抽象化や識別子の重複を防ぐための入口となる。

## Read this when
- realization file の作成、変更、リファクタ、レビューに関する作業規定を確認するとき
- oracle と realization の責務分担、正本の一元化、実装・test・設定の最小範囲を確認するとき
- realization の変更に伴う関連手順や検証要件を確認するとき

## Do not read this when
- oracle file の意味や仕様そのものを確認することが目的のとき
- realization file を扱わない一般的な prompt builder の実装や質問のとき
- 具体的な realization file の内容や挙動を直接確認すべきとき

## hash
- d27a59209587c3155665d3886050fbfe707597ae31ca42f7c9887577230da120

# `realization_oracle_reference.py`

## Summary
- realization code から対応する oracle file のパスを参照する規定を構築する関数を定義する。
- AgentCallPathContext から root placeholder 定義を取得し、work-root を起点とする PlaceholderMap と、realization code のコメントに oracle file path を記載する SDHeader を返す。

## Read this when
- realization code に対応する oracle file path の参照規定を確認・変更するとき
- prompt builder の policy 用 SDHeader や placeholder map の生成経路を調査するとき

## Do not read this when
- oracle file の具体的な内容や一般的な realization 配置規則だけを確認したいとき
- 対象関数を直接利用する realization code の実装責務を確認したいときは、対応する realization file を先に読むべき場合

## hash
- 1bcfef96f7254e58af1fdef46941debf8f6ed2964d5979b4453bbfbe5a3c113f

# `routing.py`

## Summary
- INDEX.md で作業対象に対応する本文やディレクトリを特定するための routing policy 文面を構築する。
- AgentCallPathContext から call-scoped な root placeholder 定義を取得し、`{{work-root}}` を含む規定文面へ渡す。
- `INDEX.md` の位置づけ、起点の選択、本文優先、本文を根拠とする原則を定義する。

## Read this when
- INDEX.md を使った対象ファイル・ディレクトリの特定規則を確認するとき
- routing policy の文面や、そこへ渡す `{{work-root}}` の解決元を変更・調査するとき

## Do not read this when
- INDEX.md の個別階層における具体的なエントリー内容を確認するとき
- root placeholder の解決ロジック自体を変更・調査するときは、`AgentCallPathContext` やパス解決処理を直接読む場合

## hash
- 55cd76c0dc71c231c2c9f7fb217e2bc7680c3522d0ccb9871c6b464e71e24f47

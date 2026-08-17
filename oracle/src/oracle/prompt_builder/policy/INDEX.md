# `apply_review.py`

## Summary
- oracle file と realization file の適合性を判定する agent 向け policy を構築する。oracle を正本仕様として扱い、明示要求と実装挙動の不整合、または realization 単独で説明できる実行不能・明白な致命的バグを修正対象とする判断の入口となる。

## Read this when
- oracle file に対する realization file の追従要否、所見、修正対象を判断するとき
- oracle と realization の記述・挙動の不整合を、具体的な根拠に基づいて評価するとき

## Do not read this when
- oracle file や realization file を扱わない prompt builder の実装を確認するとき
- 仕様内容そのものを確認するときは、対象となる oracle file または realization file を直接読むとき

## hash
- b680af72b342011132bd2e281e87cf56a364fb956903067574c292924e69a704

# `conflict_resolution.py`

## Summary
- `cmoc session join` で conflict marker を解消する際の、oracle と realization の意味を保つための指示文を構築する。conflict の両側と関連 oracle file の扱い、および意図を両立できない場合の未解消事項としての報告方針を確認する入口である。

## Read this when
- `cmoc session join` の conflict marker 解消規定を確認・変更するとき。
- oracle file と realization file の conflict を、正本仕様の意味を保ちながら解消するとき。
- conflict の両側の意図を両立できず、人間による選択が必要な状態の扱いを確認するとき。

## Do not read this when
- conflict marker の解消を扱わない prompt policy を確認するとき。
- 通常の実装改善、仕様変更、整形、または別 file の変更方針を確認するとき。

## hash
- 3544ddab9ff843f261bec0d73e1b47720cba5c34f244113cea1767190ee55401

# `editor_handoff.py`

## Summary
- agent call から editor work file へ handoff する際の instruction 文面を構築する policy。選択済みの file access mode と Codex CLI sandbox の維持、および正式な成果物の完遂を定める。editor handoff の許容範囲を確認するための入口。

## Read this when
- agent call から editor work file への handoff 規定を確認・変更するとき
- handoff 時の file access mode、Codex CLI sandbox、正式な成果物の扱いを確認するとき
- handoff file への書き込みに必要な sandbox escalation の許容範囲を確認するとき

## Do not read this when
- editor work file 自体の内容や編集処理だけを確認するとき
- agent call と editor handoff の規定に関係しない prompt builder の policy を確認するとき
- handoff を伴わない通常の agent call の挙動を確認するとき

## hash
- 61ab3b9e671fc70075c103b67be68128de111b1a43997e876830afd31e4d93ec

# `feedback_reporting.py`

## Summary
- 対象は、全 agent call に共通する human feedback reporting 規定を構築する実装です。セッション内で解決できなかった問題を `cmoc_feedback.submit_observation` で報告する方針と、報告不要な問題の範囲を扱います。
- 共通 feedback 報告ポリシーの構築・変更を行う際の入口です。個別の agent call の作業内容や feedback 保存処理を調べる場合は、より直接的な対象を参照してください。

## Read this when
- 全 agent call に共通する human feedback 報告規定の構築や変更を行うとき
- セッション内で解決できなかった問題の MCP 報告方針を確認するとき

## Do not read this when
- feedback 報告の対象となる個別問題を解決するとき
- MCP tool `cmoc_feedback.submit_observation` の実装や保存処理を直接調べるとき
- 共通ポリシーではなく、個別のプロンプト生成規定を確認するとき

## hash
- d8ac149202fa51d69bb38b3904a7d0de20575263910f44e0decea344a8ef8aef

# `file_access.py`

## Summary
- cmoc が agent 向けのファイル読み書き制限文面を生成する実装。FileAccessMode とパスコンテキストに応じて、リポジトリ外・保護対象・oracle/realization file などの禁止事項を組み立て、プレースホルダー定義とともに構造化文書として返す。
- ファイルアクセスモードの制約、repo-root と work-root の関係、または agent prompt に埋め込む読み書きポリシーの生成・変更を扱う作業では、この実装を入口として確認する。

## Read this when
- FileAccessMode ごとの読み書き禁止範囲を確認または変更するとき
- agent 向け file R/W policy の文面生成や、repo-root/work-root の扱いを調査するとき
- file access policy の戻り値に含まれるプレースホルダー定義や構造化文書の組み立てを確認するとき

## Do not read this when
- 単に個別の oracle file や realization file の内容・配置を確認するだけで、agent 向けアクセス制限の生成規則を扱わないとき
- 一般的な prompt 構築や FileAccessMode の定義自体を確認する場合は、まずそれぞれの直接の定義元を読むとき

## hash
- 120354ad99996e746db0409ad65f52717156649c2af950b60f1693ced47ae6c6

# `index_entry.py`

## Summary
- INDEX.md 用エントリーを生成する agent 向けのルーティング規定を定義する。
- 対象を読むべき作業・質問・変更の条件、対象の責務、同階層の他対象ではなく対象へ進む理由を示す。
- 対象本文に根拠のある責務・入口・適用条件だけを扱い、対象外の責務や過度な詳細説明を INDEX.md に持ち込まないための境界を定める。

## Read this when
- INDEX.md 用エントリーの生成規定を作成・変更するとき
- INDEX.md エントリーに記載する責務、入口、適用条件、対象範囲の境界を判断するとき

## Do not read this when
- INDEX.md エントリーではなく、通常のプロンプト構築処理を実装・変更するとき
- Structured Output schema の出力項目や形式だけを確認するとき
- 対象本文に基づくルーティング情報が不要な作業を行うとき

## hash
- cc9b19f5748e52763c317399e54b2e1aa21733a102eb0f1ef102ffe407f1538e

# `oracle.py`

## Summary
- oracle file を作成・変更・レビューする agent call に適用する正本仕様の構築定義。oracle authority policy と、oracle file の読み取り専用調査 policy を提供し、判断根拠、優先関係、仕様上の境界、禁止事項、許容される補完範囲を定める。oracle 関連の動的 instruction 文面や、その調査規約を確認・変更する際の入口となる。

## Read this when
- oracle file または realization file を扱う agent call の instruction policy を確認・変更するとき。
- oracle authority policy における正本仕様の扱い、判断根拠、goal/non-goal、既存仕様維持、仕様間の優先関係を確認するとき。
- oracle file の読み取り専用調査で、定義済み事項と未定義事項の区別や、実装から仕様を逆算しない制約を確認するとき。

## Do not read this when
- oracle 関連 policy 自体ではなく、個別 oracle file の内容や realization 実装の配置・挙動だけを調べるときは、対象の oracle file または設計規約を直接読む。
- 一般的な agent call の構築定義や oracle と無関係な policy を扱うとき。

## hash
- 90b706867f8a69321c8bfcf1c909e0195dce765c30e5759cd28b905fa1724084

# `oracle_review.py`

## Summary
- oracle review の全段階で共有する所見判定規定を構築する。所見・修正対象に必要な根拠、fatal と minor の成立条件、oracle file 単独で成立する所見の判定条件を定める。
- oracle review の所見を列挙・統合・検証・採否判定するときに参照する共通ポリシーとして機能する。

## Read this when
- oracle review の所見または修正対象が成立する条件を確認するとき
- fatal・minor の判定基準を確認するとき
- oracle file だけを根拠にした所見の扱いを確認するとき

## Do not read this when
- 個別の oracle file や realization file の内容自体を確認するとき
- oracle review policy をプロンプトへ組み込む実装詳細だけを確認するとき

## hash
- 15b4226ea6b4947e0d7448afac0ee7e81aea17e42d5a03ba4a61b396df8f408d

# `realization.py`

## Summary
- realization file の作成・変更・リファクタ・レビュー時に適用する instruction 文面を構築する。oracle を人間所有の正本仕様として扱い、関連 oracle の確認、正本の一元化、必要最小限の実装・test・設定・ancillary、責務境界の整理、関連手順と検証環境の確認を要求する。禁止事項として、realization 都合による oracle 意味の変更、正本定義の複製、旧実装や不要物の温存、根拠のない拡張、必要な意味や検証の損失、手順配置先の限定を定める。

## Read this when
- realization file を作成・変更・リファクタ・レビューするとき
- oracle と realization の責務分担、正本の一元化、不要な実装や依存の追加禁止を確認するとき
- realization の変更に必要な repository 固有手順や検証環境を判断するとき

## Do not read this when
- realization file の具体的な実装内容や prompt builder の API を確認したいときは、対象実装や関連する oracle file を直接読む
- realization file 以外の agent call 向け policy を確認・変更するときは、対応する policy 定義へ進む

## hash
- a66c22292aac02513a5eaf46359a6ea676df855fc533b98bdd9abe9e00178878

# `realization_oracle_reference.py`

## Summary
- realization code から、対応する oracle file の参照規則を構築するポリシー定義。realization code の作成・変更時に適用され、対応する oracle file が存在する場合のコメント記載ルールを確認する入口となる。

## Read this when
- realization code の作成または変更にあたり、oracle file path をコメントへ記載する規則を確認するとき。
- realization code と oracle file の対応付けに関する prompt policy を変更・調査するとき。

## Do not read this when
- realization code 自体の実装責務や配置を確認したいとき。
- oracle file の本文や、個別の realization code の動作仕様を直接確認するとき。

## hash
- a72583769048b759b2d53f7ca62ecd97cffc25515bb5b1f3f72c1afd4b2bf1c3

# `routing.py`

## Summary
- 作業対象に応じた INDEX.md の起点と読み方を示す routing policy の文面を構築する。call-scoped context から work-root を取得し、対象に近い階層を優先しつつ領域不明時はリポジトリルートを入口とする。INDEX.md は対象特定の補助として使い、本文を最終的な根拠とする。

## Read this when
- INDEX.md を起点に、作業対象のファイルやディレクトリを特定する必要があるとき
- INDEX.md と本文の記述が異なる場合の優先順位や、対象領域不明時の探索起点を確認するとき

## Do not read this when
- 特定済みの対象本文だけを直接確認すれば足りるとき
- routing policy ではなく、個別の prompt builder 実装やデータ型の仕様を確認するとき

## hash
- b22fd2e2601d1df96a5b9a0cdc20723a1bb929d3a8b2a21bdd439c79dd004263

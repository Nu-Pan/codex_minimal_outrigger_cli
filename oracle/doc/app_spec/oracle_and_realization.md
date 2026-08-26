# oracle file と realization file の責務

oracle file は、人間が所有して全責任を負う正本仕様断片とする。agent は oracle file の作成、変更、調査、およびレビューを補助してよいが、realization file から正本仕様を逆算してはならない。

## oracle doc と oracle src の正本責務

oracle file の下位概念は、正本として所有する事項で区別する。

- oracle doc は `{{work-root}}/oracle/doc` に置く。cmoc の要求、責務、判断基準、goal、non-goal、および意味上の優先関係を定義する意味仕様を所有する。
- oracle src は `{{work-root}}/oracle/src` に置く。oracle doc から明示的に委譲された正確な algorithm、builder の選択値、prompt の構築順序・文面・rendering、および schema を所有する。
- oracle test は `{{work-root}}/oracle/test` に置き、プログラミング言語で正本仕様を検査する。

明示的に委譲された prompt literal の正確な文面は oracle src が所有し、その文面が表す意味仕様は oracle doc が所有する。builder が生成した prompt（generated prompt）は実行時生成物であり、意味仕様または prompt 文面の正本ではない。

本書と関連する分類仕様を agent 向けに表現する文面と構造は、次の oracle src へ委譲する。

| 意味仕様 | 委譲先 |
|---|---|
| oracle file、realization file、および uncategorised file の役割と分類。本書と `oracle/doc/app_spec/oracle_and_realization_file_enumeration.md:3` の「分類結果」を正本とする | `oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py:7` の `build_oracle_and_realization_basic` |
| oracle file を扱う判断基準 | `oracle/src/oracle/prompt_builder/policy/oracle.py:7` の `build_oracle_policy` |
| realization file を扱う判断基準 | `oracle/src/oracle/prompt_builder/policy/realization.py:8` の `build_realization_policy` |
| oracle file に対する realization file の適合性 | `oracle/src/oracle/prompt_builder/policy/realization_findings.py:7` の `build_realization_findings_policy` |

prompt literal に固有の役割、制限、および call 固有の実行時指示の優先関係は、`oracle/doc/app_spec/codex_exec_rule.md:172` の「prompt literal の役割と制限」以降を参照する。

## 正本責務の重複禁止

同じ仕様事項の正本所有者は一つだけとする。この重複禁止は正本責務を対象とし、同じ文字列が複数箇所に現れること自体を禁止しない。

- oracle doc は、oracle src が所有する exact literal、schema、構築方法、または選択値を言い換えて再定義しない。
- oracle src は、oracle doc が所有する意味仕様を独立した正本として補完、変更、または拡張しない。
- prompt literal は、oracle doc が所有する規則を受信 agent 向けに必要最小限で再表現してよい。この再表現は第二の正本とせず、その変更で意味仕様が変わる場合は対応する oracle doc も変更する。

## oracle doc から oracle src への委譲

oracle doc は、正確な詳細の正本責務を oracle src へ明示的に委譲してよい。委譲する oracle doc は、参照先が所有する範囲を限定し、次の参照情報を示す。

- repository-relative path
- 現在の行番号
- 関数、class、定数、または JSON Pointer などの安定した locator
- 参照先が正本として所有する内容の短い説明

行番号は移動の補助情報とし、参照対象は安定した locator でも特定できるようにする。委譲する oracle doc は、参照先が所有する詳細を本文へ複製しない。

正本関係を相互に追跡する必要がある場合は、Codex へ注入されない oracle src の docstring、comment、または参照 metadata に、意味仕様を所有する oracle doc の repository-relative path と見出しを記載してよい。この記載によって、注入される literal または rendering 結果を変更してはならない。

## 正本責務に基づく優先関係

oracle doc と oracle src の優先関係は、ファイル種別の一律な上下関係ではなく、対象事項の正本責務に基づいて判断する。

- 意味仕様については、その事項を所有する oracle doc を優先する。oracle src の記述が詳細、実行可能、または Codex へ注入されることだけでは、この正本責務と優先関係は変わらない。
- oracle doc が明示的に委譲した正確な表現、構築、選択値、および schema については、参照先の oracle src を優先する。
- 同じ意味仕様について oracle doc と oracle src が食い違う場合は、詳細な記述を選んで解決してはならない。oracle file 間の不整合として扱う。
- generated prompt は、oracle doc または oracle src の正本を上書きしない。

realization file は、oracle file に記述された人間意図を具体化する成果物とする。realization file は AI が編集し、正本仕様を述べる場所にしてはならない。

realization file の下位概念は、次の責務で区別する。

- realization implementation は `{{work-root}}/src` に置き、product の実装と挙動を記述する設定を含む。
- realization test は `{{work-root}}/test` に置き、realization code の外部挙動または制御ロジックを検査する。
- realization ancillary は、実装と test 以外の補助的な realization file とする。

## oracle file を扱う判断基準

- 判断の根拠は、関連する oracle file に置く。cmoc 固有契約または oracle file と installed skill が競合する場合は、前者を優先する。
- 合わせて読む必要がある oracle file は、path、現在の行番号、および参照先の簡潔な内容で特定する。
- installed skill の存在または一般的なベストプラクティスだけを、oracle file の意味または作業完了条件の根拠にしてはならない。
- 実装差を許容しない事項と、人間が判断すべき境界を明示する。仕様の隙間を網羅的に埋めるためだけの分類、列挙、または新規 oracle file を追加してはならない。
- 正本仕様断片には未定義部分を残してよい。明示仕様の隙間は、関連する oracle file と、アクセス可能な場合の既存実装および test から自然に導ける小さな範囲で実装者が補ってよい。過剰な実装を誘発し得る境界では、goal と non-goal を読み取れるようにする。
- realization file の都合、過去の実装、または偶然の挙動だけから正本仕様を導いてはならない。実装上の制約は、仕様の矛盾または実現不能を調べる材料に限って使用してよい。
- 関連する正本仕様断片の整合性と、一般方針と個別仕様の優先関係を保つ。依頼の対象外である既存仕様の意味を維持する。
- 同じ概念の用語と表記を統一し、名前と定義を一致させる。文意または検索性を損なう誤字、脱字、文法誤り、および同じ意味の重複を残してはならない。

## realization file を扱う判断基準

- 「oracle file と realization file の責務」に基づき、関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする。
- oracle src の定義または prompt 文面を realization file へ正本のように複製しない。同じ情報が必要な場合は、参照、生成、または意味を変えない変換によって正本を一箇所に保つ。
- 現行仕様に必要な implementation、test、設定、および ancillary だけを保つ。旧仕様の分岐、同じ責務の重複、および将来使う可能性だけを根拠とするものを含む、根拠のない公開面や抽象化を追加しない。
- 新しい実装は実在する責務境界または重複に対応させ、既存の近い責務を同時に整理する。簡潔化によって意味、可読性、失敗時挙動、または必要な検証を損なわない。
- 対象 repository が追跡する手順を配置場所にかかわらず特定し、必要な検証を行う。手順または実行環境が利用できない範囲を検証済みとして扱わない。

## oracle file に対する realization file の適合性

realization apply と realization refactor は、oracle file への適合を回復する追従作業であり、一般的な品質改善の列挙を目的としない。追従要否と所見は、次の基準で判断する。

- oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は、修正対象とする。
- realization file だけから説明できる実行不能または明白な致命的バグは、修正対象とする。
- 修正対象は、根拠となる oracle file と realization file、または致命的な実装箇所を特定できなければならない。
- oracle file に記述がないこと、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に修正対象を作らない。
- 調査開始時点ですでに解消されている問題を所見として扱わない。
- 修正後も関連する oracle file の明示要求を満たし、realization file の既存挙動を正本仕様へ逆流させない。

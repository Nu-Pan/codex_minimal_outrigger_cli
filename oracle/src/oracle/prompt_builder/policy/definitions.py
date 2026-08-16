"""全用途の Policy 文面を一箇所で管理する定義。"""

from .basic import Policy

ORACLE_AUTHORITY_POLICY = Policy(
    policy_id="oracle_authority.10.authority",
    title="oracle file を正本仕様断片として扱う",
    required=("oracle file を人間が所有する正本仕様断片として扱う",),
)

ORACLE_AUTHORITY_NO_REVERSE_FLOW_POLICY = Policy(
    policy_id="oracle_authority.20.no_reverse_flow",
    title="realization file から oracle file へ意味を逆流させない",
    prohibited=(
        "realization file の都合または挙動を根拠に oracle file の意味を変更してはいけない",
    ),
)

ORACLE_AUTHORITATIVE_BASIS_POLICY = Policy(
    policy_id="oracle.10.authoritative_basis",
    title="判断根拠と installed skill の優先関係を守る",
    required=(
        "判断の根拠を関連する oracle file に置く",
        "cmoc 固有契約または oracle file と installed skill が競合する場合は前者を優先する",
    ),
    prohibited=(
        "installed skill の存在を oracle file の意味または作業完了条件の前提にしてはいけない",
    ),
)

ORACLE_EDIT_AUTHORITATIVE_BASIS_POLICY = Policy(
    policy_id="oracle.15.edit_authoritative_basis",
    title="一般論だけを根拠に oracle file の要求を変更しない",
    prohibited=(
        "一般的なベストプラクティスだけを根拠に oracle file の要求を変更してはいけない",
    ),
)

ORACLE_INTENT_AND_GAPS_POLICY = Policy(
    policy_id="oracle.20.intent_and_gaps",
    title="重要な人間意図へ絞り、仕様の隙間を許容する",
    required=(
        "実装差を許容しない事項と、人間が判断した事項は、境界として明示する",
        "過剰な実装を誘発し得る境界では goal と non-goal を読み取れるようにする",
    ),
    prohibited=(
        "仕様全体を網羅するためだけの分類、列挙、説明を追加してはいけない",
        "未定義部分を埋めることだけを目的に oracle file を増やしてはいけない",
    ),
    permitted=(
        "明示仕様の隙間は、現行の oracle file と、file access が許す場合の既存実装・既存 test から自然に導ける範囲で実装者が補ってよい",
    ),
)

ORACLE_NO_REVERSE_ENGINEERING_POLICY = Policy(
    policy_id="oracle.30.no_reverse_engineering",
    title="実装から正本仕様を逆算しない",
    prohibited=("realization file または実装だけから正本仕様を逆算してはいけない",),
)

ORACLE_IMPLEMENTATION_CONSTRAINT_POLICY = Policy(
    policy_id="oracle.35.implementation_constraint",
    title="実装上の制約は仕様の矛盾または実現不能の調査に限って使用する",
    permitted=(
        "正本仕様の矛盾または実現不能を調べる場合に限り、実装上の制約を修正提案の材料にしてよい",
    ),
)

ORACLE_DEFINED_AND_UNDEFINED_POLICY = Policy(
    policy_id="oracle_investigation.40.defined_and_undefined",
    title="定義済みの事項と未定義の事項を区別する",
    required=("oracle file で定義されている事項と未定義の事項を区別する",),
    prohibited=("未定義の事項を正本仕様として断定してはいけない",),
)

ORACLE_CONSISTENCY_AND_SEARCHABILITY_POLICY = Policy(
    policy_id="oracle.40.consistency_and_searchability",
    title="正本仕様断片の整合性と検索性を保つ",
    required=(
        "一般方針と個別仕様の優先関係を読み取れるようにする",
        "依頼の対象外である既存仕様の意味を維持する",
        "oracle file を作成または変更する場合は、同じ概念の用語と表記を統一し、名前から推測される意味を定義と一致させる",
        "oracle file を作成または変更する場合は、文意または検索性を損なう誤字、脱字、文法誤りを残さない",
    ),
    prohibited=(
        "一方の正本仕様断片に従うと別の正本仕様断片へ必ず違反する状態を作ってはいけない",
        "oracle file を作成または変更する場合は、同じ意味の記述を複数箇所へ重複させてはいけない",
    ),
)

REALIZATION_ORACLE_CONFORMANCE_POLICY = Policy(
    policy_id="realization.10.oracle_conformance",
    title="realization file を現行の oracle file に適合させる",
    required=(
        "関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする",
        "正本と同じ情報が必要な場合は、参照、生成、または変換により正本を一箇所に保つ",
    ),
    prohibited=(
        "oracle src の定義または prompt 文面を realization file へ正本のように複製してはいけない",
    ),
)

REALIZATION_CURRENT_SPEC_ONLY_POLICY = Policy(
    policy_id="realization.20.current_spec_only",
    title="現行仕様に必要な実装だけを保つ",
    required=(
        "現行仕様を満たすために必要な implementation、test、設定、および ancillary だけを保つ",
        "新しい実装は実在する責務境界または重複に対応させ、既存の近い責務を同時に整理する",
    ),
    prohibited=(
        "同じ責務の実装、旧仕様の分岐、未使用の識別子、または置換済みの test を残してはいけない",
        "将来使う可能性だけを根拠に抽象化、公開 interface、設定、永続状態、依存関係、または補助 file を追加してはいけない",
        "簡潔化のために意味、可読性、失敗時挙動、または必要な検証を損なってはいけない",
    ),
)

REALIZATION_REPOSITORY_VERIFICATION_POLICY = Policy(
    policy_id="realization.30.repository_verification",
    title="対象 repository 固有の手順で変更を検証する",
    required=(
        "対象 repository で追跡されている関連手順を配置場所にかかわらず特定し、変更に必要な検証を行う",
        "必要な手順または実行環境が利用できない場合は、検証済みと扱わず不足を報告する",
    ),
    prohibited=("work-root 固有手順の配置先を `.agents/skills` に限定してはいけない",),
)

FINDING_BASIS_EVIDENCE_POLICY = Policy(
    policy_id="finding_basis.10.evidence",
    title="所見・修正対象に具体的な根拠を求める",
    required=(
        "所見または修正対象には、用途固有の policy が認める具体的な oracle file または realization file の記述・挙動を示す",
    ),
    prohibited=(
        "oracle file に記述がないこと、仕様の隙間、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に所見または修正対象を作ってはいけない",
    ),
)

APPLY_REVIEW_FIX_TARGETS_POLICY = Policy(
    policy_id="apply_review.10.fix_targets",
    title="明確な不適合または致命的な実装問題を修正対象にする",
    required=(
        "oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は修正対象とする",
        "realization file だけから実行不能または明白な致命的バグと説明できる場合は修正対象とする",
        "修正後の realization file も関連する oracle file の明示要求を満たす",
    ),
)

APPLY_REVIEW_ALREADY_RESOLVED_POLICY = Policy(
    policy_id="apply_review.20.already_resolved",
    title="調査開始時点で解消済みの問題を所見にしない",
    prohibited=("調査開始時点ですでに解消されている問題を所見として扱ってはいけない",),
)

ORACLE_REVIEW_FATAL_POLICY = Policy(
    policy_id="oracle_review.10.fatal",
    title="実装者の裁量で解消不能な問題だけを fatal 所見にする",
    required=(
        "正本仕様断片同士に解釈の余地がない明確な矛盾がある場合は fatal とする",
        "仕様に従うと実装者の裁量では解消不能な問題が必ず発生する場合は fatal とする",
        "fatal は、両立する妥当な実装方針が残っていないことを具体的な記述から説明する",
    ),
)

ORACLE_REVIEW_MINOR_POLICY = Policy(
    policy_id="oracle_review.20.minor",
    title="文意または検索性を損なう表記上の誤りだけを minor 所見にする",
    required=(
        "文意または検索性を損なう誤字、脱字、明確な文法誤り、用語不統一、または表記揺れは minor とする",
        "minor は正本仕様の意味を変更しない表記上の修正として説明できなければならない",
    ),
    prohibited=(
        "文法的に正しく検索性も損なわない言い回しを、好みだけで minor にしてはいけない",
    ),
)

ORACLE_REVIEW_ORACLE_ONLY_POLICY = Policy(
    policy_id="oracle_review.30.oracle_only",
    title="oracle file だけから成立する問題を所見にする",
    required=(
        "所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定で同じ成立条件を使用する",
    ),
    prohibited=(
        "realization file、外部事情、または未確認の可能性を追加しなければ成立しない事項を所見にしてはいけない",
    ),
)

CONFLICT_RESOLUTION_PRESERVE_BOTH_BRANCHES_POLICY = Policy(
    policy_id="conflict_resolution.10.preserve_both_branches",
    title="両 branch の意味を保って conflict marker だけを解消する",
    required=(
        "conflict 対象の両側と関連する oracle file を読み、両立する意図と挙動を失わない解消結果にする",
        "両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する",
    ),
    prohibited=(
        "conflict marker の解消に不要な仕様変更、実装改善、整形、または別 file の変更を行ってはいけない",
    ),
)

EDITOR_HANDOFF_PRESERVE_RESULT_POLICY = Policy(
    policy_id="editor_handoff.10.preserve_result",
    title="editor handoff でも agent call の責務を維持する",
    required=(
        "agent call に選択された file access mode と Codex CLI sandbox を維持する",
        "handoff file への書き込みとは別に、その agent call が要求する正式な結果または成果物を満たす",
    ),
    permitted=(
        "handoff file への書き込みに必要な command だけについて、対象 path と理由を限定した sandbox escalation を要求してよい",
    ),
)

INDEX_ENTRY_ROUTING_POLICY = Policy(
    policy_id="index_entry.10.routing",
    title="INDEX.md エントリーは読むべき対象へのルーティング情報である",
    required=(
        "対象を読むべき作業・質問・変更の条件を判断できる意味情報を書く",
        "対象が担う責務と、同階層の他対象ではなくその対象へ進む理由を書く",
    ),
    prohibited=(
        "対象本文を読まなければ理解できない詳細説明を INDEX.md エントリーに展開してはいけない",
        "関連しそうという理由だけで対象へ進ませるような広すぎる条件を書いてはいけない",
    ),
)

INDEX_ENTRY_EVIDENCE_POLICY = Policy(
    policy_id="index_entry.20.evidence",
    title="INDEX.md エントリーは対象内容に根拠を持つ",
    required=(
        "対象内容から根拠を持って言える責務・入口・読む条件だけを書く",
        "対象を読まなくてよい境界や、より直接読むべき別対象がある場合の境界を書く",
    ),
    prohibited=("推測で対象外の責務や将来の用途を広げてはいけない",),
)

INDEX_ENTRY_SEMANTIC_INFORMATION_POLICY = Policy(
    policy_id="index_entry.30.semantic_information",
    title="機械的に補える情報を INDEX.md エントリーの意味情報に混ぜない",
    required=(
        "機械的な識別情報ではなく、対象を読むべきか判断するための意味情報だけを書く",
    ),
    prohibited=(
        "ファイル名・ディレクトリ名・ハッシュ値のような機械的に補える情報を書いてはいけない",
        "Structured Output schema を読めば分かる出力項目名・型・形式を説明してはいけない",
    ),
)

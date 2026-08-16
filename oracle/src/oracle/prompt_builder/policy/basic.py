from dataclasses import dataclass

from oracle.other.struct_doc import StructDoc


@dataclass(frozen=True)
class Policy:
    """agent 向け instruction の一つの規定を表す immutable な値。"""

    # ID は合成時の同一性検査だけに使い、prompt へは出力しない。
    policy_id: str
    title: str
    required: tuple[str, ...] = ()
    prohibited: tuple[str, ...] = ()
    recommended: tuple[str, ...] = ()
    permitted: tuple[str, ...] = ()
    # requirements だけでは判断できない場合に限り、判断例を持たせる。
    examples: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """文字列群を tuple に固定し、値の入れ子まで immutable にする。"""
        if not self.policy_id or not self.title:
            raise ValueError("Policy ID and title must not be empty")
        for field_name in (
            "required",
            "prohibited",
            "recommended",
            "permitted",
            "examples",
        ):
            object.__setattr__(
                self,
                field_name,
                _as_text_tuple(field_name, getattr(self, field_name)),
            )
        if not any((self.required, self.prohibited, self.recommended, self.permitted)):
            raise ValueError("Policy must contain at least one requirement")


@dataclass(frozen=True)
class PolicyGroup:
    """同じ適用範囲を持つ複数の Policy をまとめる immutable な値。"""

    # group ID も合成と順序付けだけに使い、prompt へは出力しない。
    group_id: str
    title: str
    scope: str
    policies: tuple[Policy, ...]

    def __post_init__(self) -> None:
        """group 自身と保持する Policy を検証する。"""
        if not self.group_id or not self.title or not self.scope:
            raise ValueError("PolicyGroup ID, title, and scope must not be empty")
        policies = tuple(self.policies)
        if not policies or not all(isinstance(policy, Policy) for policy in policies):
            raise ValueError("PolicyGroup must contain Policy values")
        object.__setattr__(self, "policies", policies)


@dataclass(frozen=True)
class PolicyCollection:
    """合成および render の単位となる PolicyGroup の集合。"""

    groups: tuple[PolicyGroup, ...] = ()

    def __post_init__(self) -> None:
        """保持する group を immutable な tuple に固定する。"""
        groups = tuple(self.groups)
        if not all(isinstance(group, PolicyGroup) for group in groups):
            raise ValueError("PolicyCollection must contain PolicyGroup values")
        object.__setattr__(self, "groups", groups)


def combine_policy_collections(
    *collections: PolicyCollection,
) -> PolicyCollection:
    """Policy ID の衝突を検査し、選択順に依存しない集合へ合成する。"""
    # ID ごとの定義と、重複 Policy を置く決定的な group を集める。
    group_definitions: dict[str, tuple[str, str]] = {}
    policy_definitions: dict[str, Policy] = {}
    owner_group_ids: dict[str, str] = {}
    for collection in collections:
        for group in collection.groups:
            group_definition = (group.title, group.scope)
            if (
                group.group_id in group_definitions
                and group_definitions[group.group_id] != group_definition
            ):
                raise ValueError(
                    f"Conflicting PolicyGroup definition (group_id={group.group_id!r})"
                )
            group_definitions[group.group_id] = group_definition

            for policy in group.policies:
                current = policy_definitions.get(policy.policy_id)
                if current is not None and current != policy:
                    raise ValueError(
                        "Conflicting Policy definition "
                        f"(policy_id={policy.policy_id!r})"
                    )
                policy_definitions[policy.policy_id] = policy
                owner_group_ids[policy.policy_id] = min(
                    owner_group_ids.get(policy.policy_id, group.group_id),
                    group.group_id,
                )

    # group と Policy の ID で並べ、builder の選択順から出力順を切り離す。
    policies_by_group: dict[str, list[Policy]] = {}
    for policy_id, policy in policy_definitions.items():
        policies_by_group.setdefault(owner_group_ids[policy_id], []).append(policy)
    return PolicyCollection(
        tuple(
            PolicyGroup(
                group_id,
                *group_definitions[group_id],
                tuple(
                    sorted(
                        policies_by_group[group_id],
                        key=lambda policy: policy.policy_id,
                    )
                ),
            )
            for group_id in sorted(policies_by_group)
        )
    )


def policy_collection_to_struct_docs(
    collection: PolicyCollection,
) -> list[StructDoc]:
    """合成済み collection を agent 向け instruction 文面へ変換する。"""
    # 適用範囲は独立した定型節にせず、各 group の見出しへ統合する。
    documents = []
    for group in collection.groups:
        policies = [(policy, _policy_body(policy)) for policy in group.policies]
        if len(policies) == 1:
            policy, body = policies[0]
            documents.append(StructDoc(f"{policy.title}（{group.scope}）", body))
        else:
            documents.append(
                StructDoc(
                    f"{group.title}（{group.scope}）",
                    *(StructDoc(policy.title, body) for policy, body in policies),
                )
            )
    return documents


def _policy_body(policy: Policy) -> str:
    """label ごとの要求文群と、必要な場合だけ判断例を構築する。"""
    # label の順序を固定し、空の文群は label ごと出力しない。
    fields: list[str] = []
    for label, requirements in (
        ("必須", policy.required),
        ("禁止", policy.prohibited),
        ("推奨", policy.recommended),
        ("許容", policy.permitted),
    ):
        if requirements:
            fields.append(
                f"**{label}**\n\n" + "\n".join(f"- {body}" for body in requirements)
            )
    if policy.examples:
        fields.append(
            "**判断例**\n\n" + "\n".join(f"- {example}" for example in policy.examples)
        )
    return "\n\n".join(fields)


def _as_text_tuple(field_name: str, values: tuple[str, ...]) -> tuple[str, ...]:
    """要求文群を immutable にし、空または文字列以外の要素を拒否する。"""
    result = tuple(values)
    if not all(isinstance(value, str) and value for value in result):
        raise ValueError(f"Policy.{field_name} must contain non-empty strings")
    return result

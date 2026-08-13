from dataclasses import dataclass

from oracle.other.struct_doc import StructDoc


@dataclass(frozen=True)
class Standard:
    """agent 向け instruction の一つの規範を表す immutable な値。"""

    # ID は合成時の同一性検査だけに使い、prompt へは出力しない。
    standard_id: str
    title: str
    required: tuple[str, ...] = ()
    prohibited: tuple[str, ...] = ()
    recommended: tuple[str, ...] = ()
    permitted: tuple[str, ...] = ()
    # requirements だけでは判断できない場合に限り、判断例を持たせる。
    examples: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """文字列群を tuple に固定し、値の入れ子まで immutable にする。"""
        if not self.standard_id or not self.title:
            raise ValueError("Standard ID and title must not be empty")
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
            raise ValueError("Standard must contain at least one requirement")


@dataclass(frozen=True)
class StandardGroup:
    """同じ適用範囲を持つ複数の Standard をまとめる immutable な値。"""

    # group ID も合成と順序付けだけに使い、prompt へは出力しない。
    group_id: str
    title: str
    scope: str
    standards: tuple[Standard, ...]

    def __post_init__(self) -> None:
        """group 自身と保持する Standard を検証する。"""
        if not self.group_id or not self.title or not self.scope:
            raise ValueError("StandardGroup ID, title, and scope must not be empty")
        standards = tuple(self.standards)
        if not standards or not all(
            isinstance(standard, Standard) for standard in standards
        ):
            raise ValueError("StandardGroup must contain Standard values")
        object.__setattr__(self, "standards", standards)


@dataclass(frozen=True)
class StandardCollection:
    """合成および render の単位となる StandardGroup の集合。"""

    groups: tuple[StandardGroup, ...] = ()

    def __post_init__(self) -> None:
        """保持する group を immutable な tuple に固定する。"""
        groups = tuple(self.groups)
        if not all(isinstance(group, StandardGroup) for group in groups):
            raise ValueError("StandardCollection must contain StandardGroup values")
        object.__setattr__(self, "groups", groups)


def combine_standard_collections(
    *collections: StandardCollection,
) -> StandardCollection:
    """Standard ID の衝突を検査し、選択順に依存しない集合へ合成する。"""
    # ID ごとの定義と、重複 Standard を置く決定的な group を集める。
    group_definitions: dict[str, tuple[str, str]] = {}
    standard_definitions: dict[str, Standard] = {}
    owner_group_ids: dict[str, str] = {}
    for collection in collections:
        for group in collection.groups:
            group_definition = (group.title, group.scope)
            if (
                group.group_id in group_definitions
                and group_definitions[group.group_id] != group_definition
            ):
                raise ValueError(
                    "Conflicting StandardGroup definition "
                    f"(group_id={group.group_id!r})"
                )
            group_definitions[group.group_id] = group_definition

            for standard in group.standards:
                current = standard_definitions.get(standard.standard_id)
                if current is not None and current != standard:
                    raise ValueError(
                        "Conflicting Standard definition "
                        f"(standard_id={standard.standard_id!r})"
                    )
                standard_definitions[standard.standard_id] = standard
                owner_group_ids[standard.standard_id] = min(
                    owner_group_ids.get(standard.standard_id, group.group_id),
                    group.group_id,
                )

    # group と Standard の ID で並べ、builder の選択順から出力順を切り離す。
    standards_by_group: dict[str, list[Standard]] = {}
    for standard_id, standard in standard_definitions.items():
        standards_by_group.setdefault(owner_group_ids[standard_id], []).append(standard)
    return StandardCollection(
        tuple(
            StandardGroup(
                group_id,
                *group_definitions[group_id],
                tuple(
                    sorted(
                        standards_by_group[group_id],
                        key=lambda standard: standard.standard_id,
                    )
                ),
            )
            for group_id in sorted(standards_by_group)
        )
    )


def standard_collection_to_struct_docs(
    collection: StandardCollection,
) -> list[StructDoc]:
    """合成済み collection を agent 向け instruction 文面へ変換する。"""
    # 適用範囲は独立した定型節にせず、各 group の見出しへ統合する。
    documents = []
    for group in collection.groups:
        standards = [
            (standard, _standard_body(standard)) for standard in group.standards
        ]
        if len(standards) == 1:
            standard, body = standards[0]
            documents.append(StructDoc(f"{standard.title}（{group.scope}）", body))
        else:
            documents.append(
                StructDoc(
                    f"{group.title}（{group.scope}）",
                    *(StructDoc(standard.title, body) for standard, body in standards),
                )
            )
    return documents


def _standard_body(standard: Standard) -> str:
    """label ごとの要求文群と、必要な場合だけ判断例を構築する。"""
    # label の順序を固定し、空の文群は label ごと出力しない。
    fields: list[str] = []
    for label, requirements in (
        ("必須", standard.required),
        ("禁止", standard.prohibited),
        ("推奨", standard.recommended),
        ("許容", standard.permitted),
    ):
        if requirements:
            fields.append(
                f"**{label}**\n\n" + "\n".join(f"- {body}" for body in requirements)
            )
    if standard.examples:
        fields.append(
            "**判断例**\n\n"
            + "\n".join(f"- {example}" for example in standard.examples)
        )
    return "\n\n".join(fields)


def _as_text_tuple(field_name: str, values: tuple[str, ...]) -> tuple[str, ...]:
    """要求文群を immutable にし、空または文字列以外の要素を拒否する。"""
    result = tuple(values)
    if not all(isinstance(value, str) and value for value in result):
        raise ValueError(f"Standard.{field_name} must contain non-empty strings")
    return result

from sub_commands.oracle.review import cmoc_oracle_review_impl


def cmoc_eval_oracle_impl(scope: str) -> None:
    """want を書き出した oracle を oracle review と同じ評価経路へ渡す。"""
    # {{work-root}}/oracle/doc/considered_alternative/working_plan_review.md
    cmoc_oracle_review_impl(scope)

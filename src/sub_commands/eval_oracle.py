from sub_commands.review.oracle import cmoc_review_oracle_impl


def cmoc_eval_oracle_impl(scope: str) -> None:
    """want を書き出した oracle を review oracle と同じ評価経路へ渡す。"""
    # <work-root>/oracle/doc/considered_alternative/working_plan_review.md
    cmoc_review_oracle_impl(scope)

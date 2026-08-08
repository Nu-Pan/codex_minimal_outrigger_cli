"""実経路統合テストの subprocess にだけモデル設定の例外を適用する。"""

from functools import wraps

from basic.acp import AgentCallParameter, ModelClass, ReasoningEffort

# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# この directory を明示的に PYTHONPATH へ加えた実経路統合 subprocess だけで、
# builder が構築した parameter のモデル設定をテスト専用値へ置き換える。
_original_init = AgentCallParameter.__init__


@wraps(_original_init)
def _init_with_real_path_model_settings(
    self: AgentCallParameter, *args: object, **kwargs: object
) -> None:
    _original_init(self, *args, **kwargs)
    object.__setattr__(self, "model_class", ModelClass.MINIMUM)
    object.__setattr__(self, "reasoning_effort", ReasoningEffort.LOW)


AgentCallParameter.__init__ = _init_with_real_path_model_settings  # type: ignore[method-assign]

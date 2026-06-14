from utils.struct_docs import StructDocs
from agent_call_parameters.standards.base import Standard


def build_oracles_standards() -> StructDocs:
    """
    oracles files のレビュー観点を表す StructDocs を構築する。
    """
    #
    Standards = [Standard()]

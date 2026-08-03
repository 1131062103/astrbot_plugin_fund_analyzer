"""
模型路由工具
根据插件配置（ai_model）决定各分析模块调用 LLM 时使用的模型。
未配置或配置无效时返回 None，表示使用 AstrBot 当前默认模型。
"""

from astrbot.api import logger

# 按 provider 缓存其支持模型列表，避免每次调用都拉取
_supported_cache: dict[str, set[str]] = {}


def _provider_id(provider) -> str:
    """生成 provider 的唯一标识"""
    try:
        meta = provider.meta()
        return f"{meta.id}:{meta.model}:{meta.type}"
    except Exception:
        return str(id(provider))


async def resolve_model(provider, config) -> str | None:
    """
    解析插件配置中指定的模型名。

    Args:
        provider: AstrBot Provider 实例
        config: 插件配置（dict/AstrBotConfig），包含 ai_model 字段

    Returns:
        要使用的模型名；未配置、配置为空或模型无效时返回 None（使用默认模型）
    """
    if not provider:
        return None

    model = ""
    try:
        model = (config or {}).get("ai_model") or ""
        model = str(model).strip()
    except Exception:
        model = ""
    if not model:
        return None

    pid = _provider_id(provider)

    # 已缓存且命中，直接返回
    if pid in _supported_cache and model in _supported_cache[pid]:
        return model

    # 拉取 provider 支持模型列表并缓存
    supported: set[str] = set()
    try:
        models = await provider.get_models()
        supported = set(models or [])
    except Exception as e:
        logger.warning(f"无法获取模型列表: {e}")
    _supported_cache[pid] = supported

    if supported and model not in supported:
        preview = "、".join(sorted(supported)[:8])
        logger.warning(
            f"配置的模型 {model} 不在当前 LLM 提供商支持列表中，已回退使用默认模型。"
            f"当前支持模型: {preview}..."
        )
        return None

    return model

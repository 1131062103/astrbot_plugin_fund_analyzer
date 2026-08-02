"""
基金影响因素配置模块
定义不同类型基金的影响因素和搜索关键词
支持季节性因素分析（中国特定节日/时期）
"""

import re
from datetime import datetime
from typing import TypedDict


class FactorInfo(TypedDict):
    """影响因素信息类型"""

    type: str  # 基金类型
    underlying: str  # 追踪标的
    factors: dict[str, list[str]]  # 因素分类及关键词


class SeasonalFactor(TypedDict):
    """季节性因素类型"""

    period: str  # 时期名称
    date_range: str  # 日期范围描述
    impact: str  # 影响方向：positive/negative/neutral
    description: str  # 影响描述
    keywords: list[str]  # 相关搜索关键词


# ============================================================
# 中国特定时期/节日季节性因素配置
# ============================================================

CHINA_SEASONAL_FACTORS: dict[str, list[SeasonalFactor]] = {
    "贵金属": [
        {
            "period": "春节前（腊月）",
            "date_range": "农历腊月初至除夕",
            "impact": "positive",
            "description": "春节前黄金首饰消费旺季，婚庆、送礼需求大增，金价银价往往走强",
            "keywords": ["春节黄金消费", "婚庆首饰需求", "贺岁金银"],
        },
        {
            "period": "国庆黄金周",
            "date_range": "9月下旬至10月上旬",
            "impact": "positive",
            "description": "国庆婚庆旺季，黄金首饰消费需求上升",
            "keywords": ["国庆婚庆", "金九银十", "首饰消费"],
        },
        {
            "period": "情人节/七夕",
            "date_range": "2月14日/农历七月初七前后",
            "impact": "positive",
            "description": "情人节/七夕首饰送礼需求增加",
            "keywords": ["情人节礼物", "七夕黄金", "首饰销售"],
        },
        {
            "period": "年末",
            "date_range": "12月",
            "impact": "neutral",
            "description": "机构年末调仓，贵金属波动可能加大",
            "keywords": ["年末调仓", "资金流向", "机构持仓"],
        },
    ],
    "消费行业": [
        {
            "period": "双十一",
            "date_range": "11月1日至11月11日",
            "impact": "positive",
            "description": "电商大促，消费板块业绩预期提升",
            "keywords": ["双十一销售额", "电商大促", "消费数据"],
        },
        {
            "period": "618大促",
            "date_range": "6月1日至6月18日",
            "impact": "positive",
            "description": "年中电商大促，消费品销售旺季",
            "keywords": ["618销售", "年中大促", "电商业绩"],
        },
        {
            "period": "春节消费季",
            "date_range": "农历腊月至正月",
            "impact": "positive",
            "description": "春节期间白酒、食品等消费品销售旺季",
            "keywords": ["春节消费", "白酒销售", "年货采购"],
        },
        {
            "period": "中秋国庆",
            "date_range": "9月至10月上旬",
            "impact": "positive",
            "description": "节假日消费旺季，白酒礼品需求增加",
            "keywords": ["中秋白酒", "节日消费", "礼品市场"],
        },
    ],
    "新能源行业": [
        {
            "period": "年末抢装",
            "date_range": "11月至12月",
            "impact": "positive",
            "description": "光伏风电年末抢装潮，装机量集中释放",
            "keywords": ["光伏抢装", "风电并网", "年末装机"],
        },
        {
            "period": "两会期间",
            "date_range": "3月上旬",
            "impact": "positive",
            "description": "两会政策预期，新能源政策利好预期",
            "keywords": ["两会政策", "碳中和", "新能源规划"],
        },
    ],
    "房地产行业": [
        {
            "period": "金九银十",
            "date_range": "9月至10月",
            "impact": "positive",
            "description": "传统楼市销售旺季",
            "keywords": ["金九银十", "楼市销售", "房产成交"],
        },
        {
            "period": "年末冲刺",
            "date_range": "12月",
            "impact": "positive",
            "description": "房企年末冲业绩，促销力度加大",
            "keywords": ["房企促销", "年末冲刺", "楼盘优惠"],
        },
    ],
    "能源": [
        {
            "period": "夏季用电高峰",
            "date_range": "7月至8月",
            "impact": "positive",
            "description": "夏季用电高峰，能源需求上升",
            "keywords": ["夏季用电", "电力需求", "煤炭价格"],
        },
        {
            "period": "冬季取暖季",
            "date_range": "11月至次年2月",
            "impact": "positive",
            "description": "北方取暖季，天然气煤炭需求旺盛",
            "keywords": ["取暖季", "天然气需求", "煤炭冬储"],
        },
    ],
    "医药行业": [
        {
            "period": "流感季节",
            "date_range": "11月至次年3月",
            "impact": "positive",
            "description": "流感高发季节，医药需求增加",
            "keywords": ["流感疫情", "医药需求", "疫苗接种"],
        },
        {
            "period": "医保谈判期",
            "date_range": "10月至12月",
            "impact": "negative",
            "description": "医保谈判结果公布，可能影响药品价格预期",
            "keywords": ["医保谈判", "药品降价", "集采结果"],
        },
    ],
    "金融行业": [
        {
            "period": "年报季",
            "date_range": "3月至4月",
            "impact": "neutral",
            "description": "银行年报披露，业绩兑现期",
            "keywords": ["银行年报", "业绩披露", "分红预案"],
        },
        {
            "period": "年末流动性",
            "date_range": "12月",
            "impact": "neutral",
            "description": "年末资金面紧张，银行间利率波动",
            "keywords": ["年末流动性", "资金利率", "央行操作"],
        },
    ],
    "军工行业": [
        {
            "period": "两会预算",
            "date_range": "3月",
            "impact": "positive",
            "description": "两会公布国防预算，军工板块关注度提升",
            "keywords": ["国防预算", "军费增长", "军工订单"],
        },
    ],
    "综合": [
        {
            "period": "两会期间",
            "date_range": "3月上旬",
            "impact": "neutral",
            "description": "政策预期升温，市场观望情绪",
            "keywords": ["两会政策", "政策预期", "市场情绪"],
        },
        {
            "period": "季末效应",
            "date_range": "3月末/6月末/9月末/12月末",
            "impact": "neutral",
            "description": "季末机构调仓，市场波动可能加大",
            "keywords": ["季末调仓", "机构持仓", "基金仓位"],
        },
    ],
}


# ============================================================
# 国际形势/地缘政治因素配置
# ============================================================

GLOBAL_SITUATION_FACTORS: dict[str, dict] = {
    "贵金属": {
        "keywords": [
            "美联储加息", "美联储降息", "美元汇率",
            "地缘政治冲突", "中东局势", "俄乌冲突",
            "避险情绪", "全球通胀", "美国通胀数据",
            "全球央行购金", "中国央行购金", "印度购金",
        ],
        "impact_desc": "贵金属作为避险资产，受美联储政策、地缘冲突、通胀预期影响显著",
        "positive_signals": ["地缘冲突升级", "美联储降息预期", "通胀抬头", "央行增持黄金", "美元贬值"],
        "negative_signals": ["地缘缓和", "美联储加息", "通胀回落", "美元走强", "风险偏好回升"],
    },
    "能源": {
        "keywords": [
            "OPEC减产", "OPEC增产", "中东局势",
            "俄罗斯石油", "美国页岩油", "原油库存",
            "全球经济增长", "制造业PMI", "能源危机",
        ],
        "impact_desc": "能源价格受OPEC政策、地缘冲突、全球经济需求影响",
        "positive_signals": ["OPEC减产", "中东紧张", "库存下降", "经济复苏"],
        "negative_signals": ["OPEC增产", "库存累积", "经济衰退担忧"],
    },
    "科技行业": {
        "keywords": [
            "中美科技摆擦", "芯片制裁", "半导体出口管制",
            "科技自主可控", "AI产业", "英伟达业绩",
        ],
        "impact_desc": "科技行业受中美关系、芯片管制、AI产业发展影响",
        "positive_signals": ["国产替代加速", "AI产业爆发", "半导体周期回暖"],
        "negative_signals": ["制裁升级", "出口管制加严", "产业链担忧"],
    },
    "金融行业": {
        "keywords": [
            "央行政策", "LPR利率", "存款准备金率",
            "中美利差", "人民币汇率", "资本市场改革",
        ],
        "impact_desc": "金融行业受国内货币政策、中美利差、经济周期影响",
        "positive_signals": ["降准降息", "信贷扩张", "经济复苏"],
        "negative_signals": ["不良贷款上升", "利差收窄", "房地产风险"],
    },
    "综合": {
        "keywords": [
            "全球经济", "美联储政策", "中国GDP",
            "地缘政治", "A股走势", "资金流向",
        ],
        "impact_desc": "综合受国内外经济形势、政策预期、市场情绪影响",
        "positive_signals": ["政策利好", "经济复苏", "外资流入"],
        "negative_signals": ["政策收紧", "经济下行", "资金外流"],
    },
}


# 基金类型关键词映射配置
FUND_TYPE_FACTORS: dict[str, FactorInfo] = {
    "白银": {
        "type": "贵金属",
        "underlying": "白银期货",
        "factors": {
            "商品价格": ["白银价格走势", "COMEX白银", "上海白银期货"],
            "宏观经济": ["美联储利率决议", "美元指数走势", "通胀数据"],
            "地缘政治": ["地缘政治风险", "避险情绪"],
            "供需关系": ["白银工业需求", "光伏白银需求", "白银产量"],
            "市场情绪": ["贵金属ETF持仓", "白银投资需求"],
            "季节性消费": ["春节首饰需求", "婚庆旺季", "节日送礼"],
        },
    },
    "黄金": {
        "type": "贵金属",
        "underlying": "黄金期货",
        "factors": {
            "商品价格": ["黄金价格走势", "COMEX黄金", "上海金"],
            "宏观经济": ["美联储利率", "美元走势", "实际利率"],
            "地缘政治": ["地缘风险", "避险需求"],
            "央行政策": ["央行购金", "黄金储备"],
            "市场情绪": ["黄金ETF持仓", "投资需求"],
            "季节性消费": ["春节黄金消费", "婚庆首饰", "节日购金"],
        },
    },
    "原油|石油": {
        "type": "能源",
        "underlying": "原油期货",
        "factors": {
            "商品价格": ["原油价格", "WTI原油", "布伦特原油"],
            "供需关系": ["OPEC减产", "原油库存", "美国页岩油"],
            "宏观经济": ["全球经济增长", "制造业PMI"],
            "地缘政治": ["中东局势", "俄乌冲突"],
        },
    },
    "医药|医疗|生物": {
        "type": "医药行业",
        "underlying": "医药股票",
        "factors": {
            "政策因素": ["医药集采", "医保谈判", "药品审批"],
            "行业动态": ["创新药研发", "医药企业业绩"],
            "市场情绪": ["医药板块资金流向"],
        },
    },
    "科技|芯片|半导体": {
        "type": "科技行业",
        "underlying": "科技股票",
        "factors": {
            "产业政策": ["芯片政策", "科技自主"],
            "行业周期": ["半导体周期", "消费电子需求"],
            "国际贸易": ["芯片出口管制", "科技摩擦"],
        },
    },
    "消费|食品|白酒": {
        "type": "消费行业",
        "underlying": "消费股票",
        "factors": {
            "宏观数据": ["社会消费品零售", "CPI数据"],
            "政策因素": ["促消费政策", "消费补贴"],
            "企业业绩": ["消费龙头业绩", "白酒销售"],
        },
    },
    "新能源|光伏|锂电": {
        "type": "新能源行业",
        "underlying": "新能源股票",
        "factors": {
            "产业政策": ["新能源补贴", "碳中和政策"],
            "供需关系": ["锂价走势", "硅料价格", "装机量"],
            "技术进步": ["电池技术", "光伏效率"],
        },
    },
    "银行|金融": {
        "type": "金融行业",
        "underlying": "银行股票",
        "factors": {
            "货币政策": ["LPR利率", "存款准备金率"],
            "宏观经济": ["GDP增速", "信贷数据"],
            "监管政策": ["金融监管", "资本充足率"],
        },
    },
    "房地产|地产": {
        "type": "房地产行业",
        "underlying": "地产股票",
        "factors": {
            "政策因素": ["房地产政策", "限购限贷"],
            "市场数据": ["房价走势", "销售数据"],
            "资金链": ["房企融资", "债务风险"],
        },
    },
    "军工|国防": {
        "type": "军工行业",
        "underlying": "军工股票",
        "factors": {
            "国防预算": ["军费开支", "国防预算"],
            "地缘局势": ["周边安全形势", "国际关系"],
            "订单交付": ["军工订单", "装备交付"],
        },
    },
}

# 默认因素（通用）
DEFAULT_FACTORS: FactorInfo = {
    "type": "综合",
    "underlying": "多元资产",
    "factors": {
        "宏观经济": ["宏观经济数据", "GDP增速", "PMI数据"],
        "政策因素": ["货币政策", "财政政策"],
        "市场情绪": ["A股市场走势", "资金流向"],
    },
}


class FundInfluenceFactors:
    """基金影响因素分析器"""

    @staticmethod
    def get_factors(fund_name: str) -> FactorInfo:
        """
        根据基金名称获取可能的影响因素

        Args:
            fund_name: 基金名称

        Returns:
            影响因素信息
        """
        # 根据基金名称匹配类型
        for keyword_pattern, info in FUND_TYPE_FACTORS.items():
            if re.search(keyword_pattern, fund_name):
                return info

        return DEFAULT_FACTORS

    @staticmethod
    def get_search_keywords(fund_name: str) -> list[str]:
        """
        获取用于搜索新闻的关键词列表

        Args:
            fund_name: 基金名称

        Returns:
            搜索关键词列表
        """
        factors = FundInfluenceFactors.get_factors(fund_name)
        keywords = []

        # 添加追踪标的
        if factors["underlying"]:
            keywords.append(factors["underlying"])

        # 从各因素中提取关键词
        for category, kw_list in factors["factors"].items():
            keywords.extend(kw_list[:2])  # 每个类别取前2个

        return keywords[:10]  # 最多返回10个

    @staticmethod
    def get_seasonal_factors(fund_type: str) -> list[SeasonalFactor]:
        """
        获取指定基金类型的季节性因素

        Args:
            fund_type: 基金类型（如"贵金属"、"消费行业"等）

        Returns:
            季节性因素列表
        """
        return CHINA_SEASONAL_FACTORS.get(fund_type, CHINA_SEASONAL_FACTORS.get("综合", []))

    @staticmethod
    def get_current_seasonal_context(fund_name: str) -> str:
        """
        获取当前时期对基金的季节性影响分析

        Args:
            fund_name: 基金名称

        Returns:
            当前季节性影响的文本描述
        """
        factors = FundInfluenceFactors.get_factors(fund_name)
        fund_type = factors["type"]
        seasonal_factors = FundInfluenceFactors.get_seasonal_factors(fund_type)

        now = datetime.now()
        month = now.month
        day = now.day

        relevant_factors = []

        for sf in seasonal_factors:
            # 简单的月份匹配逻辑
            date_range = sf["date_range"]
            is_relevant = False

            # 春节前（腊月）- 大约1月中旬到2月中旬
            if "腊月" in date_range or "春节" in date_range:
                if month == 1 or (month == 2 and day <= 15):
                    is_relevant = True
            # 双十一
            elif "11月" in date_range and "11日" in date_range:
                if month == 11 and day <= 15:
                    is_relevant = True
            # 618
            elif "6月" in date_range and "18日" in date_range:
                if month == 6 and day <= 20:
                    is_relevant = True
            # 国庆/中秋 (9-10月)
            elif "9月" in date_range or "10月" in date_range:
                if month in [9, 10]:
                    is_relevant = True
            # 年末 (12月)
            elif "12月" in date_range:
                if month == 12:
                    is_relevant = True
            # 两会 (3月)
            elif "3月" in date_range:
                if month == 3 and day <= 15:
                    is_relevant = True
            # 夏季 (7-8月)
            elif "7月" in date_range or "8月" in date_range:
                if month in [7, 8]:
                    is_relevant = True
            # 冬季取暖 (11月-2月)
            elif "11月至次年" in date_range or "取暖" in date_range:
                if month in [11, 12, 1, 2]:
                    is_relevant = True
            # 季末
            elif "季末" in date_range or "月末" in date_range:
                # 季末最后一周
                if month in [3, 6, 9, 12] and day >= 25:
                    is_relevant = True

            if is_relevant:
                impact_emoji = {
                    "positive": "📈",
                    "negative": "📉",
                    "neutral": "➡️",
                }.get(sf["impact"], "❓")
                relevant_factors.append(
                    f"{impact_emoji} 【{sf['period']}】{sf['description']}"
                )

        if relevant_factors:
            return "当前季节性因素:\n" + "\n".join(relevant_factors)
        return "当前无明显季节性影响因素"

    @staticmethod
    def get_news_search_keywords(fund_name: str) -> list[str]:
        """
        获取用于新闻搜索的关键词列表（增强版）

        Args:
            fund_name: 基金名称

        Returns:
            搜索关键词列表，用于搜索相关新闻
        """
        factors = FundInfluenceFactors.get_factors(fund_name)
        fund_type = factors["type"]
        keywords = []

        # 1. 添加追踪标的
        if factors["underlying"]:
            keywords.append(factors["underlying"])

        # 2. 从各因素中提取关键词
        for category, kw_list in factors["factors"].items():
            keywords.extend(kw_list[:2])

        # 3. 添加当前季节性相关关键词
        seasonal_factors = FundInfluenceFactors.get_seasonal_factors(fund_type)
        now = datetime.now()
        month = now.month

        for sf in seasonal_factors:
            date_range = sf["date_range"]
            # 简化的月份匹配
            if (
                (month == 1 and ("腊月" in date_range or "春节" in date_range))
                or (month == 2 and ("春节" in date_range or "正月" in date_range))
                or (month == 11 and "11月" in date_range)
                or (month == 6 and "6月" in date_range)
                or (month in [9, 10] and ("9月" in date_range or "10月" in date_range))
                or (month == 12 and "12月" in date_range)
                or (month == 3 and "3月" in date_range)
            ):
                keywords.extend(sf["keywords"])

        # 去重并限制数量
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        return unique_keywords[:15]

    @staticmethod
    def get_global_situation_factors(fund_type: str) -> dict:
        """
        获取指定基金类型的国际形势因素

        Args:
            fund_type: 基金类型

        Returns:
            国际形势因素配置
        """
        return GLOBAL_SITUATION_FACTORS.get(fund_type, GLOBAL_SITUATION_FACTORS.get("综合", {}))

    @staticmethod
    def format_global_situation_text(fund_name: str) -> str:
        """
        格式化国际形势因素为文本

        Args:
            fund_name: 基金名称

        Returns:
            国际形势分析文本
        """
        factors = FundInfluenceFactors.get_factors(fund_name)
        fund_type = factors["type"]
        global_factors = FundInfluenceFactors.get_global_situation_factors(fund_type)

        if not global_factors:
            return "无特定国际形势影响因素"

        text = f"**国际形势影响分析** ({global_factors.get('impact_desc', '')})\n"
        text += "\n重点关注新闻关键词:\n"
        keywords = global_factors.get("keywords", [])
        text += f"  {', '.join(keywords[:8])}\n"
        text += "\n利多信号词:\n"
        text += f"  📈 {', '.join(global_factors.get('positive_signals', []))}\n"
        text += "利空信号词:\n"
        text += f"  📉 {', '.join(global_factors.get('negative_signals', []))}\n"

        return text

    @staticmethod
    def format_factors_text(fund_name: str) -> str:
        """
        格式化影响因素为文本（增强版，包含季节性因素）

        Args:
            fund_name: 基金名称

        Returns:
            格式化的文本
        """
        factors = FundInfluenceFactors.get_factors(fund_name)

        text = f"标的类型: {factors['type']}\n"
        text += f"追踪标的: {factors['underlying']}\n"
        text += "主要影响因素:\n"

        for category, keywords in factors["factors"].items():
            text += f"  【{category}】{', '.join(keywords)}\n"

        # 添加季节性因素
        seasonal_context = FundInfluenceFactors.get_current_seasonal_context(fund_name)
        text += f"\n{seasonal_context}\n"

        return text

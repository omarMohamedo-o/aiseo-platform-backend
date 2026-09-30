export type Language = "en" | "ar" | "zh";

export interface Translations {
  appName: string;
  phaseBadge: string;
  appSubtitle: string;
  monolithBadge: string;
  tenantBadge: string;
  nav: {
    crawl: string;
    leaderboard: string;
    compare: string;
    intel: string;
    trends: string;
    lab: string;
    more: string;
    email: string;
    overview: string;
    flow: string;
    vault: string;
  };
  crawlTab: {
    title: string;
    badge: string;
    subtitle: string;
    quickTargets: string;
    targetUrlLabel: string;
    brandNameLabel: string;
    scopeLabel: string;
    scopeAll: string;
    scope5: string;
    scope15: string;
    scope35: string;
    crawlButton: string;
    crawlingButton: string;
    stages: {
      sitemap: string;
      extraction: string;
      scoring: string;
      recommendations: string;
    };
    liveExecution: string;
    targetText: string;
    kpi: {
      overallVisibility: string;
      overallVisibilitySub: string;
      overallOpportunity: string;
      overallOpportunitySub: string;
      pagesDetected: string;
      pagesDetectedSub: string;
      totalText: string;
      totalTextSub: string;
      realtime: string;
      sitewide: string;
    };
    searchStats: {
      title: string;
      subtitle: string;
      badge: string;
      searchRank: string;
      searchRankSub: string;
      aiSearchRank: string;
      aiSearchRankSub: string;
      monthlySearches: string;
      monthlySearchesSub: string;
      uniqueSearchers: string;
      uniqueSearchersSub: string;
      searchAppearances: string;
      searchAppearancesSub: string;
      aiAppearances: string;
      aiAppearancesSub: string;
      ctr: string;
      cpc: string;
      monthlyTraffic: string;
      shareOfVoice: string;
      topQueriesTitle: string;
      colQuery: string;
      colRank: string;
      colVolume: string;
      colAppearances: string;
      colAiAppearances: string;
      colCtr: string;
      colCpc: string;
      colCompetition: string;
    };
    recommendations: {
      title: string;
      subtitle: string;
      badge: string;
      priority: string;
      checklist: string;
    };
    perPage: {
      title: string;
      subtitle: string;
      filterPlaceholder: string;
      colPath: string;
      colVis: string;
      colOpp: string;
      colChars: string;
      colBrand: string;
      colSearchRank: string;
      colSearchVol: string;
      colSearchApp: string;
      colRec: string;
      colAction: string;
      inspect: string;
      brandPresent: string;
      brandMissing: string;
      inspectorTitle: string;
      extractedTextTitle: string;
      specificRecsTitle: string;
    };
    questions: {
      title: string;
      subtitle: string;
      colQuery: string;
      colIntent: string;
      colStage: string;
      colRationale: string;
    };
    citations: {
      title: string;
      subtitle: string;
      verified: string;
    };
  };
}

export const translations: Record<Language, Translations> = {
  en: {
    appName: "AISEO Platform",
    phaseBadge: "Phase 1 Production",
    appSubtitle: "Enterprise AI Visibility & Answer Engine Optimization (GEO / AEO) Command Center",
    monolithBadge: "FastAPI Monolith / Microservices Ready",
    tenantBadge: "Tenant: default-tenant",
    nav: {
      crawl: "Audit",
      leaderboard: "Leaderboard",
      compare: "Compare",
      intel: "Keywords",
      trends: "Trends",
      lab: "Query Lab",
      more: "More",
      email: "Email Reports",
      overview: "Architecture",
      flow: "Workflow Engine",
      vault: "API Keys",
    },
    crawlTab: {
      title: "Live Website Crawler & Generative Audit Engine",
      badge: "Trafilatura + Httpx + Sitemaps",
      subtitle: "Auto-detect total pages on any domain, crawl & extract pure text across all subpages, score each page individually, and get actionable recommendations to increase AI engine visibility.",
      quickTargets: "Quick Targets:",
      targetUrlLabel: "Active Website Target URL",
      brandNameLabel: "Brand / Entity Name",
      scopeLabel: "Pages Scope:",
      scopeAll: "All Pages (Auto-Detect)",
      scope5: "5 Pages",
      scope15: "15 Pages",
      scope35: "35 Pages",
      crawlButton: "Perform Real Website Crawl & Audit",
      crawlingButton: "Crawling & Auditing Entire Site...",
      stages: {
        sitemap: "Sitemap & Page Auto-Detection",
        extraction: "Concurrent DOM & Meta Extraction",
        scoring: "Semantic Chunking & Per-Page Scoring",
        recommendations: "Strategic GEO Recommendations",
      },
      liveExecution: "Live Pipeline Execution in Progress",
      targetText: "Target:",
      kpi: {
        overallVisibility: "Overall AI Visibility",
        overallVisibilitySub: "Audited against neural engine direct-answer queries",
        overallOpportunity: "Overall Opportunity",
        overallOpportunitySub: "Formula: 40% Vol + 30% KD + 15% CPC + 15% SERP",
        pagesDetected: "Domain Pages Detected",
        pagesDetectedSub: "Discovered via Sitemap.xml and internal link traversal",
        totalText: "Total Extracted Text",
        totalTextSub: "Decomposed into semantic chunks",
        realtime: "Real-time",
        sitewide: "Site-wide",
      },
      searchStats: {
        title: "Search Rankings, Search Volume & Appearance Statistics",
        subtitle: "Real search demand analysis, monthly search volume, unique people searching, SERP impressions, and generative AI answer appearances",
        badge: "Search & Neural Intelligence",
        searchRank: "Organic Search Rank",
        searchRankSub: "Average position across Google & Bing SERP",
        aiSearchRank: "AI Citation Rank",
        aiSearchRankSub: "Position in ChatGPT & Perplexity direct answers",
        monthlySearches: "Monthly Search Volume",
        monthlySearchesSub: "Total search frequency across brand & topics",
        uniqueSearchers: "People Searching",
        uniqueSearchersSub: "Estimated unique monthly search audience",
        searchAppearances: "Search Appearances",
        searchAppearancesSub: "Total impressions in search query results",
        aiAppearances: "AI Answer Appearances",
        aiAppearancesSub: "Times cited in neural engine responses",
        ctr: "Organic CTR",
        cpc: "Avg CPC",
        monthlyTraffic: "Estimated Monthly Traffic",
        shareOfVoice: "Share of Voice",
        topQueriesTitle: "High-Intent Search Queries & Impression Distribution",
        colQuery: "Search Query",
        colRank: "SERP Rank",
        colVolume: "Monthly Searches",
        colAppearances: "Search Appearances",
        colAiAppearances: "AI Citations",
        colCtr: "CTR",
        colCpc: "CPC",
        colCompetition: "Competition",
      },
      recommendations: {
        title: "Actionable Recommendations to Increase AI Engine Scores",
        subtitle: "Specific steps to boost citation frequency and positioning in ChatGPT, Perplexity, Claude & Gemini",
        badge: "High Impact Optimization",
        priority: "Priority",
        checklist: "Action Checklist:",
      },
      perPage: {
        title: "Individual Per-Page Scores & Content Depth Audit",
        subtitle: "Detailed visibility, opportunity, and recommendations calculated separately for every crawled page",
        filterPlaceholder: "Filter by page or keyword...",
        colPath: "Page Path & Title",
        colVis: "Visibility Score",
        colOpp: "Opportunity Score",
        colChars: "Characters / Chunks",
        colBrand: "Brand Mention",
        colSearchRank: "Search Rank",
        colSearchVol: "Searches / Mo",
        colSearchApp: "Appearances",
        colRec: "Key Action Recommendation",
        colAction: "Action",
        inspect: "Inspect",
        brandPresent: "Present",
        brandMissing: "Missing",
        inspectorTitle: "Page Content Inspector:",
        extractedTextTitle: "Extracted DOM & Semantic Body Text:",
        specificRecsTitle: "Specific Recommendations for This Page:",
      },
      questions: {
        title: "Generated Buyer Persona Questions Across All Pages",
        subtitle: "Simulated User Inquiries for ChatGPT, Claude, Perplexity",
        colQuery: "Generated Search Query",
        colIntent: "Intent Lens",
        colStage: "Funnel Stage",
        colRationale: "Strategic Evaluation Rationale",
      },
      citations: {
        title: "Verified Citations & Domain Authority",
        subtitle: "Extracted URLs verified as direct references across domain links",
        verified: "Verified",
      },
    },
  },

  ar: {
    appName: "منصة AISEO الذكية",
    phaseBadge: "الإصدار الإنتاجي الأول",
    appSubtitle: "مركز قيادة ظهور الذكاء الاصطناعي وتحسين محركات الإجابة العصبية (GEO / AEO)",
    monolithBadge: "معمارية FastAPI الموحدة / جاهزة للخدمات المصغرة",
    tenantBadge: "المستأجر: default-tenant",
    nav: {
      crawl: "فحص المواقع",
      leaderboard: "لوحة المتصدرين",
      compare: "مقارنة المنافسين",
      intel: "الكلمات المفتاحية",
      trends: "مؤشرات البحث",
      lab: "مختبر الأسئلة",
      more: "المزيد",
      email: "تقارير البريد",
      overview: "مواصفات النظام",
      flow: "محرك التدفق",
      vault: "مفاتيح API",
    },
    crawlTab: {
      title: "محرك الزحف المباشر وتدقيق الذكاء الاصطناعي للمواقع",
      badge: "Trafilatura + Httpx + خرائط المواقع",
      subtitle: "اكتشاف تلقائي لكافة صفحات النطاق، استخراج النصوص النقية لجميع الصفحات الفرعية، تقييم درجات كل صفحة بشكل منفصل، وتوصيات عملية لزيادة الظهور في محركات الذكاء الاصطناعي.",
      quickTargets: "أهداف سريعة:",
      targetUrlLabel: "رابط الموقع النشط المستهدف",
      brandNameLabel: "اسم العلامة التجارية / الكيان",
      scopeLabel: "نطاق الصفحات:",
      scopeAll: "كافة الصفحات (اكتشاف تلقائي)",
      scope5: "5 صفحات",
      scope15: "15 صفحة",
      scope35: "35 صفحة",
      crawlButton: "بدء الزحف الفعلي وتدقيق الموقع",
      crawlingButton: "جارٍ الزحف والتدقيق الشامل لكامل الموقع...",
      stages: {
        sitemap: "اكتشاف خريطة الموقع والصفحات",
        extraction: "استخراج نصوص DOM والبيانات الوصفية",
        scoring: "التقطيع الدلالي وحساب درجات كل صفحة",
        recommendations: "إنشاء توصيات استراتيجية الظهور (GEO)",
      },
      liveExecution: "تنفيذ المسار المباشر قيد المعالجة الآن",
      targetText: "الهدف:",
      kpi: {
        overallVisibility: "معدل الظهور العام في الذكاء الاصطناعي",
        overallVisibilitySub: "تدقيق دقيق ضد استفسارات محركات الإجابة العصبية",
        overallOpportunity: "مؤشر الفرصة الاستراتيجية العام",
        overallOpportunitySub: "المعادلة: 40% حجم البحث + 30% صعوبة الكلمة + 15% نقرة + 15% نتائج البحث",
        pagesDetected: "إجمالي الصفحات المكتشفة",
        pagesDetectedSub: "تم العثور عليها عبر Sitemap.xml والروابط الداخلية للنطاق",
        totalText: "إجمالي النصوص المستخرجة",
        totalTextSub: "تم تقسيمها إلى أجزاء دلالية مفهرسة للبحث المتجهي",
        realtime: "مباشر",
        sitewide: "لكامل الموقع",
      },
      searchStats: {
        title: "إحصائيات الترتيب والبحث ومعدل الظهور في محركات البحث والذكاء الاصطناعي",
        subtitle: "تحليل شامل لحجم البحث الشهري، عدد الأشخاص الذين يبحثون، مرات الظهور في النتائج، والظهور في إجابات الذكاء الاصطناعي",
        badge: "استخبارات الظهور والترتيب الفعلي",
        searchRank: "الترتيب في محركات البحث",
        searchRankSub: "متوسط الترتيب في نتائج Google و Bing",
        aiSearchRank: "ترتيب الاقتباس بالذكاء الاصطناعي",
        aiSearchRankSub: "المرتبة في إجابات ChatGPT و Perplexity المباشرة",
        monthlySearches: "حجم البحث الشهري (مرات البحث)",
        monthlySearchesSub: "إجمالي عمليات البحث شهرياً عن علامتك ومجالك",
        uniqueSearchers: "عدد الأشخاص الباحثين",
        uniqueSearchersSub: "الجمهور الفعلي الفريد الذي يبحث عن خدماتك شهرياً",
        searchAppearances: "مرات الظهور في البحث (الانطباعات)",
        searchAppearancesSub: "إجمالي مرات ظهور موقعك في نتائج البحث",
        aiAppearances: "مرات الظهور في إجابات الذكاء الاصطناعي",
        aiAppearancesSub: "عدد المرات التي استشهد فيها الذكاء الاصطناعي بموقعك",
        ctr: "نسبة النقر للظهور (CTR)",
        cpc: "سعر النقرة (CPC)",
        monthlyTraffic: "الزيارات التقديرية شهرياً",
        shareOfVoice: "حصة الصوت في السوق",
        topQueriesTitle: "أبرز استفسارات البحث وتوزيع مرات الظهور",
        colQuery: "استفسار البحث",
        colRank: "الترتيب",
        colVolume: "مرات البحث",
        colAppearances: "مرات الظهور",
        colAiAppearances: "ظهور الذكاء الاصطناعي",
        colCtr: "معدل النقر",
        colCpc: "تكلفة النقرة",
        colCompetition: "المنافسة",
      },
      recommendations: {
        title: "توصيات عملية واستراتيجية لرفع درجات الظهور",
        subtitle: "خطوات محددة لزيادة معدل الاستشهاد والترتيب في ChatGPT و Perplexity و Claude و Gemini",
        badge: "تحسين عالي التأثير والأولوية",
        priority: "أولوية",
        checklist: "قائمة خطوات التنفيذ:",
      },
      perPage: {
        title: "تقييم الدرجات الفردية وعمق المحتوى وإحصائيات البحث لكل صفحة",
        subtitle: "حساب مؤشرات الظهور والترتيب ومرات البحث والتوصيات المخصصة بشكل منفصل لكل رابط تم الزحف إليه",
        filterPlaceholder: "تصفية بالصفحة أو الكلمة المفتاحية...",
        colPath: "مسار الصفحة وعنوانها",
        colVis: "درجة الظهور",
        colOpp: "مؤشر الفرصة",
        colChars: "الأحرف / الأجزاء",
        colBrand: "العلامة التجارية",
        colSearchRank: "الترتيب",
        colSearchVol: "مرات البحث/شهر",
        colSearchApp: "مرات الظهور",
        colRec: "أبرز توصية للتنفيذ",
        colAction: "الإجراء",
        inspect: "معاينة",
        brandPresent: "مذكورة",
        brandMissing: "غير مذكورة",
        inspectorTitle: "معاينة محتوى الصفحة وتوصياتها:",
        extractedTextTitle: "النصوص المستخرجة من الصفحة:",
        specificRecsTitle: "توصيات مخصصة لهذه الصفحة تحديداً:",
      },
      questions: {
        title: "أسئلة المشترين والجمهور المستهدف المنشأة عبر كافة الصفحات",
        subtitle: "محاكاة استفسارات المستخدمين الحقيقيين لـ ChatGPT و Claude و Perplexity",
        colQuery: "استفسار البحث المولد",
        colIntent: "عدسة القصد والنية",
        colStage: "مرحلة مسار الشراء",
        colRationale: "مبرر التقييم الاستراتيجي",
      },
      citations: {
        title: "الاستشهادات الموثوقة ومصادر النطاق المعتمدة",
        subtitle: "الروابط المفحوصة والمؤكدة كمراجع مباشرة في نتائج الاستعلام",
        verified: "موثق",
      },
    },
  },

  zh: {
    appName: "AISEO 智能中枢",
    phaseBadge: "第一阶段 生产就绪",
    appSubtitle: "企业级 AI 可见度与生成式回答引擎优化 (GEO / AEO) 指挥中心",
    monolithBadge: "FastAPI 单体架构 / 微服务就绪",
    tenantBadge: "租户: default-tenant",
    nav: {
      crawl: "网站审计",
      leaderboard: "全球榜单",
      compare: "竞品对比",
      intel: "关键词库",
      trends: "搜索趋势",
      lab: "提示词工坊",
      more: "更多工具",
      email: "邮件报告",
      overview: "系统架构",
      flow: "执行流引擎",
      vault: "API 密钥",
    },
    crawlTab: {
      title: "实时网站爬虫与生成式 AI 审计引擎",
      badge: "Trafilatura + Httpx + 站点地图",
      subtitle: "自动检测全站页面总量，并发抓取并解析全站纯文本，独立计算单页与整体得分，输出提升 AI 大模型引用率的实战建议。",
      quickTargets: "快速目标:",
      targetUrlLabel: "活跃网站目标网址",
      brandNameLabel: "品牌 / 实体名称",
      scopeLabel: "页面范围:",
      scopeAll: "全站所有页面 (自动探测)",
      scope5: "5 个页面",
      scope15: "15 个页面",
      scope35: "35 个页面",
      crawlButton: "执行真实网站爬取与审计",
      crawlingButton: "正在爬取并全面审计全站内容...",
      stages: {
        sitemap: "站点地图探测与页面发现",
        extraction: "并发 DOM 结构与元数据提取",
        scoring: "语义分块与单页独立评分",
        recommendations: "生成战略级 GEO 优化建议",
      },
      liveExecution: "实时流水线执行中",
      targetText: "目标:",
      kpi: {
        overallVisibility: "全站 AI 综合可见度",
        overallVisibilitySub: "基于神经网络回答引擎直接引用的实测得分",
        overallOpportunity: "综合商业机会评分",
        overallOpportunitySub: "公式: 40% 搜索量 + 30% 难度 + 15% CPC + 15% SERP 特性",
        pagesDetected: "全站检测页面总量",
        pagesDetectedSub: "通过 Sitemap.xml 及内部链接图谱全面发现",
        totalText: "提取纯文本总量",
        totalTextSub: "已切分为高质量语义文本块供向量索引检索",
        realtime: "实时",
        sitewide: "全站统计",
      },
      searchStats: {
        title: "搜索引擎与 AI 问答真实排名、搜索量与曝光量统计",
        subtitle: "月度搜索总量、独立搜索人数、搜索展现曝光量以及大模型直接回答引用出现频次的全面统计",
        badge: "搜索与神经引擎曝光智能",
        searchRank: "自然搜索排名",
        searchRankSub: "在 Google 与主流搜索引擎中的平均排位",
        aiSearchRank: "AI 引用位次",
        aiSearchRankSub: "在 ChatGPT 与 Perplexity 直接回答中的引用排序",
        monthlySearches: "月度搜索量 (被搜索次数)",
        monthlySearchesSub: "品牌与核心业务词的全网月度搜索总频次",
        uniqueSearchers: "搜索受众人数",
        uniqueSearchersSub: "每月主动检索该业务的独立用户预估规模",
        searchAppearances: "搜索展现量 (曝光次数)",
        searchAppearancesSub: "在搜索引擎结果页面中的总计曝光次数",
        aiAppearances: "AI 答案出现频次",
        aiAppearancesSub: "在大模型生成回答中被作为参考来源引用的次数",
        ctr: "点击率 (CTR)",
        cpc: "平均单次点击费用",
        monthlyTraffic: "预估月自然流量",
        shareOfVoice: "行业声量份额 (SOV)",
        topQueriesTitle: "高意向核心搜索查询与展现分布",
        colQuery: "搜索查询词",
        colRank: "搜索位次",
        colVolume: "月搜索频次",
        colAppearances: "搜索展现量",
        colAiAppearances: "AI 引用量",
        colCtr: "点击率",
        colCpc: "CPC",
        colCompetition: "竞争度",
      },
      recommendations: {
        title: "提升 AI 引擎可见度与引用率的行动指南",
        subtitle: "针对 ChatGPT、Perplexity、Claude 及 Gemini 排序机制量身定制的具体提升步骤",
        badge: "高优先级优化建议",
        priority: "优先级",
        checklist: "行动核对清单:",
      },
      perPage: {
        title: "独立单页评分、搜索统计与内容深度审计清单",
        subtitle: "针对抓取的每个页面分别计算独立可见度得分、搜索排名、曝光量与定向改进建议",
        filterPlaceholder: "按路径或关键词过滤页面...",
        colPath: "页面路径与标题",
        colVis: "可见度得分",
        colOpp: "机会评分",
        colChars: "字符数 / 文本块",
        colBrand: "品牌提及",
        colSearchRank: "搜索排位",
        colSearchVol: "月搜索频次",
        colSearchApp: "搜索展现量",
        colRec: "核心改进建议",
        colAction: "操作",
        inspect: "检视内容",
        brandPresent: "已包含",
        brandMissing: "未提及",
        inspectorTitle: "单页内容与建议检视器:",
        extractedTextTitle: "从该页面提取的纯文本与语义正文:",
        specificRecsTitle: "针对该页面的专属改进措施:",
      },
      questions: {
        title: "基于全站业务体系生成的买家人格提问矩阵",
        subtitle: "模拟真实高潜用户向 ChatGPT、Claude 与 Perplexity 提出的采购咨询问题",
        colQuery: "生成式搜索查询",
        colIntent: "意图透镜",
        colStage: "采购决策阶段",
        colRationale: "战略评估依据",
      },
      citations: {
        title: "已验证权威引用与域名权重",
        subtitle: "在 AI 引擎测试探测中被成功引用为直接来源的页面清单",
        verified: "已验证",
      },
    },
  },
};

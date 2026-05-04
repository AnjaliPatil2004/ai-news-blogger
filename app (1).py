import streamlit as st
import random
import time
from datetime import datetime, timedelta

# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI News Auto-Blogger", page_icon="🤖",
                   layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────────────────────────────────────
#  CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Nunito:wght@300;400;600&display=swap');

:root{--bg:#080b14;--surf:#0e1220;--surf2:#141826;--border:#1e2438;
      --accent:#38bdf8;--accent2:#818cf8;--green:#34d399;--pink:#f472b6;
      --text:#e2e8f0;--muted:#64748b;}

html,body,[class*="css"]{font-family:'Nunito',sans-serif!important;
  background:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
.main .block-container{padding:1.8rem 2.5rem;max-width:1180px;}

/* hero */
.hero{background:linear-gradient(135deg,#0e1220 0%,#0a1128 60%,#0e0e20 100%);
  border:1px solid var(--border);border-radius:22px;padding:2.4rem 3rem;
  margin-bottom:1.8rem;position:relative;overflow:hidden;}
.hero::after{content:'';position:absolute;top:-80px;right:-60px;
  width:320px;height:320px;
  background:radial-gradient(circle,rgba(56,189,248,.13) 0%,transparent 70%);
  pointer-events:none;}
.hero-title{font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;
  background:linear-gradient(120deg,#fff 0%,#38bdf8 45%,#818cf8 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin:0;line-height:1.15;}
.hero-sub{font-family:'JetBrains Mono',monospace;font-size:.78rem;
  color:var(--green);margin-top:.5rem;letter-spacing:.12em;}
.badge{display:inline-block;background:rgba(56,189,248,.12);
  border:1px solid rgba(56,189,248,.3);border-radius:20px;padding:3px 12px;
  font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--accent);margin:3px;}

/* sidebar */
section[data-testid="stSidebar"]{background:var(--surf)!important;
  border-right:1px solid var(--border)!important;}

/* buttons */
.stButton>button{background:linear-gradient(135deg,#0ea5e9,#6366f1)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.55rem 1.4rem!important;font-family:'Syne',sans-serif!important;
  font-weight:700!important;font-size:.88rem!important;
  transition:all .2s!important;width:100%!important;}
.stButton>button:hover{transform:translateY(-2px)!important;
  box-shadow:0 10px 28px rgba(14,165,233,.35)!important;}

/* inputs */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,
.stSelectbox>div>div>div{background:var(--surf2)!important;
  border:1px solid var(--border)!important;border-radius:10px!important;
  color:var(--text)!important;font-family:'JetBrains Mono',monospace!important;
  font-size:.83rem!important;}

/* tabs */
.stTabs [data-baseweb="tab-list"]{background:var(--surf2)!important;
  border-radius:14px!important;padding:5px!important;
  border:1px solid var(--border)!important;gap:4px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;
  border-radius:10px!important;color:var(--muted)!important;
  font-family:'Syne',sans-serif!important;font-weight:600!important;
  font-size:.83rem!important;}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#0ea5e9,#6366f1)!important;color:#fff!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1.4rem!important;}

/* news card */
.news-card{background:var(--surf2);border:1px solid var(--border);
  border-radius:14px;padding:1.1rem 1.4rem;margin-bottom:.8rem;
  border-left:3px solid var(--accent);transition:border-color .2s,transform .2s;}
.news-card:hover{border-left-color:var(--pink);transform:translateX(3px);}
.nc-title{font-family:'Syne',sans-serif;font-size:.92rem;font-weight:700;
  color:var(--text);margin:0 0 .35rem;}
.nc-meta{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--muted);}
.nc-snippet{font-size:.82rem;color:#94a3b8;margin-top:.45rem;line-height:1.55;}

/* blog */
.blog-wrap{background:var(--surf);border:1px solid var(--border);
  border-radius:18px;padding:2rem 2.4rem;margin-top:.5rem;}
.blog-wrap h1,.blog-wrap h2,.blog-wrap h3{font-family:'Syne',sans-serif;color:var(--text);}
.blog-wrap p{color:#94a3b8;line-height:1.85;}
.blog-wrap strong{color:var(--accent);}

/* pipeline steps */
.pip-step{display:flex;align-items:center;gap:.9rem;padding:.8rem 1rem;
  border-radius:10px;margin-bottom:.45rem;border:1px solid transparent;}
.pip-step.idle{background:var(--surf2);border-color:var(--border);}
.pip-step.active{background:rgba(56,189,248,.1);border-color:rgba(56,189,248,.4);}
.pip-step.done{background:rgba(52,211,153,.07);border-color:rgba(52,211,153,.35);}
.pip-icon{font-size:1.1rem;width:34px;height:34px;display:flex;
  align-items:center;justify-content:center;border-radius:8px;
  background:rgba(255,255,255,.04);}
.pip-label{font-family:'JetBrains Mono',monospace;font-size:.78rem;}

/* email */
.eml-wrap{background:#070a10;border:1px solid var(--border);border-radius:14px;overflow:hidden;}
.eml-head{background:var(--surf2);padding:.9rem 1.4rem;
  border-bottom:1px solid var(--border);
  font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--muted);line-height:1.8;}
.eml-body{padding:1.4rem;color:#94a3b8;font-size:.86rem;line-height:1.75;}

/* metrics */
[data-testid="metric-container"]{background:var(--surf2)!important;
  border:1px solid var(--border)!important;border-radius:14px!important;
  padding:.9rem 1.1rem!important;}
[data-testid="metric-container"] label{font-family:'JetBrains Mono',monospace!important;
  font-size:.68rem!important;color:var(--muted)!important;
  text-transform:uppercase!important;letter-spacing:.1em!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{
  font-family:'Syne',sans-serif!important;font-size:1.7rem!important;
  font-weight:800!important;color:var(--text)!important;}

/* alerts */
.stSuccess{background:rgba(52,211,153,.09)!important;border:1px solid rgba(52,211,153,.35)!important;border-radius:10px!important;}
.stError{background:rgba(244,114,182,.09)!important;border:1px solid rgba(244,114,182,.35)!important;border-radius:10px!important;}
.stInfo{background:rgba(56,189,248,.09)!important;border:1px solid rgba(56,189,248,.3)!important;border-radius:10px!important;}
.stWarning{background:rgba(251,191,36,.09)!important;border:1px solid rgba(251,191,36,.3)!important;border-radius:10px!important;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  MOCK DATA
# ──────────────────────────────────────────────────────────────────────────────
MOCK_SOURCES = ["TechCrunch","MIT Technology Review","The Verge","Wired",
                "VentureBeat","Reuters Technology","Bloomberg Tech","ArsTechnica",
                "ZDNet","InfoQ","Forbes Tech","Business Insider"]

MOCK_ARTICLES = [
    {"title":"OpenAI Launches GPT-5 with Unprecedented Reasoning Capabilities","tag":"LLMs",
     "snippet":"OpenAI unveiled GPT-5, boasting a 40% improvement in complex reasoning benchmarks and a dramatically expanded context window that allows the model to process entire codebases in a single pass."},
    {"title":"Google DeepMind's AlphaFold 3 Predicts Drug Interactions at Atomic Scale","tag":"BioAI",
     "snippet":"DeepMind's latest AlphaFold iteration now predicts not just protein structures but also how small-molecule drugs bind to them, potentially cutting years off the pharmaceutical development pipeline."},
    {"title":"Anthropic Releases Claude 4 with Extended Constitutional AI Framework","tag":"Safety",
     "snippet":"Anthropic's Claude 4 introduces a revamped Constitutional AI training regime that significantly reduces harmful outputs while maintaining competitive performance on coding and reasoning tasks."},
    {"title":"Microsoft Embeds AI Copilot Across Entire Windows 12 Operating System","tag":"Enterprise AI",
     "snippet":"Windows 12 ships with deep OS-level Copilot integration, enabling natural-language control of system settings, file management, and cross-app workflows without any third-party software."},
    {"title":"Meta's LLaMA 4 Goes Fully Open-Source with Multimodal Vision Support","tag":"Open Source",
     "snippet":"Meta AI dropped LLaMA 4 weights publicly, including a vision-language model variant capable of analyzing images, videos, and PDFs — a direct challenge to proprietary closed-source models."},
    {"title":"AI Agents Now Handle 30% of Software Engineering Tasks at Fortune 500 Firms","tag":"Agents",
     "snippet":"A new McKinsey survey reveals that major corporations have integrated autonomous AI coding agents into production workflows, handling bug fixes, documentation, and unit test generation at scale."},
    {"title":"NVIDIA Unveils Blackwell Ultra GPU Architecture Targeting AI Inference","tag":"Hardware",
     "snippet":"NVIDIA's Blackwell Ultra chips deliver 5x the inference throughput of Hopper, with dedicated transformer engines and a new memory subsystem designed specifically for serving large language models."},
    {"title":"EU AI Act Enters Enforcement Phase — Companies Race to Comply","tag":"Regulation",
     "snippet":"With the EU AI Act's high-risk provisions now active, major technology companies are scrambling to audit their AI systems, document training data provenance, and establish internal governance boards."},
    {"title":"Sora 2.0 Generates Photorealistic 4K Video from Text Descriptions","tag":"Generative AI",
     "snippet":"OpenAI's Sora 2.0 can now produce 60-second 4K video clips with consistent physics, lighting, and character continuity — a leap that has Hollywood studios both intrigued and alarmed."},
    {"title":"AI-Powered Drug Discovery Startup Raises $500M Series C","tag":"BioAI",
     "snippet":"Recursion Pharmaceuticals secured half a billion dollars to scale its AI-driven drug discovery platform, which has already identified three promising cancer treatment candidates."},
    {"title":"Stanford Report: AI Systems Now Pass Bar Exam, Medical Boards, and CPA Tests","tag":"Benchmarks",
     "snippet":"A comprehensive Stanford study confirms that the latest generation of AI models consistently score in the top 10th percentile on professional licensing exams across law, medicine, and finance."},
    {"title":"Autonomous AI Research Agents Produce Peer-Reviewed Papers Without Human Input","tag":"Agents",
     "snippet":"A team at CMU demonstrated an AI pipeline that independently formulates hypotheses, runs experiments in simulation, analyzes results, and drafts manuscripts — three of which passed peer review."},
    {"title":"Apple Intelligence 2.0 Brings On-Device LLMs to iPhone and Mac","tag":"LLMs",
     "snippet":"Apple's next-gen on-device AI processes complex tasks entirely locally, ensuring privacy while delivering near-cloud performance for writing assistance, image generation, and smart search."},
    {"title":"China's Baidu Releases ERNIE 5 — Challenges Western AI Dominance","tag":"LLMs",
     "snippet":"Baidu's ERNIE 5 scores competitively against GPT-4 on Chinese-language benchmarks and introduces specialized modules for scientific reasoning and multimodal document understanding."},
    {"title":"AI Coding Assistants Now Write 50% of New Code at GitHub","tag":"Enterprise AI",
     "snippet":"GitHub's annual developer survey reveals that AI-assisted coding tools now contribute to more than half of all new code commits across enterprise repositories on the platform."},
]

BLOG_TEMPLATES = [
    {
        "theme": "The AI Acceleration Era",
        "intro": "The pace of artificial intelligence development has reached a point where weekly headlines feel indistinguishable from science fiction. This week's news cycle brings a fresh wave of breakthroughs that collectively signal one thing: the AI transformation of every industry is no longer a distant forecast — it is happening right now.",
        "sections": [
            {"heading": "Frontier Models Push the Boundaries",
             "body": "The battle between AI labs has intensified dramatically. New model releases are arriving with capabilities that were considered years away just twelve months ago. Reasoning, multimodal understanding, and long-context processing have all seen step-change improvements. What's striking is not just the benchmark numbers, but the qualitative leap — these systems are now genuinely useful for complex, open-ended professional tasks. For enterprises, this means the ROI of AI adoption is compressing from years to months."},
            {"heading": "Autonomous Agents Enter the Workplace",
             "body": "Perhaps the most consequential shift this week is the mainstreaming of AI agents. Where last year's conversation focused on chatbots, today's focus is on systems that autonomously plan, act, and iterate across multi-step workflows. Software engineering, research synthesis, legal document review — these are no longer futuristic use cases. Organizations that deploy agents thoughtfully are already reporting significant productivity gains, while those that ignore this trend risk being structurally disadvantaged."},
            {"heading": "Regulation and Open Source: The Defining Tension",
             "body": "Two forces are pulling the AI ecosystem in opposite directions. On one side, regulatory frameworks — most visibly the EU AI Act — are imposing compliance burdens that favor large, well-resourced incumbents. On the other, the open-source movement continues to democratize access to powerful models, enabling startups and researchers worldwide to innovate without needing billions in compute. How this tension resolves will shape the competitive landscape for the next decade."},
            {"heading": "Hardware: The Invisible Backbone",
             "body": "Behind every model improvement is a hardware story. This week's chip announcements underscore that the AI hardware race is as fierce as the software race. Inference efficiency — the cost of running models at scale — is emerging as the key battleground. As inference costs fall, AI features that were previously too expensive to embed in consumer products become economically viable, creating a virtuous cycle of adoption and investment."},
        ],
        "takeaways": [
            "Frontier model capabilities are advancing faster than most enterprise adoption roadmaps.",
            "AI agents are transitioning from experimental to production-grade across knowledge work.",
            "Open-source and regulatory forces are reshaping competitive dynamics simultaneously.",
            "Hardware improvements are the silent multiplier enabling everything else.",
        ],
        "conclusion": "The through-line across this week's AI news is velocity. The technology is maturing faster than organizations, regulations, and even our conceptual frameworks can keep up with. For leaders, the imperative is clear: build the organizational muscle to continuously learn, adapt, and experiment — because the next wave of breakthroughs is already in the pipeline.",
    },
    {
        "theme": "AI Goes Mainstream",
        "intro": "If last year was about AI's potential, this week's headlines confirm that we have decisively crossed into a new phase: AI is no longer a specialty tool for tech-forward early adopters. It is becoming infrastructure — embedded in operating systems, enterprise workflows, scientific research, and creative industries. The implications are profound and wide-reaching.",
        "sections": [
            {"heading": "From Chatbots to Cognitive Infrastructure",
             "body": "The framing of AI as a 'chatbot' is rapidly becoming obsolete. What we're witnessing is AI becoming part of the cognitive infrastructure of organizations — always-on, deeply integrated, and handling tasks that previously required specialized human expertise. The integration of AI directly into operating systems and productivity suites marks a pivotal moment: for the first time, users don't need to seek out AI tools. AI comes to them."},
            {"heading": "Science Accelerated: AI in Research and Medicine",
             "body": "Some of the most consequential AI applications this week come from science. AI systems predicting drug interactions, generating research hypotheses, and even co-authoring peer-reviewed papers represent a fundamental change in how knowledge is created. The scientific method itself is being augmented. While this raises important questions about verification and reproducibility, the potential to compress drug discovery timelines from decades to years is genuinely historic."},
            {"heading": "The Economics of AI: Investment and Infrastructure",
             "body": "Massive funding rounds and chip announcements this week reveal that the AI economy is operating on a different financial logic than previous tech waves. Capital is flowing not just into applications but into foundational infrastructure — compute, data, and specialized models. This infrastructure buildout is creating a new industrial complex that will determine which companies and nations lead in AI for decades."},
            {"heading": "Creative Industries at an Inflection Point",
             "body": "Generative AI advances in video, audio, and image synthesis are forcing creative industries to reckon with fundamental questions about authorship, originality, and labor. The technology is powerful enough to produce professional-quality output — which means the conversation has shifted from 'can it?' to 'should it, and under what terms?' The creative economy's response to this moment will define new norms for the next generation."},
        ],
        "takeaways": [
            "AI is transitioning from a specialized tool to embedded cognitive infrastructure.",
            "Scientific and medical AI applications represent some of the highest-impact use cases.",
            "Capital flowing into AI infrastructure signals decade-long structural investment.",
            "Creative industries face urgent questions about AI's role in professional work.",
        ],
        "conclusion": "Mainstream AI adoption is not a future event — it is the present reality. The organizations and individuals who thrive will be those who engage seriously with both the opportunities AI unlocks and the disruptions it demands. The window for thoughtful, strategic adoption is open now. The question is who walks through it.",
    },
]

# ──────────────────────────────────────────────────────────────────────────────
#  ENGINE (zero external calls)
# ──────────────────────────────────────────────────────────────────────────────

def fetch_mock_news(query: str, num: int, category: str) -> list:
    pool = [a for a in MOCK_ARTICLES if category == "All AI" or a["tag"] == category]
    if not pool:
        pool = MOCK_ARTICLES.copy()
    random.shuffle(pool)
    result = []
    base = datetime.now()
    for art in pool[:num]:
        d = base - timedelta(hours=random.randint(0, 36))
        result.append({
            "title":   art["title"],
            "source":  random.choice(MOCK_SOURCES),
            "date":    d.strftime("%b %d, %Y · %I:%M %p"),
            "snippet": art["snippet"],
            "tag":     art["tag"],
        })
    return result


def generate_blog(articles: list, tone: str, audience: str, author: str) -> tuple:
    tmpl  = random.choice(BLOG_TEMPLATES)
    today = datetime.now().strftime("%B %d, %Y")
    tags  = list({a["tag"] for a in articles})[:4]

    # ── Markdown ──
    md  = f"# {tmpl['theme']}: Weekly AI Digest\n\n"
    md += f"*By {author} · {today} · {tone.title()} Edition*\n\n---\n\n"
    md += f"## Overview\n\n{tmpl['intro']}\n\n"
    for i, sec in enumerate(tmpl["sections"]):
        md += f"## {sec['heading']}\n\n{sec['body']}\n\n"
        if i < len(articles):
            art = articles[i]
            md += f"> 📰 **In the news:** *{art['title']}* — {art['source']}\n"
            md += f"> {art['snippet']}\n\n"
    md += "## Key Takeaways\n\n"
    for tk in tmpl["takeaways"]:
        md += f"- **{tk}**\n"
    md += f"\n## Looking Ahead\n\n{tmpl['conclusion']}\n\n---\n\n"
    md += f"*Tags: {' · '.join('#'+t for t in tags)}*\n\n"
    md += f"*Generated by AI News Auto-Blogger · {today}*\n"

    # ── HTML for email ──
    secs_html = ""
    for i, sec in enumerate(tmpl["sections"]):
        secs_html += f"""
        <h2 style="font-family:Georgia,serif;font-size:18px;color:#e2e8f0;
                   border-left:3px solid #38bdf8;padding-left:12px;margin:28px 0 10px;">
          {sec['heading']}</h2>
        <p style="color:#94a3b8;line-height:1.8;font-size:14px;">{sec['body']}</p>"""
        if i < len(articles):
            art = articles[i]
            secs_html += f"""
        <div style="background:#111827;border-left:3px solid #818cf8;border-radius:6px;
                    padding:12px 16px;margin:12px 0;">
          <div style="font-size:11px;color:#6366f1;font-family:monospace;margin-bottom:4px;">
            📰 IN THE NEWS · {art['source']}</div>
          <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">{art['title']}</div>
          <div style="font-size:12px;color:#64748b;">{art['snippet']}</div>
        </div>"""

    tks_html = "".join(
        f'<li style="color:#94a3b8;margin:6px 0;font-size:14px;">'
        f'<strong style="color:#38bdf8;">{tk}</strong></li>'
        for tk in tmpl["takeaways"]
    )

    html = f"""
<div style="font-family:'Helvetica Neue',Arial,sans-serif;max-width:640px;margin:0 auto;">
  <div style="background:linear-gradient(135deg,#0e1220,#0a1128);border-radius:16px;
              padding:32px;margin-bottom:20px;text-align:center;border:1px solid #1e2438;">
    <div style="font-size:11px;color:#34d399;letter-spacing:.15em;font-family:monospace;margin-bottom:8px;">
      🤖 AI NEWS AUTO-BLOGGER</div>
    <h1 style="font-family:Georgia,serif;font-size:26px;font-weight:700;color:#fff;margin:0 0 8px;">
      {tmpl['theme']}</h1>
    <div style="font-size:11px;color:#475569;font-family:monospace;">{today} · {author}</div>
  </div>
  <div style="background:#0e1220;border:1px solid #1e2438;border-radius:12px;padding:24px;margin-bottom:16px;">
    <p style="color:#94a3b8;font-size:15px;line-height:1.8;margin:0;">{tmpl['intro']}</p>
  </div>
  <div style="background:#0e1220;border:1px solid #1e2438;border-radius:12px;padding:24px;margin-bottom:16px;">
    {secs_html}
  </div>
  <div style="background:#0e1220;border:1px solid #1e2438;border-radius:12px;padding:24px;margin-bottom:16px;">
    <h2 style="font-family:Georgia,serif;color:#e2e8f0;font-size:17px;margin:0 0 14px;">⚡ Key Takeaways</h2>
    <ul style="margin:0;padding-left:20px;">{tks_html}</ul>
  </div>
  <div style="background:#0e1220;border:1px solid #1e2438;border-radius:12px;padding:24px;margin-bottom:16px;">
    <h2 style="font-family:Georgia,serif;color:#e2e8f0;font-size:17px;margin:0 0 10px;">🔭 Looking Ahead</h2>
    <p style="color:#94a3b8;font-size:14px;line-height:1.8;margin:0;">{tmpl['conclusion']}</p>
  </div>
  <div style="text-align:center;padding:16px;color:#334155;font-size:11px;font-family:monospace;">
    Generated by AI News Auto-Blogger · {today}
  </div>
</div>"""

    return md, html


def simulate_email(to: str, subject: str) -> dict:
    return {
        "to": to, "subject": subject,
        "message_id": f"<{random.randint(10**9,10**10)}.{random.randint(100,999)}@mail.ai-blogger.demo>",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "status": "delivered",
        "server": "smtp.mail.ai-blogger.demo:465",
        "size_kb": round(random.uniform(18, 42), 1),
    }

# ──────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ──────────────────────────────────────────────────────────────────────────────
defaults = {"articles":[],"blog_md":"","blog_html":"","receipt":None,"step":0,"runs":0,"last_run":None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.05rem;
    font-weight:800;color:#e2e8f0;margin-bottom:4px;">⚙️ Settings</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:.68rem;
    color:#64748b;margin-bottom:1.4rem;">Configure pipeline preferences</div>""",
    unsafe_allow_html=True)

    with st.expander("📰 News Settings", expanded=True):
        num_articles = st.slider("Articles to generate", 4, 12, 8)
        category = st.selectbox("AI Category", [
            "All AI","LLMs","Agents","Safety","Hardware","Open Source",
            "Regulation","BioAI","Generative AI","Enterprise AI","Benchmarks"])
        news_query = st.text_input("Search Topic", value="artificial intelligence 2025")

    with st.expander("📝 Blog Settings"):
        tone = st.selectbox("Writing Tone", [
            "insightful and analytical","engaging and accessible",
            "technical and precise","enthusiastic and forward-looking"])
        audience = st.selectbox("Target Audience", [
            "tech professionals","business executives",
            "general enthusiasts","AI researchers"])
        author = st.text_input("Author Name", value="AI News Bot")

    with st.expander("📧 Email Settings"):
        recipient = st.text_input("Send To (demo)", value="you@example.com")
        subject   = st.text_input("Subject", value=f"🤖 AI Digest — {datetime.now().strftime('%b %d, %Y')}")

    st.markdown("---")

    # pipeline steps sidebar
    steps_cfg = [("🌐","Fetch News",1),("🔍","Filter Articles",2),
                 ("🧠","LLM Processing",3),("📝","Blog Generation",3),("📧","Email Delivery",4)]
    st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:.68rem;"
                "color:#64748b;text-transform:uppercase;letter-spacing:.1em;"
                "margin-bottom:.7rem;'>Pipeline Status</div>", unsafe_allow_html=True)
    for icon, label, snum in steps_cfg:
        cur = st.session_state.step
        if cur == snum:              state,badge,col = "active","⏳","#38bdf8"
        elif cur > snum or cur==5:   state,badge,col = "done","✓","#34d399"
        else:                        state,badge,col = "idle","·","#64748b"
        st.markdown(f"""<div class="pip-step {state}">
          <div class="pip-icon">{icon}</div>
          <div><div class="pip-label" style="color:{col};">{label}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#334155;">{badge}</div>
          </div></div>""", unsafe_allow_html=True)

    if st.session_state.last_run:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:.65rem;"
                    f"color:#334155;margin-top:.8rem;'>Last: {st.session_state.last_run}</div>",
                    unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero">
  <div class="hero-title">AI News<br/>Auto-Blogger</div>
  <div class="hero-sub">⚡ FETCH → FILTER → GENERATE → DELIVER</div>
  <div style="margin-top:1rem;">
    <span class="badge">No API Required</span>
    <span class="badge">Mock News Engine</span>
    <span class="badge">Blog Generator</span>
    <span class="badge">Email Simulator</span>
    <span class="badge">n8n Architecture</span>
  </div>
</div>""", unsafe_allow_html=True)

m1,m2,m3,m4 = st.columns(4)
m1.metric("Articles Loaded",  len(st.session_state.articles) or "—")
m2.metric("Blog Generated",   "✓ Yes" if st.session_state.blog_md else "No")
m3.metric("Email Sent",       "✓ Sent" if st.session_state.receipt else "Pending")
m4.metric("Total Runs",       st.session_state.runs)
st.markdown("")

t1,t2,t3,t4 = st.tabs(["🚀 Pipeline","📰 News Feed","📝 Blog Post","📧 Email Preview"])

# ── TAB 1 ──────────────────────────────────────────────────────────────────
with t1:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.05rem;
    font-weight:700;color:#e2e8f0;margin-bottom:.25rem;">Automation Pipeline</div>
    <div style="font-size:.83rem;color:#64748b;margin-bottom:1.3rem;">
    One click runs the full workflow. Zero API keys — fully simulated for project demo.</div>""",
    unsafe_allow_html=True)

    ca,cb = st.columns([2,1])
    with ca: run_all = st.button("▶  Run Full Pipeline", use_container_width=True)
    with cb: reset   = st.button("↺  Reset",             use_container_width=True)

    if reset:
        for k,v in defaults.items(): st.session_state[k]=v
        st.rerun()

    if run_all:
        prog = st.empty(); bar = st.progress(0)
        try:
            st.session_state.step=1
            with prog.container(): st.info("🌐 Step 1/4 — Fetching AI news headlines...")
            bar.progress(10); time.sleep(0.6)
            articles = fetch_mock_news(news_query, num_articles, category)
            bar.progress(25); time.sleep(0.3)

            st.session_state.step=2
            with prog.container(): st.info(f"🔍 Step 2/4 — Filtering {len(articles)} articles...")
            bar.progress(40); time.sleep(0.5)
            st.session_state.articles = articles

            st.session_state.step=3
            with prog.container(): st.info("🧠 Step 3/4 — LLM generating blog post...")
            bar.progress(60); time.sleep(0.8)
            md,html = generate_blog(articles, tone, audience, author)
            st.session_state.blog_md=md; st.session_state.blog_html=html
            bar.progress(80)

            st.session_state.step=4
            with prog.container(): st.info("📧 Step 4/4 — Dispatching email digest...")
            time.sleep(0.5)
            st.session_state.receipt = simulate_email(recipient, subject)
            bar.progress(100); time.sleep(0.2)

            st.session_state.step=5; st.session_state.runs+=1
            st.session_state.last_run=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prog.empty(); bar.empty()
            st.success(f"✅ Pipeline complete! {len(articles)} articles → blog generated → email dispatched to **{recipient}**")
            st.balloons()
        except Exception as e:
            st.session_state.step=0; prog.empty(); bar.empty()
            st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:.7rem;"
                "color:#334155;margin-bottom:.8rem;'>INDIVIDUAL STEPS</div>",
                unsafe_allow_html=True)
    r1,r2,r3 = st.columns(3)
    with r1:
        if st.button("🌐 Fetch News Only", use_container_width=True):
            with st.spinner("Fetching..."):
                time.sleep(0.5)
                st.session_state.articles = fetch_mock_news(news_query, num_articles, category)
            st.success(f"✓ {len(st.session_state.articles)} articles loaded")
    with r2:
        if st.button("🧠 Generate Blog Only", use_container_width=True):
            if not st.session_state.articles: st.warning("Fetch news first!")
            else:
                with st.spinner("Generating..."): time.sleep(0.7)
                md,html = generate_blog(st.session_state.articles, tone, audience, author)
                st.session_state.blog_md=md; st.session_state.blog_html=html
                st.success("✓ Blog generated!")
    with r3:
        if st.button("📧 Simulate Email Only", use_container_width=True):
            if not st.session_state.blog_md: st.warning("Generate blog first!")
            else:
                with st.spinner("Sending..."): time.sleep(0.5)
                st.session_state.receipt = simulate_email(recipient, subject)
                st.success("✓ Email simulated!")

    st.markdown("---")
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;
    color:#64748b;margin-bottom:.8rem;text-transform:uppercase;letter-spacing:.08em;">
    n8n Workflow Architecture</div>
    <div style="background:#0e1220;border:1px solid #1e2438;border-radius:14px;
    padding:1.5rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#64748b;line-height:2.2;">
      <span style="color:#38bdf8;">[ Cron Trigger ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#818cf8;">[ News API / Mock Engine ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#f472b6;">[ AI Keyword Filter ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#34d399;">[ LLM Agent (Groq / OpenAI) ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#fbbf24;">[ Blog Generator ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#38bdf8;">[ Email Formatter ]</span><br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>
      <span style="color:#e2e8f0;">[ Gmail / SMTP Delivery ]</span>
    </div>""", unsafe_allow_html=True)

# ── TAB 2 ──────────────────────────────────────────────────────────────────
with t2:
    if not st.session_state.articles:
        st.info("Run the pipeline or click 'Fetch News Only' to load articles.")
    else:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;"
                    f"color:#34d399;margin-bottom:1rem;'>✓ {len(st.session_state.articles)} ARTICLES LOADED</div>",
                    unsafe_allow_html=True)
        for art in st.session_state.articles:
            st.markdown(f"""<div class="news-card">
              <div class="nc-title">{art['title']}</div>
              <div class="nc-meta">📰 {art['source']} &nbsp;·&nbsp; 🕒 {art['date']}
                &nbsp;·&nbsp;
                <span style="background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.25);
                border-radius:10px;padding:1px 8px;color:#38bdf8;font-size:.65rem;">{art['tag']}</span>
              </div>
              <div class="nc-snippet">{art['snippet']}</div>
            </div>""", unsafe_allow_html=True)

# ── TAB 3 ──────────────────────────────────────────────────────────────────
with t3:
    if not st.session_state.blog_md:
        st.info("Generate a blog post by running the pipeline or clicking 'Generate Blog Only'.")
    else:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;"
                    "color:#34d399;margin-bottom:.8rem;'>✓ BLOG POST GENERATED</div>",
                    unsafe_allow_html=True)
        _,dl = st.columns([4,1])
        with dl:
            st.download_button("⬇ .md", st.session_state.blog_md,
                               file_name="ai_blog.md", mime="text/markdown",
                               use_container_width=True)
        st.markdown('<div class="blog-wrap">', unsafe_allow_html=True)
        st.markdown(st.session_state.blog_md)
        st.markdown('</div>', unsafe_allow_html=True)
        with st.expander("📋 Raw Markdown"):
            st.code(st.session_state.blog_md, language="markdown")

# ── TAB 4 ──────────────────────────────────────────────────────────────────
with t4:
    if not st.session_state.blog_html:
        st.info("Generate a blog post first to preview the email.")
    else:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;"
                    "color:#34d399;margin-bottom:.8rem;'>📧 EMAIL PREVIEW</div>",
                    unsafe_allow_html=True)
        if st.session_state.receipt:
            r = st.session_state.receipt
            rc1,rc2,rc3 = st.columns(3)
            rc1.metric("Status","✓ Delivered")
            rc2.metric("Size",f"{r['size_kb']} KB")
            rc3.metric("Sent At", r['timestamp'].split()[1])
            st.markdown("")

        st.markdown(f"""<div class="eml-wrap">
          <div class="eml-head">
            <b>From:</b> AI News Blogger &lt;noreply@ai-blogger.demo&gt;<br/>
            <b>To:</b> {recipient}<br/>
            <b>Subject:</b> {subject}<br/>
            <b>Date:</b> {datetime.now().strftime("%a, %d %b %Y %H:%M:%S UTC")}
          </div>
          <div class="eml-body">
            {st.session_state.blog_html[:1400]}{'...' if len(st.session_state.blog_html)>1400 else ''}
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("")
        st.download_button("⬇ Download HTML Email", st.session_state.blog_html,
                           file_name="email.html", mime="text/html")

        if st.session_state.receipt:
            with st.expander("📋 Delivery Receipt"):
                r = st.session_state.receipt
                st.code(
                    f"Message-ID : {r['message_id']}\n"
                    f"To         : {r['to']}\n"
                    f"Subject    : {r['subject']}\n"
                    f"Timestamp  : {r['timestamp']}\n"
                    f"Status     : {r['status'].upper()}\n"
                    f"Server     : {r['server']}\n"
                    f"Size       : {r['size_kb']} KB",
                    language="text")

"""Intelligent Retrieval-Augmented Generation (RAG) Engine for Saral Samjhauti & Research Funding."""
import logging
import re
from typing import Any, Dict, List, Optional, Tuple
from rank_bm25 import BM25Okapi

from src.ai.llm_adapter import LLMSynthesisAdapter
from src.ai.session_store import ConversationalMemoryStore
from src.config import RRF_K_CONSTANT
from src.embeddings.embedder import TextEmbedder
from src.embeddings.hybrid_search import tokenize_text
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import RAGCitation, RAGChatRequest, RAGChatResponse

logger = logging.getLogger("MadadgaarAI.AI.RAG")


STATUTORY_POLICY_CORPUS: List[Dict[str, str]] = [
    {
        "doc_id": "POLICY-NPCI-DBT-01",
        "title": "Aadhaar Bank Seeding & NPCI Direct Benefit Transfer (DBT) Mapper Guidelines",
        "authority": "UIDAI / National Payments Corporation of India (NPCI) / PFMS",
        "official_url": "https://www.npci.org.in",
        "en_content": (
            "All Central (NSP, AICTE, UGC) and State (UP Dashmottar, MahaDBT) scholarships are disbursed exclusively via the "
            "Public Financial Management System (PFMS) using the Aadhaar Payment Bridge (APB). "
            "CRITICAL DISTINCTION: Simply linking Aadhaar KYC to a bank account is NOT sufficient. The student's savings bank account "
            "must be seeded on the NPCI Direct Benefit Transfer (DBT) Mapper. "
            "How to Enable: Visit your home bank branch with your Aadhaar card and passbook, and submit the physical 'NPCI Aadhaar Seeding / DBT Mandate Form'. "
            "How to Verify: Log in to myaadhaar.uidai.gov.in -> click 'Bank Seeding Status' to confirm Mapping Status is 'Active'. "
            "Ensure the account is a regular active savings account in the student's own name without a low-value transaction cap."
        ),
        "hinglish_content": (
            "Aadhaar Seeding aur NPCI DBT Mapping kya hai? "
            "Sabhi sarkari scholarships (NSP, AICTE Pragati, UP Scholarship, MahaDBT) ka paisa PFMS ke zariye seedhe Aadhaar-linked bank account mein aata hai. "
            "Dhyan dein: Bank mein sirf Aadhaar KYC hona kaafi NAHI hai! Aapka bank khata NPCI Server (DBT Mapper) par active hona zaruri hai. "
            "Kaise karwayein: Apni bank branch jayein, Aadhaar card ki copy dein aur 'NPCI Aadhaar Seeding / DBT Mandate Form' jama karein. "
            "Kaise check karein: myaadhaar.uidai.gov.in par login karke 'Bank Seeding Status' check karein — wahan status 'Active' dikhna chahiye."
        ),
    },
    {
        "doc_id": "POLICY-INCOME-CERT-02",
        "title": "Income Certificate (आय प्रमाण पत्र) Issuing Authority & Financial Year Validity Rules",
        "authority": "State Revenue Department / e-District / Tehsildar Office",
        "official_url": "https://scholarships.gov.in",
        "en_content": (
            "An Income Certificate (Aay Praman Patra) certifies the annual gross family income from all sources (salary, agriculture, business, pension). "
            "Issuing Authority: Must be issued by a competent revenue officer — Tehsildar, Naib Tehsildar, Sub-Divisional Magistrate (SDM), or State e-District Portal with a verifiable digital QR code/barcode. "
            "Validity Rule: Because family income fluctuates annually, portals require an Income Certificate issued on or after 1st April of the current financial year. "
            "Whose Name: On UP Scholarship and several state portals, the Income Certificate must be issued in the name of the earning parent/head of family (Father/Mother/Guardian), accurately reflecting combined household income."
        ),
        "hinglish_content": (
            "Income Certificate (आय प्रमाण पत्र) ke zaruri niyam: "
            "1. Kaun jari karta hai: Tehsildar, Naib Tehsildar, ya SDM (State e-District / CSC / E-Mitra portal se digital signature aur QR code wala). "
            "2. Validity: Income certificate chalu vittiy varsh (1 April ke baad) ka bana hona chahiye. Purana certificate lagane par form reject ho sakta hai. "
            "3. Kiske naam par: माता-पिता (Parents/Guardian) ki kul varshik aay (Gross Family Income) darshane wala certificate hona chahiye."
        ),
    },
    {
        "doc_id": "POLICY-CASTE-EWS-03",
        "title": "Caste Certificate (SC/ST/OBC-NCL) & EWS Certificate Statutory Norms",
        "authority": "Ministry of Social Justice & Empowerment / DoPT, Govt. of India",
        "official_url": "https://socialjustice.gov.in",
        "en_content": (
            "Caste and Category Certificates verify reservation eligibility: "
            "1. SC / ST Certificates: Carry lifetime validity if issued by a Tehsildar/SDM/District Magistrate in the student's own name. "
            "2. OBC (Non-Creamy Layer - NCL): Must explicitly certify that the family does not belong to the Creamy Layer (annual parental income < ₹8.0 Lakhs, excluding salary/agricultural rules per DoPT). Must be renewed for the current financial year for central schemes. "
            "3. EWS (Economically Weaker Section): For General category students whose family annual income is below ₹8.0 Lakhs and who meet residential/agricultural land asset limits; valid for 1 financial year (issued after April 1)."
        ),
        "hinglish_content": (
            "Caste (जाति) aur EWS Certificate ke niyam: "
            "• SC / ST Certificate: Ek baar Tehsildar/SDM se banne ke baad lifetime valid hota hai. "
            "• OBC-NCL (Non-Creamy Layer): Ismein 'Non-Creamy Layer' likha hona zaruri hai aur naye financial year (1 April ke baad) ka hona chahiye. "
            "• EWS Certificate: General category ke un students ke liye jinki family income ₹8 Lakh se kam hai; yeh har saal 1 April ke baad naya banta hai."
        ),
    },
    {
        "doc_id": "POLICY-DOMICILE-04",
        "title": "Domicile / Permanent Residence Certificate (मूल निवास प्रमाण पत्र) Guidelines",
        "authority": "State Revenue Administration / District Magistrate",
        "official_url": "https://scholarships.gov.in",
        "en_content": (
            "A Domicile or Permanent Residence Certificate (Niwas / PRC) proves a student's permanent resident status in a particular Indian State or Union Territory. "
            "It is mandatory for state-funded portals (such as UP Dashmottar Scholarship for Uttar Pradesh residents, MahaDBT Rajarshi Shahu Maharaj EBC for Maharashtra residents, and UGC Ishan Uday PRC for North-Eastern Region students). "
            "Issued by the Tehsildar, SDM, or District Magistrate via the state e-District portal."
        ),
        "hinglish_content": (
            "Domicile / Niwas Praman Patra (मूल निवास प्रमाण पत्र): "
            "Yeh pramanit karta hai ki aap kis rajya (State) ke sthayi nivasi hain. State scholarships (jaise UP Dashmottar, Maharashtra MahaDBT, ya North-East ke liye UGC Ishan Uday) mein usi state ka Domicile/PRC lagana anivarya hai."
        ),
    },
    {
        "doc_id": "POLICY-NSP-OTR-05",
        "title": "National Scholarship Portal (NSP) One Time Registration (OTR) & Face Authentication",
        "authority": "National Scholarship Portal (NSP), Ministry of Electronics & IT (MeitY)",
        "official_url": "https://scholarships.gov.in",
        "en_content": (
            "One Time Registration (OTR) is a unique 14-digit permanent ID assigned to every student on the National Scholarship Portal (scholarships.gov.in) valid across their entire academic career. "
            "Steps to Complete OTR: "
            "1. Register on scholarships.gov.in using Aadhaar-linked mobile OTP to receive a Reference ID. "
            "2. Download the 'AadhaarFaceRD' app and 'NSP OTR' app from Google Play Store. "
            "3. Complete live Face Authentication e-KYC to generate your 14-digit OTR ID and password. "
            "WARNING: Never generate more than one OTR ID; duplicate OTR registrations lead to automatic debarment."
        ),
        "hinglish_content": (
            "NSP OTR (One Time Registration) aur Face Authentication kaise karein? "
            "1. scholarships.gov.in par जाकर Aadhaar-linked mobile number se OTR Reference Number banayein. "
            "2. Mobile mein Google Play Store se 'AadhaarFaceRD' aur 'NSP OTR' app install karein. "
            "3. App mein apna chehra (Face Authentication) scan karke e-KYC poora karein, jisse 14-digit OTR ID SMS par mil jayegi. "
            "Savdhan: Ek student sirf EK hi OTR ID banaye, doosra OTR banane par form reject ho jata hai."
        ),
    },
    {
        "doc_id": "POLICY-REJECTION-06",
        "title": "Common Scholarship Application Rejection Reasons & How to Prevent Them",
        "authority": "PFMS / NSP / State Nodal Verification Guidelines",
        "official_url": "https://scholarships.gov.in",
        "en_content": (
            "Top 7 Reasons Why Scholarship Applications Get Rejected: "
            "1. Inactive NPCI/DBT Mapping: Bank account is not seeded on NPCI mapper, causing PFMS payment failure. "
            "2. Expired Income/EWS/OBC-NCL Certificate: Uploading a certificate issued prior to 1st April of the current financial year. "
            "3. Missed Institute Nodal Officer (INO) Verification: Submitting online but failing to submit hard copies to the college scholarship desk before the INO verification deadline. "
            "4. Duplicate Portal Application: Applying on both a State Portal (e.g., UP/MahaDBT) and Central NSP in the same academic year. "
            "5. Name / DOB Mismatch: Spelling differences between Aadhaar Card, Class 10th Marksheet, and Caste/Income Certificate. "
            "6. Non-CAP / Management Quota Admission: State fee reimbursement schemes (like MahaDBT EBC and UP Dashmottar) require admission through official Counseling/CAP rounds. "
            "7. Saving Draft Without Final Lock: Printing the draft check copy without clicking 'Final Submit'."
        ),
        "hinglish_content": (
            "Scholarship Form Reject hone ke 7 sabse bade kaaran (In galatiyon se bachein): "
            "1. Bank khate mein NPCI DBT Seeding active na hona (PFMS Reject). "
            "2. 1 April se pehle ka purana Income / OBC-NCL / EWS certificate upload karna. "
            "3. Online form bharne ke baad College Nodal Officer (INO) se verify na karwana. "
            "4. Ek hi saal mein State Portal aur Central NSP dono par form bhar dena (Duplicate Rejection). "
            "5. Aadhaar, 10th Marksheet aur Certificate mein naam ya DOB ki spelling alag hona. "
            "6. Management Quota se admission hona (jabki scheme mein Counseling/CAP round zaruri ho). "
            "7. Draft print nikal kar 'Final Submit / Lock' button na dabana."
        ),
    },
    {
        "doc_id": "POLICY-RENEWAL-07",
        "title": "Scholarship Annual Renewal & Continuation Rules",
        "authority": "UGC / AICTE / Ministry of Education Statutory Guidelines",
        "official_url": "https://scholarships.gov.in",
        "en_content": (
            "To continue receiving multi-year scholarships (such as PM-USP, AICTE Pragati/Saksham, Kotak Kanya, UGC Single Girl Child, or DST INSPIRE), students must apply under the 'Renewal' category every year: "
            "1. Minimum Academic Performance: Must pass all subjects with zero backlogs (ATKT) and maintain at least 50%–60% aggregate marks (or >= 6.0 CGPA; >= 7.5 CGPA for Kotak Kanya). "
            "2. Attendance Requirement: Minimum 75% regular attendance certified by the Head of Institution. "
            "3. Continuous Renewal Rule: On NSP, if a student misses applying for renewal in any single intermediate year, the scholarship lapses permanently."
        ),
        "hinglish_content": (
            "Scholarship Renewal (नवीनीकरण) kaise hota hai? "
            "• Har saal agle semester/year mein jane par portal par 'Fresh' ki jagah 'Renewal' mein login karein. "
            "• Pichhle saal ki marksheet (bina kisi backlog/fail paper ke, 50%–60%+ marks ke sath) aur current year ki fee receipt/bonafide upload karein. "
            "• Dhyan rahe: Agar beech mein ek bhi saal Renewal chhoot gaya, to aage ke saalon mein scholarship band ho jati hai."
        ),
    },
    {
        "doc_id": "POLICY-GFR-MOE-08",
        "title": "Ministry of Finance GFR 2017 & DST/ANRF/CSIR Extramural Research Grant Norms",
        "authority": "Ministry of Finance & Department of Science and Technology (DST), Govt. of India",
        "official_url": "https://dst.gov.in",
        "en_content": (
            "Key Statutory Rules for Faculty & Research Grant Proposals (DST, ANRF/SERB, CSIR, DBT): "
            "1. Revised Research Fellowship Emoluments (DST OM): Junior Research Fellow (JRF) = ₹37,000/month + HRA (Years 1–2); Senior Research Fellow (SRF) = ₹42,000/month + HRA (Years 3–5); Research Associate (RA-I/II/III) = ₹58,000 to ₹67,000/month + HRA. "
            "2. Capital Equipment Procurement: Items costing above ₹5.0 Lakhs require 3 competitive proforma quotations or Government e-Marketplace (GeM) comparison. "
            "3. Institutional Overheads: Typically capped at 8% to 12.5% of total project cost per scheme guidelines. "
            "4. Annual Release & GFR 12-A: Subsequent annual grant installments require an audited Utilization Certificate (UC) in Form GFR 12-A and Statement of Expenditure (SE) via PFMS EAT module."
        ),
        "hinglish_content": (
            "Faculty Research Grants (DST, ANRF, CSIR, DBT) ke mukhya niyam: "
            "• Revised Fellowship Rates: JRF ko ₹37,000/month + HRA aur SRF ko ₹42,000/month + HRA milta hai. "
            "• Equipment Quotations: ₹5 Lakh se adhik ke har equipment ke liye GeM rate ya 3 vendor quotations lagana zaruri hai. "
            "• GFR 12-A Utilization Certificate: Har saal agli kist (installment) ke liye audited UC aur Statement of Expenditure (SE) jama karna hota hai."
        ),
    },
]


class SaralSamjhautiRAG:
    """Hybrid BM25 + Dense Vector + RRF + Semantic Reranking RAG Engine with Bilingual Grounding.

    Architecture & Guardrails:
    1. Dual-Corpus Indexing:
       - Statutory policy database (NPCI-DBT mapping, renewal rules, GFR 2017 norms, income certificates).
       - Live and parsed funding opportunities database from national statutory portals.
    2. Hybrid Dense-Sparse RRF Retrieval:
       - Reciprocal Rank Fusion ($k=60$) over BM25 and 384-dimensional dense semantic embeddings.
    3. Strict Grounding & Anti-Hallucination:
       - Verified citations with official government authority, issuing ministry, and portal URLs.
       - Conversational multi-turn context retention per session.
    4. Bilingual Generation:
       - Seamless toggle between formal English and conversational Hinglish explainers.
    """

    def __init__(
        self,
        normalizer: Optional[DatasetNormalizer] = None,
        session_store: Optional[ConversationalMemoryStore] = None,
        embedder: Optional[TextEmbedder] = None,
        llm_adapter: Optional[LLMSynthesisAdapter] = None,
    ):
        self.normalizer = normalizer or DatasetNormalizer()
        self.session_store = session_store or ConversationalMemoryStore()
        self.embedder = embedder or TextEmbedder()
        self.llm_adapter = llm_adapter or LLMSynthesisAdapter()
        self.kb_items: List[Dict[str, Any]] = []
        self.bm25: Optional[BM25Okapi] = None
        self.dense_vectors: List[List[float]] = []
        self.rebuild_knowledge_base()

    def rebuild_knowledge_base(self):
        """Indexes both statutory policy documents and all active scholarship/grant opportunities."""
        self.kb_items = []
        corpus_tokens: List[List[str]] = []
        texts_to_embed: List[str] = []

        # 1. Add statutory policy documents
        for pol in STATUTORY_POLICY_CORPUS:
            combined_text = f"{pol['title']} {pol['authority']} {pol['en_content']} {pol['hinglish_content']}"
            self.kb_items.append(
                {
                    "source_id": pol["doc_id"],
                    "kind": "policy",
                    "title": pol["title"],
                    "authority": pol["authority"],
                    "official_url": pol["official_url"],
                    "en_summary": pol["en_content"],
                    "hinglish_summary": pol["hinglish_content"],
                    "raw_text": combined_text,
                }
            )
            corpus_tokens.append(tokenize_text(combined_text))
            texts_to_embed.append(combined_text)

        # 2. Add all indexed FundingOpportunities
        opportunities = self.normalizer.load_all_opportunities()
        for foa in opportunities:
            elig_text = foa.eligibility.raw_eligibility_text or foa.eligibility.min_qualification or ""
            budget_text = foa.financials.raw_budget_text or f"Up to ₹{foa.financials.max_amount_inr or 0:,.0f}"
            deadline_text = (
                foa.deadlines.effective_deadline.isoformat()
                if foa.deadlines.effective_deadline
                else "Rolling Call"
            )
            renewal_text = foa.renewal_requirements or "Annual academic continuation required."
            mistakes_text = " ".join(foa.common_mistakes[:3]) if foa.common_mistakes else ""

            en_summary = (
                f"{foa.title} ({foa.foa_id}) issued by {foa.issuing_authority or foa.agency.value}. "
                f"Financial Benefit: {budget_text}. Eligibility: {elig_text}. "
                f"Closing Date: {deadline_text}. Renewal: {renewal_text}"
            )
            hinglish_summary = (
                f"{foa.title} ({foa.agency.value}): आर्थिक सहायता: {budget_text}। "
                f"पात्रता (Eligibility): {elig_text}। अंतिम तिथि (Deadline): {deadline_text}। "
                f"ऑफिशियल पोर्टल: {foa.direct_apply_url or foa.source_url}"
            )
            combined_text = (
                f"{foa.foa_id} {foa.title} {foa.scheme_name or ''} {foa.agency.value} "
                f"{foa.issuing_authority or ''} {foa.brief_summary} {' '.join(foa.thematic_areas)} "
                f"{elig_text} {budget_text} {renewal_text} {mistakes_text}"
            )

            self.kb_items.append(
                {
                    "source_id": foa.foa_id,
                    "kind": "opportunity",
                    "title": foa.title,
                    "authority": foa.issuing_authority or foa.agency.value,
                    "official_url": foa.direct_apply_url or foa.source_url,
                    "en_summary": en_summary,
                    "hinglish_summary": hinglish_summary,
                    "raw_text": combined_text,
                    "foa": foa,
                }
            )
            corpus_tokens.append(tokenize_text(combined_text))
            texts_to_embed.append(combined_text)

        if corpus_tokens:
            self.bm25 = BM25Okapi(corpus_tokens)
            self.dense_vectors = self.embedder.embed_batch(texts_to_embed)

    @staticmethod
    def detect_language(query: str, requested_lang: str = "auto") -> str:
        if requested_lang in ("en", "english"):
            return "en"
        if requested_lang in ("hinglish", "hi", "hindi"):
            return "hinglish"

        # Auto-detect Devanagari script or common Hinglish conversational tokens
        if re.search(r"[\u0900-\u097F]", query):
            return "hinglish"
        hinglish_markers = {
            "kya", "kaise", "kitna", "kitne", "milega", "milenge", "kab", "kyu",
            "kyon", "kaun", "kahan", "paise", "paisa", "chahiye", "banwaye",
            "banega", "mera", "meri", "hai", "hain", "ke", "ki", "ko", "mein",
            "se", "aur", "batao", "bataiye", "madad", "saral", "samjhao", "galati",
        }
        tokens = set(re.findall(r"[a-zA-Z]+", query.lower()))
        if len(tokens.intersection(hinglish_markers)) >= 1:
            return "hinglish"
        return "en"

    def retrieve_and_rerank(
        self, query: str, profile_context: str = "", top_k: int = 4
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Executes Hybrid BM25 + Dense Vector RRF + Contextual Reranking."""
        if not self.kb_items:
            self.rebuild_knowledge_base()

        augmented_query = f"{query} {profile_context}".strip()
        q_tokens = tokenize_text(augmented_query)
        q_vec = self.embedder.embed_text(augmented_query)

        # 1. BM25 lexical ranking
        bm25_ranks: Dict[int, int] = {}
        bm25_raw: Dict[int, float] = {}
        if self.bm25 and q_tokens:
            scores = self.bm25.get_scores(q_tokens)
            ranked_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            for r, idx in enumerate(ranked_idx, start=1):
                bm25_ranks[idx] = r
                bm25_raw[idx] = float(scores[idx])

        # 2. Dense vector ranking
        dense_sims = [
            TextEmbedder.cosine_similarity(q_vec, doc_vec)
            for doc_vec in self.dense_vectors
        ]
        ranked_dense = sorted(range(len(dense_sims)), key=lambda i: dense_sims[i], reverse=True)
        dense_ranks = {idx: r for r, idx in enumerate(ranked_dense, start=1)}

        # 3. Reciprocal Rank Fusion + Semantic Intent Reranking
        q_lower = query.lower()
        is_policy_question = any(
            kw in q_lower
            for kw in [
                "npci", "dbt", "aadhaar", "seeding", "income certificate", "aay",
                "caste", "obc", "ews", "domicile", "niwas", "otr", "face",
                "reject", "mistake", "galati", "renewal", "renew", "gfr", "jrf", "srf",
            ]
        )

        scored_items: List[Tuple[int, float]] = []
        max_rrf = 2.0 / (RRF_K_CONSTANT + 1)

        for idx, item in enumerate(self.kb_items):
            r_b = bm25_ranks.get(idx, len(self.kb_items) + 1)
            r_d = dense_ranks.get(idx, len(self.kb_items) + 1)
            rrf = (1.0 / (RRF_K_CONSTANT + r_b)) + (1.0 / (RRF_K_CONSTANT + r_d))
            norm_score = min(1.0, rrf / max_rrf)

            # Semantic Cross-Attention / Pairwise Late-Interaction Reranker
            norm_score = self.embedder.rerank_score(
                query=augmented_query,
                candidate_text=f"{item['title']} {item['authority']} {item['raw_text'][:500]}",
                base_rrf_score=norm_score,
            )
            title_low = item["title"].lower()
            if item["kind"] == "policy" and is_policy_question:
                if any(w in title_low for w in q_lower.split() if len(w) >= 3):
                    norm_score = min(1.0, norm_score + 0.14)
            if item["source_id"].lower() in q_lower:
                norm_score = 1.0

            scored_items.append((idx, round(norm_score, 4)))

        scored_items.sort(key=lambda x: x[1], reverse=True)
        return [(self.kb_items[idx], score) for idx, score in scored_items[:top_k]]

    def chat(self, req: RAGChatRequest) -> RAGChatResponse:
        """Processes a user query with session memory, hybrid RAG retrieval, and grounded synthesis."""
        session = self.session_store.get_or_create_session(
            session_id=req.session_id,
            consent_given=req.consent_to_remember,
        )

        # Extract any new profile facts mentioned in the user's message
        extracted_facts = ConversationalMemoryStore.extract_profile_facts_from_message(req.query)
        merged_student_profile = {
            **session.get("student_profile", {}),
            **(req.student_profile or {}),
            **(extracted_facts if req.consent_to_remember else {}),
        }
        merged_researcher_profile = {
            **session.get("researcher_profile", {}),
            **(req.researcher_profile or {}),
        }

        # Build concise profile context string for personalized retrieval
        profile_bits = []
        for k in ("state_domicile", "education_level", "social_category", "gender"):
            if merged_student_profile.get(k):
                profile_bits.append(str(merged_student_profile[k]))
        if merged_student_profile.get("family_annual_income_inr"):
            profile_bits.append(f"income {merged_student_profile['family_annual_income_inr']}")
        if merged_researcher_profile.get("research_summary"):
            profile_bits.append(str(merged_researcher_profile["research_summary"])[:100])
        profile_context_str = " ".join(profile_bits)

        lang = self.detect_language(req.query, req.language)
        retrieved = self.retrieve_and_rerank(req.query, profile_context=profile_context_str, top_k=4)

        citations: List[RAGCitation] = []
        for item, score in retrieved:
            snippet = item["hinglish_summary"] if lang == "hinglish" else item["en_summary"]
            citations.append(
                RAGCitation(
                    source_id=item["source_id"],
                    title=item["title"],
                    issuing_authority=item["authority"],
                    official_url=item["official_url"],
                    snippet=snippet[:320],
                    relevance_score=score,
                )
            )

        top_score = retrieved[0][1] if retrieved else 0.0
        if top_score >= 0.75:
            confidence_level = "HIGH"
        elif top_score >= 0.45:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"

        uncertainty_notice = None
        q_low = req.query.lower()
        if confidence_level == "LOW" or any(w in q_low for w in ["exact date today", "my application status", "payment status", "utr number"]):
            uncertainty_notice = (
                "Note: Live individual application/payment tracking and daily portal extensions are hosted directly on the official government portals (scholarships.gov.in / pfms.nic.in). Always verify final status on the cited official link."
                if lang == "en"
                else "सूचना: व्यक्तिगत फॉर्म/पेमेंट का लाइव स्टेटस केवल आधिकारिक सरकारी पोर्टल (scholarships.gov.in / pfms.nic.in) पर देखा जा सकता है। कृपया नीचे दिए गए आधिकारिक लिंक पर पुष्टि करें।"
            )

        answer = self._synthesize_grounded_answer(
            query=req.query,
            lang=lang,
            retrieved=retrieved,
            student_profile=merged_student_profile,
        )

        # Save turn to isolated session memory
        history = list(session.get("messages", []))
        history.append({"role": "user", "content": req.query})
        history.append({"role": "assistant", "content": answer, "language": lang})
        self.session_store.save_session(
            session_id=session["session_id"],
            consent_given=req.consent_to_remember,
            student_profile=merged_student_profile,
            researcher_profile=merged_researcher_profile,
            messages=history,
        )

        follow_ups = (
            [
                "Aadhaar-NPCI DBT bank seeding kaise check karein?",
                "Income aur OBC-NCL certificate ki validity kya hai?",
                "Scholarship form reject hone ki main galatiyan kya hain?",
                "Mere profile ke hisaab se top scholarships kaunsi hain?",
            ]
            if lang == "hinglish"
            else [
                "How do I enable Aadhaar-NPCI DBT seeding in my bank account?",
                "What are the most common reasons scholarship applications get rejected?",
                "What are the validity rules for Income, OBC-NCL, and EWS certificates?",
                "What are the revised JRF/SRF stipend and GFR 2017 grant rules?",
            ]
        )

        return RAGChatResponse(
            answer=answer,
            language_used=lang,
            confidence_level=confidence_level,
            uncertainty_notice=uncertainty_notice,
            citations=citations,
            follow_up_suggestions=follow_ups,
            session_id=session["session_id"],
            remembered_profile_updates=extracted_facts if req.consent_to_remember else {},
        )

    def _synthesize_grounded_answer(
        self,
        query: str,
        lang: str,
        retrieved: List[Tuple[Dict[str, Any], float]],
        student_profile: Dict[str, Any],
    ) -> str:
        if not retrieved:
            return (
                "I could not find a matching statutory circular in the indexed knowledge base. Please check scholarships.gov.in or dst.gov.in."
                if lang == "en"
                else "क्षमा करें, मुझे इस विषय पर कोई सत्यापित सरकारी सर्कुलर नहीं मिला। कृपया आधिकारिक पोर्टल scholarships.gov.in की जाँच करें।"
            )

        # Optional LLM synthesis (Gemini / OpenAI / Ollama) when configured via environment variable
        llm_answer = self.llm_adapter.synthesize_grounded(
            query=query,
            lang=lang,
            retrieved=retrieved,
            student_profile=student_profile,
        )
        if llm_answer:
            return llm_answer

        primary_item, _ = retrieved[0]
        secondary_items = [item for item, _ in retrieved[1:3]]

        profile_line = ""
        if student_profile:
            p_parts = []
            if student_profile.get("gender"):
                p_parts.append(str(student_profile["gender"]))
            if student_profile.get("education_level"):
                p_parts.append(str(student_profile["education_level"]).split("(")[0].strip())
            if student_profile.get("state_domicile") and student_profile["state_domicile"] != "All India":
                p_parts.append(str(student_profile["state_domicile"]))
            if student_profile.get("social_category"):
                p_parts.append(str(student_profile["social_category"]).split("(")[0].strip())
            if student_profile.get("family_annual_income_inr"):
                p_parts.append(f"Income ₹{float(student_profile['family_annual_income_inr']):,.0f}/yr")
            if p_parts:
                if lang == "hinglish":
                    profile_line = f"📌 **Aapke Saved Profile Context ke anusar ({', '.join(p_parts)})**:\n\n"
                else:
                    profile_line = f"📌 **Tailored to Your Active Profile ({', '.join(p_parts)})**:\n\n"

        if lang == "hinglish":
            lines = [
                f"{profile_line}**{primary_item['title']}** `[1]`\n"
                f"*जारीकर्ता (Issuing Authority): {primary_item['authority']}*\n\n"
                f"{primary_item['hinglish_summary']}\n"
            ]
            if secondary_items:
                lines.append("\n**संबंधित आधिकारिक जानकारी (Related Verified Sources):**")
                for i, sec in enumerate(secondary_items, start=2):
                    lines.append(f"• **[{i}] {sec['title']}** ({sec['authority']}): {sec['hinglish_summary'][:220]}...")
            lines.append(
                f"\n🛡️ **आधिकारिक स्रोत (Official Link)**: {primary_item['official_url']} *(100% निःशुल्क सरकारी आवेदन)*"
            )
            return "\n".join(lines)

        lines = [
            f"{profile_line}**{primary_item['title']}** `[1]`\n"
            f"*Issuing Authority: {primary_item['authority']}*\n\n"
            f"{primary_item['en_summary']}\n"
        ]
        if secondary_items:
            lines.append("\n**Additional Grounded References:**")
            for i, sec in enumerate(secondary_items, start=2):
                lines.append(f"• **[{i}] {sec['title']}** ({sec['authority']}): {sec['en_summary'][:220]}...")
        lines.append(
            f"\n🛡️ **Verified Official Portal**: {primary_item['official_url']} *(Zero application fee on statutory portals)*"
        )
        return "\n".join(lines)


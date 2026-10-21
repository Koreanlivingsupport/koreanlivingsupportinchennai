# -*- coding: utf-8 -*-
"""All page text for koreanlivingsupport.com, English and Korean."""

PHONE_DISPLAY = "+91 79850 40232"
EMAIL = "kalaivani@koreanlivingsupport.com"
SITE = "https://koreanlivingsupport.com/"
ADDRESS = {"street": "Kaspapuram", "city": "Chennai", "zip": "600126", "region": "Tamil Nadu"}

SLUGS = {
    "en": {"home": "", "housing": "expat-housing-chennai/", "visa": "frro-visa-services-chennai/",
           "biz": "korean-translation-business-support/", "comp": "iso-27001-tisax-consulting/",
           "tech": "home-office-it-support-chennai/", "privacy": "privacy/"},
    "ko": {"home": "ko/", "housing": "ko/chennai-housing/", "visa": "ko/frro-visa/",
           "biz": "ko/business-support/", "comp": "ko/security-certification/", "tech": "ko/it-support/",
           "privacy": "ko/privacy/"},
}
ORDER = ["housing", "visa", "biz", "comp", "tech"]

UI = {
    "en": {
        "lang_name": "English", "other_lang_label": "한국어", "other_lang_aria": "한국어로 보기",
        "brand_sub": "코리안 리빙 서포트, Chennai",
        "nav": {"housing": "Find a home", "visa": "Visa & FRRO", "biz": "Business support", "comp": "Certification", "tech": "IT support"},
        "wa_btn": "WhatsApp us", "skip": "Skip to content",
        "general_msg": "Hello KLS, I would like to ask about your services.",
        "cta_title": "Tell us what you need, in Korean or English",
        "cta_sub": "On working days we usually reply the same day.",
        "foot_services": "Services", "foot_contact": "Contact", "foot_area": "Areas we serve",
        "foot_areas": "Anna Nagar, Kilpauk, Chennai city, Sriperumbudur, Oragadam, Irungattukottai",
        "formerly": "Formerly Mastermind IT Security Solutions, the same team with wider services",
        "privacy_link": "Privacy Policy",
        "concept": "Concept visual", "home_crumb": "Home",
        "related": "Other services", "faq": "Frequently asked questions",
        "address": "Kaspapuram, Chennai 600126, Tamil Nadu, India",
        "concept_note": "Images marked \"Concept visual\" illustrate our services and 2030 vision. They are not actual listings or current photos.",
    },
    "ko": {
        "lang_name": "한국어", "other_lang_label": "English", "other_lang_aria": "View in English",
        "brand_sub": "코리안 리빙 서포트, 첸나이",
        "nav": {"housing": "주거 찾기", "visa": "비자·FRRO", "biz": "기업 지원", "comp": "보안 인증", "tech": "IT 지원"},
        "wa_btn": "WhatsApp 상담", "skip": "본문으로 이동",
        "general_msg": "안녕하세요 KLS, 상담을 요청합니다.",
        "cta_title": "필요한 것을 한국어로 편하게 말씀해 주세요",
        "cta_sub": "영업일 기준 대부분 당일 회신드립니다.",
        "foot_services": "서비스", "foot_contact": "연락처", "foot_area": "지원 지역",
        "foot_areas": "안나 나가르, 킬파욱, 첸나이 시내, 스리페룸부두르, 오라가담, 이룽가투코타이",
        "formerly": "前 Mastermind IT Security Solutions, 같은 팀이 서비스를 넓혔습니다",
        "privacy_link": "개인정보 처리방침",
        "concept": "콘셉트 이미지", "home_crumb": "홈",
        "related": "다른 서비스", "faq": "자주 묻는 질문",
        "address": "Kaspapuram, Chennai 600126, Tamil Nadu, India",
        "concept_note": "\"콘셉트 이미지\"로 표시된 사진은 서비스와 2030 비전을 표현한 것이며, 실제 매물이나 현재 사진이 아닙니다.",
    },
}

TILES = {
    "en": {
        "housing": ("주거", "Homes & property", "Apartment and villa search, negotiation, agreement and care after move-in.", "Find a home"),
        "visa": ("비자", "Immigration & stay", "FRRO registration, visa extension, residential permit, exit permit, PAN.", "Visa & FRRO services"),
        "biz": ("기업", "Korean business support", "Interpretation, translation, HQ coordination and vendor management.", "Business support"),
        "comp": ("인증", "Certification & IT security", "ISO 27001, TISAX, PCI DSS and SOC 2 consulting and audit support.", "Certification consulting"),
        "tech": ("IT", "IT & tech support", "CCTV, Wi-Fi, smart home and IT support for homes and offices.", "IT support"),
    },
    "ko": {
        "housing": ("주거", "주거·부동산", "아파트·빌라 탐색, 협상, 계약, 입주 후 관리까지.", "집 찾기"),
        "visa": ("비자", "출입국·체류", "FRRO 등록, 비자 연장, 거주허가, 출국 허가, PAN.", "비자·FRRO 서비스"),
        "biz": ("기업", "한국 기업 지원", "통역·번역, 본사–현지 업무 조율, 벤더 관리.", "기업 지원"),
        "comp": ("인증", "보안 인증·IT 보안", "ISO 27001, TISAX, PCI DSS, SOC 2 컨설팅과 심사 대응.", "인증 컨설팅"),
        "tech": ("IT", "IT·기술 지원", "가정·사무실 CCTV, Wi-Fi, 스마트홈, IT 문제 해결.", "IT 지원"),
    },
}

# ---------------------------------------------------------------- HOME
HOME = {
    "en": {
        "title": "Korean Expat Services in Chennai | Korean Living Support",
        "desc": "Housing, FRRO, translation and IT support for Korean companies and families in Chennai. Korean-speaking team. WhatsApp +91 79850 40232.",
        "h1": "Premium apartments and villas in Chennai, found and signed in Korean.",
        "lead": "We match you with homes from our own network of house owners, then handle viewings, negotiation, the agreement and move-in. Visas, business support and IT are covered by the same team.",
        "finder_aria": "Choose what you need",
        "tabs": {"housing": "Find a home", "visa": "Visa & FRRO", "biz": "Business support", "comp": "Certification", "tech": "IT support"},
        "fields": [
            ("Home type", ["Apartment", "Villa / independent house", "Serviced apartment"], 0),
            ("Bedrooms", ["2 BHK", "3 BHK", "4 BHK or more"], 1),
            ("Preferred area", ["Anna Nagar", "Kilpauk", "Chennai city", "Near the plant (Sriperumbudur / Oragadam)", "Advise me"], 4),
            ("Monthly rent", ["Up to ₹1 lakh", "₹1–2 lakh", "Over ₹2 lakh", "Company lease"], 1),
        ],
        "home_intro": "Hello KLS, I am looking for a home in Chennai.",
        "home_cta": "Get matching homes", "home_note": "Opens WhatsApp with your choices filled in. We reply with homes that fit.",
        "panels": {
            "visa": ("We handle your visa and immigration paperwork", "Ask about visa & FRRO", "Hello KLS, I need help with visa / FRRO.",
                     ["FRRO registration and C-Form after arrival", "Visa extension and residential permit renewal", "Exit permit before leaving India", "PAN and income tax (ITR) filing"]),
            "biz": ("Language and coordination between Korean HQ and India", "Ask about business support", "Hello KLS, we are a Korean company in Chennai and need business support.",
                    ["Interpretation for vendor meetings, document translation", "HQ to India coordination and cultural consulting", "Vendor management", "English training for Korean staff"]),
            "comp": ("Security certification ready for HQ audits", "Ask about certification", "Hello KLS, we need security certification consulting.",
                     ["ISO/IEC 27001 implementation and audit", "TISAX for automotive suppliers", "PCI DSS v4.0 and SOC 1/2", "Cybersecurity checks"]),
            "tech": ("IT problems at home and in the office, fixed", "Request IT support", "Hello KLS, I need IT / tech support.",
                     ["Wi-Fi and internet setup", "CCTV and smart home installation", "PC and laptop troubleshooting", "Data backup"]),
        },
        "trust": ["Our own network of house owners", "Viewings and contracts explained in Korean", "Registered Chennai company", "Same team as Mastermind IT Security Solutions"],
        "svc_title": "Five services for living and doing business in Chennai",
        "homes_title": "The easiest way to find a good home in Chennai",
        "homes_lead": "No scrolling through portals. We talk to owners directly and only show you homes we have already checked against what Korean families need.",
        "homes_cta": "See how our housing service works",
        "types": [("Gated community apartments", "Security, power backup, and a pool or gym in a managed complex."),
                  ("Independent villas", "Family homes with a garden and more space."),
                  ("Serviced apartments", "Furnished, cleaned stays for the first weeks or short assignments."),
                  ("Company leases", "Leases in the company's name for several expat staff, managed together.")],
        "why_title": "Why find your home with KLS",
        "why": [("Our own owner network", "We search our list of house owners first for homes that match your brief."),
                ("Viewings in Korean", "We explain distances to school, office and shops in Korean."),
                ("Negotiation on your side", "Rent, deposit and repairs before move-in, negotiated for you."),
                ("Your contact after signing", "Repairs, owner communication and renewal, handled for you.")],
        "steps_title": "Six steps to your keys",
        "steps": [("Brief", "Family size, school, office location and budget."), ("Shortlist", "Homes from our owner network, sent with photos."),
                  ("Viewings", "Visit each home with a Korean-speaking guide."), ("Negotiation", "Rent, deposit, repairs and furnishing agreed."),
                  ("Agreement and documents", "Lease drafting and review, registration, C-Form."), ("Move-in and after", "Internet and utilities connected, repairs and renewals handled.")],
        "area_title": "City neighbourhoods and homes near the plant",
        "area_lead": "Homes in the city near schools, or along the industrial belt for an easy commute. We search both.",
        "area_city": "City residential areas", "area_belt": "Industrial belt along NH48", "map_note": "Chennai city",
        "map_aria": "Simplified map of KLS service areas around Chennai",
        "globe_aria": "Rotating globe showing a connection from Seoul to Chennai",
        "j_title": "From Seoul to Chennai, every step of the move",
        "j_lead": "Beyond the home, the same team looks after everything from arrival to departure.",
        "journey": [("Before you arrive", "Home signed, visa documents checked"), ("First two weeks", "FRRO registration, SIM, bank, PAN"),
                    ("Settling in", "Car and driver, internet, daily help"), ("Every year, and on leaving", "Visa extension, exit permit, tax filing")],
        "c_title": "Between Korean HQ and the Indian site, we align language and standards",
        "c_lead": "Not just one-off interpretation. We help your India operation work to the standard HQ expects.",
        "c_alt": "Concept visual of a Korea–India business meeting",
        "corp": [("주거", "Expat housing, managed", "Homes for several staff, company leases and renewals through one contact.", "housing"),
                 ("통역", "Interpretation and translation", "Vendor meetings, contracts and internal notices in Korean and English.", "biz"),
                 ("조율", "HQ to India coordination", "Fewer misunderstandings from cultural gaps, schedules kept on track.", "biz"),
                 ("인증", "Security certification", "ISO/IEC 27001, TISAX, PCI DSS v4.0 and SOC 1/2.", "comp"),
                 ("IT", "Office IT and security", "Network, CCTV, data backup and cybersecurity checks.", "tech")],
        "c_cta": "Request a company consultation", "c_msg": "Hello KLS, we are a Korean company in Chennai and would like a consultation.",
        "team_title": "A team you meet in person",
        "team": [("RK", "Raj Kumar", "CEO and Founder", "Main contact for Korean corporate clients. Owns every engagement end to end."),
                 ("K", "Kalaivani", "HR and Immigration Consultant", "FRRO, PAN, translation and coordination with company HR teams."),
                 ("YT", "Y Thavanesh", "Operations and System Administrator", "IT and security services, system setup and operations.")],
        "vis_title": "Our vision for KLS – 2030",
        "vis_lead": "To be the first call every Korean company and family makes for a home and a life in Chennai.",
        "road": [("Today", ["Housing service built on our owner network", "Five service areas, from immigration to IT"]),
                 ("Next", ["A dedicated KLS office with a client lounge", "Bilingual specialists for each service"]),
                 ("2030", ["The first housing partner for Korean families in Chennai", "Support in other Korean industrial hubs in India"])],
        "vis_alts": ["Concept visual of a future KLS office building", "Concept visual of a future KLS team", "Concept visual of a future KLS director's office"],
    },
    "ko": {
        "title": "첸나이 주재원·한국 기업 지원 | 코리안 리빙 서포트",
        "desc": "첸나이 집 구하기, FRRO·비자, 통역, IT 지원까지 한국어로. 한국 기업과 가족을 위한 현지 파트너. WhatsApp +91 79850 40232",
        "h1": "첸나이의 프리미엄 아파트와 빌라, 한국어로 찾고 계약까지.",
        "lead": "KLS가 직접 관리하는 집주인 네트워크에서 조건에 맞는 집을 골라, 방문, 가격 협상, 계약서, 입주까지 한 번에 진행합니다. 비자, 기업 지원, IT도 같은 팀이 함께합니다.",
        "finder_aria": "필요한 서비스 선택",
        "tabs": {"housing": "집 찾기", "visa": "비자·FRRO", "biz": "기업 지원", "comp": "보안 인증", "tech": "IT 지원"},
        "fields": [
            ("주거 형태", ["아파트", "빌라·단독주택", "서비스드 아파트"], 0),
            ("방 개수", ["방 2개", "방 3개", "방 4개 이상"], 1),
            ("희망 지역", ["안나 나가르", "킬파욱", "첸나이 시내", "공장 근처 (스리페룸부두르·오라가담)", "추천 받기"], 4),
            ("월 임대료", ["₹1 lakh 이하", "₹1–2 lakh", "₹2 lakh 이상", "회사 임차 (기업 계약)"], 1),
        ],
        "home_intro": "안녕하세요 KLS, 첸나이에서 집을 찾고 있습니다.",
        "home_cta": "조건에 맞는 집 받아보기", "home_note": "선택한 조건이 입력된 WhatsApp 대화가 열립니다. 담당자가 매물을 골라 한국어로 보내드립니다.",
        "panels": {
            "visa": ("비자·출입국 업무를 대신 처리합니다", "비자·FRRO 문의", "안녕하세요 KLS, 비자·FRRO 지원이 필요합니다.",
                     ["도착 후 FRRO 등록, C-Form", "비자 연장, 거주허가 갱신", "귀국 전 출국 허가(Exit Permit)", "PAN 발급, 인도 소득세(ITR) 신고"]),
            "biz": ("한국 본사와 인도 현장 사이의 언어와 업무", "기업 지원 문의", "안녕하세요 KLS, 첸나이 한국 기업입니다. 기업 지원이 필요합니다.",
                    ["협력사 미팅 통역, 계약서·문서 번역", "본사–현지 업무 조율, 문화 컨설팅", "협력사·벤더 관리", "한국 직원 영어 교육"]),
            "comp": ("본사 감사에 맞춘 보안 인증 준비", "인증 컨설팅 문의", "안녕하세요 KLS, 보안 인증 컨설팅이 필요합니다.",
                     ["ISO/IEC 27001 구축과 심사 대응", "TISAX (자동차 산업)", "PCI DSS v4.0, SOC 1/2", "사이버 보안 점검"]),
            "tech": ("집과 사무실의 IT 문제를 해결합니다", "IT 지원 요청", "안녕하세요 KLS, IT·기술 지원이 필요합니다.",
                     ["Wi-Fi, 인터넷 설치", "CCTV, 스마트홈 설치", "PC·노트북 문제 해결", "데이터 백업"]),
        },
        "trust": ["직접 관리하는 집주인 네트워크", "한국어로 방문·계약 안내", "첸나이 등록 법인", "Mastermind IT Security Solutions와 같은 팀"],
        "svc_title": "첸나이 생활과 비즈니스에 필요한 5가지 서비스",
        "homes_title": "첸나이에서 가장 편하게 좋은 집을 구하는 방법",
        "homes_lead": "포털 매물을 하나씩 확인할 필요가 없습니다. KLS가 집주인과 직접 연락하고, 한국 가족의 기준으로 먼저 확인한 집만 보여드립니다.",
        "homes_cta": "주거 서비스 자세히 보기",
        "types": [("게이티드 커뮤니티 아파트", "경비, 발전기, 수영장이나 헬스장을 갖춘 단지형 아파트."),
                  ("단독 빌라", "정원과 넓은 공간이 있는 가족용 독립 주택."),
                  ("서비스드 아파트", "가구와 청소가 포함된 초기 정착·단기 체류용 숙소."),
                  ("기업 임차", "주재원 여러 명을 위한 회사 명의 임대와 일괄 관리.")],
        "why_title": "KLS와 함께 집을 구하면",
        "why": [("직접 관리하는 집주인 네트워크", "KLS가 보유한 집주인 목록에서 조건에 맞는 집을 먼저 찾아드립니다."),
                ("한국어로 방문 안내", "학교, 회사, 마트와의 거리까지 한국어로 설명합니다."),
                ("고객 편에서 협상", "임대료, 보증금, 입주 전 수리 조건을 대신 협상합니다."),
                ("계약 후에도 연락 창구", "수리, 집주인 연락, 계약 갱신까지 계속 지원합니다.")],
        "steps_title": "계약까지 6단계",
        "steps": [("조건 상담", "가족 구성, 학교, 회사 위치, 예산 확인."), ("매물 추천", "집주인 네트워크에서 고른 집을 사진과 함께 전달."),
                  ("현장 방문", "한국어 담당자와 함께 집을 직접 확인."), ("협상", "임대료, 보증금, 수리, 가구 조건 협상."),
                  ("계약·서류", "임대차 계약서 작성과 검토, 등록, C-Form."), ("입주와 사후 관리", "인터넷, 공과금 연결, 수리와 갱신 지원.")],
        "area_title": "도심 주거지부터 공장 근처까지",
        "area_lead": "자녀 학교를 위한 도심 주거지와 출퇴근이 편한 산업 벨트 주변, 두 지역 모두 집을 찾아드립니다.",
        "area_city": "도심 주거 지역", "area_belt": "산업 벨트 (NH48 주변)", "map_note": "첸나이 시내",
        "map_aria": "첸나이 지원 지역 약도",
        "globe_aria": "서울에서 첸나이로 이어지는 회전 지구본",
        "j_title": "서울에서 첸나이로, 이주의 모든 단계",
        "j_lead": "집 외에도 도착부터 귀국까지 필요한 일을 같은 팀이 이어서 챙깁니다.",
        "journey": [("도착 전", "집 계약, 비자 서류 확인"), ("도착 후 2주", "FRRO 등록, SIM, 은행, PAN"),
                    ("정착", "차량·기사, 인터넷, 생활 지원"), ("매년, 귀국 시", "비자 연장, 출국 허가, 소득세 신고")],
        "c_title": "한국 본사와 인도 현장 사이, 말과 기준을 맞춥니다",
        "c_lead": "통역 한 번이 아니라, 본사가 기대하는 기준으로 인도 현장이 움직이도록 돕습니다.",
        "c_alt": "한국–인도 비즈니스 미팅 콘셉트 이미지",
        "corp": [("주거", "주재원 주거 일괄 관리", "여러 직원의 집 찾기, 회사 명의 계약, 갱신을 한 창구에서.", "housing"),
                 ("통역", "통역·번역", "협력사 미팅, 계약서, 사내 공지까지 한국어–영어.", "biz"),
                 ("조율", "본사–현지 업무 조율", "문화 차이로 생기는 오해를 줄이고 일정을 관리합니다.", "biz"),
                 ("인증", "보안 인증 컨설팅", "ISO/IEC 27001, TISAX, PCI DSS v4.0, SOC 1/2.", "comp"),
                 ("IT", "사무실 IT·보안", "네트워크, CCTV, 데이터 백업, 사이버 보안 점검.", "tech")],
        "c_cta": "기업 상담 요청", "c_msg": "안녕하세요 KLS, 첸나이 한국 기업입니다. 상담을 요청합니다.",
        "team_title": "직접 만나 책임지는 팀",
        "team": [("RK", "Raj Kumar", "대표", "한국 기업 고객의 주 담당자. 모든 업무를 처음부터 끝까지 책임집니다."),
                 ("K", "Kalaivani", "HR·출입국 컨설턴트", "FRRO, PAN, 번역, 기업 HR 팀과의 업무 조율."),
                 ("YT", "Y Thavanesh", "운영·시스템 관리자", "IT·보안 서비스, 시스템 구축과 운영.")],
        "vis_title": "KLS 2030 비전",
        "vis_lead": "첸나이에 오는 모든 한국 기업과 가족이 집과 생활을 위해 가장 먼저 연락하는 곳.",
        "road": [("지금", ["집주인 네트워크 기반 주거 서비스", "출입국·기업·보안·IT 5개 분야"]),
                 ("다음 단계", ["고객 라운지를 갖춘 KLS 전용 사무실", "분야별 이중언어 전문가 채용"]),
                 ("2030", ["첸나이 한국 가족의 첫 번째 주거 파트너", "인도 내 다른 한국 산업 거점으로 확장"])],
        "vis_alts": ["미래 KLS 사옥 콘셉트 이미지", "미래 KLS 팀 콘셉트 이미지", "미래 KLS 대표실 콘셉트 이미지"],
    },
}

# ---------------------------------------------------------------- SERVICE PAGES
# section kinds: ("p", [paragraphs]) | ("ul", [(bold, text)]) | ("steps", [(title, text)])
SERVICES = {
"housing": {
  "img": "housing",
  "en": {
    "title": "Expat Apartments & Villas in Chennai | KLS",
    "desc": "Premium apartments and villas for Korean expats in Chennai. Owner network, viewings in Korean, negotiation and lease paperwork done for you.",
    "h1": "Premium apartments and villas for expats in Chennai",
    "lead": "Korean Living Support (KLS) finds expat apartments and villas in Chennai from our own network of house owners. We guide viewings in Korean, negotiate rent and deposit for you, and handle the rental agreement until you have the keys.",
    "alt": "Concept visual of a KLS guide showing a Korean family an apartment in Chennai",
    "cta": "Start your home search", "wa": "Hello KLS, I am looking for a home in Chennai.",
    "service_name": "Expat apartment and villa search in Chennai",
    "sections": [
      ("Homes we find for Korean expats", "ul", [
        ("Gated community apartments", "with 24-hour security, power backup, and a pool or gym in the complex."),
        ("Independent villas", "with a garden and more space for families."),
        ("Furnished and serviced apartments", "in Chennai for the first weeks or short assignments."),
        ("Corporate leases", "in your company's name for several expat staff, managed through one contact.")]),
      ("Areas we cover", "p", [
        "Most Korean families choose city neighbourhoods close to international schools and Korean shops, such as Anna Nagar and Kilpauk. Employees working at plants in Sriperumbudur, Oragadam and Irungattukottai often prefer an apartment near Sriperumbudur or along the NH48 corridor to cut the daily commute.",
        "We search both, and we tell you honestly which suits your family better."]),
      ("Why find your home with KLS", "ul", [
        ("Our own owner network.", "We search our list of house owners first, so you see homes that are already checked."),
        ("Viewings in Korean.", "We explain the area, the distance to school and office, and the building rules in Korean."),
        ("Negotiation on your side.", "Rent, security deposit, repairs before move-in and furnishing are agreed for you."),
        ("Rental agreement help in Chennai.", "We draft or review the lease, explain each clause in Korean, and arrange registration and the C-Form."),
        ("Support after you move in.", "Repairs, communication with the owner and renewal stay with us.")]),
      ("Six steps from search to keys", "steps", [
        ("Brief", "Family size, school, office location, budget and move-in date."),
        ("Shortlist", "Homes from our owner network, sent to you with photos on WhatsApp."),
        ("Viewings", "Visit the best homes with a Korean-speaking guide."),
        ("Negotiation", "Rent, deposit, repairs and furnishing agreed with the owner."),
        ("Agreement and documents", "Lease drafted and reviewed, registration and C-Form done."),
        ("Move-in", "Internet, electricity and gas connected; we stay your contact after that.")]),
      ("For companies relocating staff to Chennai", "p", [
        "If your company is sending several employees, we manage all their housing together: one brief, one contact, company leases and renewals on one schedule. This saves your HR team time and keeps every employee's home at the same standard."]),
    ],
    "faq": [
      ("How long does it take to find a home in Chennai?", "Most searches take one to three weeks, depending on area and budget."),
      ("Can you start before I arrive in India?", "Yes. We can shortlist homes and run video viewings before you land."),
      ("What does a typical lease in Chennai include?", "Usually an 11-month agreement, a security deposit and a notice period. We explain each term in Korean before you sign."),
      ("Do you help after the lease is signed?", "Yes. Repairs, owner issues and renewal are part of our service.")],
  },
  "ko": {
    "title": "첸나이 아파트·빌라 임대, 한국어로 집 구하기 | KLS",
    "desc": "첸나이 프리미엄 아파트와 빌라. 집주인 네트워크, 한국어 방문 안내, 가격 협상, 임대차 계약까지 한 번에.",
    "h1": "첸나이 프리미엄 아파트와 빌라, 한국어로 찾고 계약까지",
    "lead": "코리안 리빙 서포트(KLS)는 직접 관리하는 집주인 네트워크에서 첸나이 아파트와 빌라를 찾아드립니다. 한국어로 집을 보여드리고, 임대료와 보증금을 대신 협상하며, 열쇠를 받을 때까지 임대차 계약을 책임집니다.",
    "alt": "첸나이 아파트를 한국 가족에게 안내하는 KLS 담당자 콘셉트 이미지",
    "cta": "집 찾기 상담 시작", "wa": "안녕하세요 KLS, 첸나이에서 집을 찾고 있습니다.",
    "service_name": "첸나이 아파트·빌라 임대 지원",
    "sections": [
      ("KLS가 찾아드리는 집", "ul", [
        ("게이티드 커뮤니티 아파트:", "24시간 경비, 발전기, 단지 내 수영장이나 헬스장."),
        ("단독 빌라:", "정원과 넓은 공간이 있는 가족용 주택."),
        ("가구 포함·서비스드 아파트:", "도착 후 초기 정착이나 단기 출장용."),
        ("기업 임차:", "여러 주재원을 위한 회사 명의 계약을 한 창구에서 관리.")]),
      ("지원 지역", "p", [
        "자녀 학교와 한인 마트가 가까운 안나 나가르, 킬파욱 등 도심 지역과, 스리페룸부두르·오라가담·이룽가투코타이 공장 근처의 숙소를 모두 찾아드립니다.",
        "가족 상황에 더 맞는 지역을 솔직하게 안내해 드립니다."]),
      ("KLS와 함께 집을 구하면", "ul", [
        ("직접 관리하는 집주인 네트워크:", "이미 확인한 집부터 보여드립니다."),
        ("한국어 방문 안내:", "동네 분위기, 학교·회사까지 거리, 건물 규칙을 한국어로 설명합니다."),
        ("고객 편에서 협상:", "임대료, 보증금, 입주 전 수리, 가구 조건을 협상합니다."),
        ("임대차 계약 지원:", "계약서 작성·검토, 조항별 한국어 설명, 등록과 C-Form까지."),
        ("입주 후 관리:", "수리, 집주인 연락, 계약 갱신을 계속 지원합니다.")]),
      ("계약까지 6단계", "steps", [
        ("조건 상담", "가족 구성, 학교, 회사 위치, 예산, 입주 날짜."),
        ("매물 추천", "집주인 네트워크에서 고른 집을 사진과 함께 WhatsApp으로 전달."),
        ("현장 방문", "한국어 담당자와 함께 집을 직접 확인."),
        ("협상", "임대료, 보증금, 수리, 가구 조건 합의."),
        ("계약·서류", "임대차 계약서 작성과 검토, 등록, C-Form."),
        ("입주", "인터넷, 전기, 가스 연결. 이후에도 계속 연락 창구가 됩니다.")]),
      ("주재원을 파견하는 기업을 위해", "p", [
        "여러 직원이 함께 오는 경우, 모든 집을 한 번에 관리합니다. 하나의 요청, 하나의 담당자, 회사 명의 계약과 갱신을 한 일정으로. 인사팀의 시간을 줄이고 모든 직원의 주거를 같은 기준으로 맞춥니다."]),
    ],
    "faq": [
      ("집을 찾는 데 얼마나 걸리나요?", "지역과 예산에 따라 보통 1~3주 걸립니다."),
      ("인도 도착 전에 시작할 수 있나요?", "네. 도착 전에 매물을 고르고 영상으로 집을 보여드립니다."),
      ("첸나이 임대차 계약은 어떻게 되어 있나요?", "보통 11개월 계약, 보증금, 해지 통보 기간이 있습니다. 서명 전에 모든 조항을 한국어로 설명해 드립니다."),
      ("계약 후에도 도와주나요?", "네. 수리, 집주인 문제, 계약 갱신까지 지원합니다.")],
  },
},
"visa": {
  "img": "immigration",
  "en": {
    "title": "FRRO Registration & Visa Extension Chennai | KLS",
    "desc": "FRRO registration, visa extension, residential permit renewal and exit permit in Chennai, handled for Korean expats and companies.",
    "h1": "FRRO and visa services in Chennai for Korean expats",
    "lead": "KLS handles FRRO registration in Chennai for Korean expats and their families, from the first registration after arrival to visa extension, residential permit renewal and the exit permit when you leave India. We prepare your documents, file on the e-FRRO portal and explain each step in Korean.",
    "alt": "Concept visual of a KLS consultant helping a Korean couple with visa documents",
    "cta": "Ask about visa & FRRO", "wa": "Hello KLS, I need help with FRRO / visa.",
    "service_name": "FRRO registration and visa services in Chennai",
    "sections": [
      ("FRRO registration after arrival", "p", [
        "Foreigners on long-term visas, such as employment or business visas for more than 180 days, must register with the FRRO soon after arrival. Your visa usually states the deadline. We collect your documents, fill the e-FRRO application, book any appointment and follow up until your Residential Permit is issued.",
        "Family members on dependent visas are registered at the same time, so the whole family is covered in one process."]),
      ("Visa extension and residential permit renewal", "p", [
        "We track your permit expiry date and start the renewal well before it lapses. You get a clear list of documents in Korean, including the letters your employer needs to provide, and we handle the online filing."]),
      ("Exit permit before leaving India", "p", [
        "When your assignment ends, you may need an exit permit before you can leave. We prepare the application together with your employer so your departure date is not delayed."]),
      ("PAN card and income tax for foreigners", "ul", [
        ("PAN card:", "needed for your bank account, salary and many daily payments."),
        ("Income tax (ITR) filing:", "we coordinate your annual return with a qualified tax professional."),
        ("C-Form:", "the landlord's or hotel's report of your stay, arranged when you move in.")]),
      ("How we work", "steps", [
        ("Check", "We review your visa, passport and employer documents."),
        ("Prepare", "You receive a document list in Korean; we fill all forms."),
        ("File", "We submit on the e-FRRO portal and track the status."),
        ("Remind", "We alert you before every renewal or expiry date.")]),
    ],
    "faq": [
      ("Who needs to register with the FRRO in Chennai?", "In general, foreigners on visas valid for more than 180 days, such as employment visas, and their dependants. Your visa conditions decide the exact rule; we check them for you."),
      ("Can you handle FRRO for all our company's Korean staff?", "Yes. We manage registrations and renewals for whole teams and keep one expiry calendar for your HR team."),
      ("Do I need to visit the FRRO office?", "Most services are online through e-FRRO. If a visit is requested, we prepare you and can accompany you."),
      ("Do you give legal advice on visas?", "We handle the process and paperwork. For legal questions about visa eligibility, we work with qualified immigration lawyers.")],
  },
  "ko": {
    "title": "첸나이 FRRO 등록·비자 연장 대행 | KLS",
    "desc": "첸나이 FRRO 등록, 비자 연장, 거주허가 갱신, 출국 허가를 한국어로 안내하고 대신 처리합니다.",
    "h1": "첸나이 FRRO·비자 업무, 한국어로 대행합니다",
    "lead": "KLS는 첸나이에 오는 한국 주재원과 가족의 FRRO 등록을 대행합니다. 도착 후 최초 등록부터 비자 연장, 거주허가 갱신, 귀국 전 출국 허가까지 서류를 준비하고 e-FRRO에 신청하며, 모든 과정을 한국어로 안내합니다.",
    "alt": "한국 부부의 비자 서류를 돕는 KLS 컨설턴트 콘셉트 이미지",
    "cta": "비자·FRRO 문의", "wa": "안녕하세요 KLS, FRRO·비자 지원이 필요합니다.",
    "service_name": "첸나이 FRRO 등록·비자 업무 대행",
    "sections": [
      ("도착 후 FRRO 등록", "p", [
        "고용 비자나 비즈니스 비자처럼 180일 이상 체류하는 외국인은 도착 후 FRRO에 등록해야 합니다. 기한은 보통 비자에 적혀 있습니다. 서류를 모으고 e-FRRO 신청서를 작성하며, 거주허가(Residential Permit)가 나올 때까지 진행 상황을 챙깁니다.",
        "동반 비자의 가족도 함께 등록하므로 가족 전체가 한 번에 처리됩니다."]),
      ("비자 연장과 거주허가 갱신", "p", [
        "거주허가 만료일을 관리하고 만료 전에 미리 갱신을 시작합니다. 회사가 준비해야 할 서류를 포함한 목록을 한국어로 드리고, 온라인 신청을 대신 진행합니다."]),
      ("귀국 전 출국 허가", "p", [
        "근무가 끝나 인도를 떠날 때 출국 허가(Exit Permit)가 필요할 수 있습니다. 회사와 함께 미리 신청해 출국 일정이 늦어지지 않도록 합니다."]),
      ("PAN과 인도 소득세", "ul", [
        ("PAN 카드:", "은행 계좌, 급여, 각종 결제에 필요합니다."),
        ("소득세(ITR) 신고:", "공인 세무 전문가와 함께 연간 신고를 진행합니다."),
        ("C-Form:", "집주인이나 호텔이 체류를 신고하는 서류로, 입주할 때 함께 처리합니다.")]),
      ("진행 방식", "steps", [
        ("확인", "비자, 여권, 회사 서류를 검토합니다."),
        ("준비", "한국어 서류 목록을 드리고 모든 신청서를 작성합니다."),
        ("신청", "e-FRRO에 제출하고 진행 상황을 확인합니다."),
        ("알림", "갱신·만료일 전에 미리 알려드립니다.")]),
    ],
    "faq": [
      ("첸나이에서 누가 FRRO에 등록해야 하나요?", "일반적으로 고용 비자 등 180일 이상 유효한 비자를 가진 외국인과 동반 가족입니다. 정확한 기준은 비자 조건에 따라 다르며, 저희가 확인해 드립니다."),
      ("회사의 한국 직원 전체 FRRO를 맡길 수 있나요?", "네. 팀 전체의 등록과 갱신을 관리하고, 인사팀이 볼 수 있는 만료 일정표를 하나로 관리합니다."),
      ("FRRO 사무실에 직접 가야 하나요?", "대부분 e-FRRO에서 온라인으로 처리됩니다. 방문이 필요하면 미리 준비해 드리고 동행할 수 있습니다."),
      ("비자에 대한 법률 자문도 하나요?", "KLS는 절차와 서류를 대행합니다. 비자 자격에 관한 법률 문제는 공인 출입국 변호사와 협력합니다.")],
  },
},
"biz": {
  "img": "business",
  "en": {
    "title": "Korean Translator & Interpreter in Chennai | KLS",
    "desc": "Korean–English interpretation, translation and HQ coordination for Korean companies in Chennai and Sriperumbudur.",
    "h1": "Korean translation and business support in Chennai",
    "lead": "Need a Korean translator in Chennai? KLS provides Korean–English interpretation and translation for Korean companies in Chennai, Sriperumbudur and Oragadam: vendor meetings, contracts, HR notices and day-to-day coordination between Korean HQ and the India team.",
    "alt": "Concept visual of a Korea–India business meeting led by a KLS consultant",
    "cta": "Ask about business support", "wa": "Hello KLS, we are a Korean company in Chennai and need business support.",
    "service_name": "Korean translation, interpretation and business support",
    "sections": [
      ("Interpretation for meetings and site visits", "p", [
        "Our Korean interpreter in Chennai joins your vendor negotiations, customer meetings, plant visits and HQ video calls. We translate meaning, not just words, so both sides understand the decision that was made."]),
      ("Document and contract translation", "ul", [
        ("Contracts and quotations", "between Korean and English, checked for consistent terms."),
        ("HR documents", "such as offer letters, policies and notices for Indian staff."),
        ("Reports to HQ", "turning Indian site reports into Korean that HQ can act on.")]),
      ("HQ to India coordination", "p", [
        "Many problems between Korean HQ and Indian teams come from different working styles, not language. We explain Korean expectations to the Indian team and Indian practice to HQ, and keep schedules and follow-ups on track."]),
      ("Vendor management and English training", "ul", [
        ("Vendor management:", "finding, briefing and following up with local suppliers."),
        ("English training:", "practical business English for Korean managers new to India.")]),
      ("How an engagement runs", "steps", [
        ("Call", "Tell us the meeting, document or project."),
        ("Quote", "Clear scope, timing and price before we start."),
        ("Deliver", "Interpretation on site or online, translation by the agreed date."),
        ("Follow up", "Action points recorded in both languages.")]),
    ],
    "faq": [
      ("Do you provide interpreters at plants in Sriperumbudur and Oragadam?", "Yes. We travel to the industrial belt for meetings, audits and site visits."),
      ("Can you translate technical documents?", "Yes, including manufacturing, quality and IT documents. Specialist terms are checked with you before final delivery."),
      ("Do you offer monthly support instead of per-job?", "Yes. Companies with regular needs can book a monthly retainer for interpretation and coordination."),
      ("Which languages do you work in?", "Korean, English and Tamil.")],
  },
  "ko": {
    "title": "첸나이 한국어 통역·번역, 한국 기업 지원 | KLS",
    "desc": "첸나이·스리페룸부두르 한국 기업을 위한 통역, 번역, 본사–현지 업무 조율.",
    "h1": "한국 본사와 인도 현장 사이, 말과 기준을 맞춥니다",
    "lead": "첸나이에서 한국어 통역이 필요하신가요? KLS는 첸나이·스리페룸부두르·오라가담의 한국 기업을 위해 협력사 미팅 통역, 계약서 번역, 본사와 인도 현지 팀 간 업무 조율을 지원합니다.",
    "alt": "KLS 컨설턴트가 진행하는 한국–인도 비즈니스 미팅 콘셉트 이미지",
    "cta": "기업 지원 문의", "wa": "안녕하세요 KLS, 첸나이 한국 기업입니다. 기업 지원이 필요합니다.",
    "service_name": "한국어 통역·번역, 한국 기업 지원",
    "sections": [
      ("미팅과 현장 방문 통역", "p", [
        "협력사 협상, 고객 미팅, 공장 방문, 본사 화상회의에 통역사가 함께합니다. 단어가 아니라 의미를 전달해, 양쪽 모두 무엇이 결정되었는지 정확히 이해하도록 돕습니다."]),
      ("문서·계약서 번역", "ul", [
        ("계약서·견적서:", "한국어–영어 번역, 용어 일관성 확인."),
        ("인사 문서:", "인도 직원용 채용 통지서, 사내 규정, 공지."),
        ("본사 보고서:", "인도 현장 보고서를 본사가 바로 판단할 수 있는 한국어로.")]),
      ("본사–현지 업무 조율", "p", [
        "본사와 인도 팀 사이의 문제는 언어보다 일하는 방식의 차이에서 생기는 경우가 많습니다. 인도 팀에는 한국의 기대를, 본사에는 인도 현지 관행을 설명하고 일정과 후속 조치를 관리합니다."]),
      ("벤더 관리와 영어 교육", "ul", [
        ("벤더 관리:", "현지 협력사 발굴, 요구사항 전달, 후속 관리."),
        ("영어 교육:", "인도에 처음 온 한국 관리자를 위한 실무 비즈니스 영어.")]),
      ("진행 방식", "steps", [
        ("문의", "미팅, 문서, 프로젝트 내용을 알려주세요."),
        ("견적", "시작 전에 범위, 일정, 비용을 명확히 안내합니다."),
        ("수행", "현장 또는 온라인 통역, 약속한 날짜에 번역 전달."),
        ("후속", "결정 사항을 두 언어로 정리해 드립니다.")]),
    ],
    "faq": [
      ("스리페룸부두르, 오라가담 공장에도 통역사가 가나요?", "네. 미팅, 심사, 현장 방문을 위해 산업 벨트까지 이동합니다."),
      ("기술 문서도 번역하나요?", "네. 생산, 품질, IT 문서도 번역하며 전문 용어는 최종 전달 전에 함께 확인합니다."),
      ("건별이 아닌 월 단위 지원도 가능한가요?", "네. 정기적으로 필요한 기업은 통역과 업무 조율을 월 단위 계약으로 이용할 수 있습니다."),
      ("어떤 언어를 지원하나요?", "한국어, 영어, 타밀어입니다.")],
  },
},
"comp": {
  "img": "vision-md",
  "en": {
    "title": "ISO 27001 & TISAX Consulting Chennai | KLS",
    "desc": "ISO/IEC 27001, TISAX, PCI DSS and SOC 2 consulting and audit support for Korean and Indian companies in Chennai.",
    "h1": "ISO 27001 and TISAX consulting in Chennai",
    "lead": "KLS is an ISO 27001 consultant in Chennai for Korean and Indian companies. We prepare you for ISO/IEC 27001, TISAX, PCI DSS v4.0 and SOC 2: gap assessment, policies, staff training and support through the certification audit, with reports your Korean HQ can read.",
    "alt": "Concept visual of a KLS director's office",
    "cta": "Ask about certification", "wa": "Hello KLS, we need security certification consulting.",
    "service_name": "ISO 27001, TISAX, PCI DSS and SOC 2 consulting",
    "sections": [
      ("ISO/IEC 27001 implementation", "p", [
        "We take you from where you are today to a certifiable information security management system: scope, risk assessment, Statement of Applicability, policies and the evidence auditors ask for. Our team comes from military IT operations and corporate information security, so the controls are practical, not paperwork only."]),
      ("TISAX for automotive suppliers", "p", [
        "Many Korean automotive suppliers in Chennai are asked by European customers for a TISAX label. We map your current controls to the VDA ISA questionnaire, close the gaps and prepare you for the assessment."]),
      ("PCI DSS, SOC 1 and SOC 2", "ul", [
        ("PCI DSS v4.0:", "for companies that handle card payments."),
        ("SOC 1 and SOC 2:", "readiness for service companies whose customers ask for assurance reports."),
        ("Cybersecurity health check:", "a short review of network, endpoints, backups and access.")]),
      ("How a certification project runs", "steps", [
        ("Gap assessment", "Where you stand against the standard, in a short report."),
        ("Plan", "Actions, owners and dates agreed with your team and HQ."),
        ("Build", "Policies, procedures, risk register and staff training."),
        ("Internal audit", "A full rehearsal before the certification body arrives."),
        ("Audit support", "We stay with you during the certification audit.")]),
    ],
    "faq": [
      ("How long does ISO 27001 certification take?", "It depends on your size and starting point. A small or mid-size site often needs several months from gap assessment to audit."),
      ("Can reports be in Korean for HQ?", "Yes. We provide summaries in Korean and full documentation in English."),
      ("Do you issue the certificate?", "No. Certificates are issued by accredited certification bodies. We prepare you and support you through their audit."),
      ("Do you support companies outside Chennai?", "Yes. Much of the work can be done remotely, with site visits as needed.")],
  },
  "ko": {
    "title": "인도 ISO 27001·TISAX 인증 컨설팅 | KLS",
    "desc": "인도 법인의 ISO/IEC 27001, TISAX, PCI DSS, SOC 2 인증 준비와 심사 대응을 지원합니다.",
    "h1": "본사 감사에 맞춘 보안 인증 준비",
    "lead": "KLS는 인도 법인의 ISO/IEC 27001, TISAX, PCI DSS v4.0, SOC 2 인증을 준비합니다. 현황 진단, 정책 수립, 직원 교육, 심사 대응까지 진행하며, 한국 본사가 바로 읽을 수 있는 보고서를 드립니다.",
    "alt": "KLS 대표 사무실 콘셉트 이미지",
    "cta": "인증 컨설팅 문의", "wa": "안녕하세요 KLS, 보안 인증 컨설팅이 필요합니다.",
    "service_name": "ISO 27001·TISAX·PCI DSS·SOC 2 인증 컨설팅",
    "sections": [
      ("ISO/IEC 27001 구축", "p", [
        "현재 상태에서 인증 가능한 정보보호 관리체계까지 함께 만듭니다. 적용 범위, 위험 평가, 적용성 보고서(SoA), 정책, 심사원이 요구하는 증적까지 준비합니다. 군 IT 운영과 기업 정보보안 경력을 바탕으로, 서류가 아닌 실제로 작동하는 통제를 만듭니다."]),
      ("자동차 협력사를 위한 TISAX", "p", [
        "첸나이의 많은 한국 자동차 부품사가 유럽 고객으로부터 TISAX 레이블을 요구받습니다. 현재 통제를 VDA ISA 질문지에 맞춰 점검하고, 부족한 부분을 보완해 평가를 준비합니다."]),
      ("PCI DSS, SOC 1, SOC 2", "ul", [
        ("PCI DSS v4.0:", "카드 결제를 처리하는 기업."),
        ("SOC 1·SOC 2:", "고객이 보증 보고서를 요구하는 서비스 기업의 준비."),
        ("사이버 보안 점검:", "네트워크, 단말, 백업, 접근 권한에 대한 간단한 점검.")]),
      ("인증 프로젝트 진행", "steps", [
        ("현황 진단", "표준 대비 현재 수준을 짧은 보고서로."),
        ("계획", "본사·현지 팀과 조치, 담당자, 일정 합의."),
        ("구축", "정책, 절차, 위험 관리 대장, 직원 교육."),
        ("내부 심사", "인증 기관 심사 전 전체 리허설."),
        ("심사 대응", "인증 심사 기간 동안 함께합니다.")]),
    ],
    "faq": [
      ("ISO 27001 인증은 얼마나 걸리나요?", "규모와 현재 수준에 따라 다릅니다. 중소 규모 사업장은 현황 진단부터 심사까지 보통 몇 개월이 걸립니다."),
      ("본사용 한국어 보고서가 가능한가요?", "네. 요약은 한국어로, 전체 문서는 영어로 드립니다."),
      ("KLS가 인증서를 발급하나요?", "아니요. 인증서는 공인 인증 기관이 발급합니다. KLS는 준비와 심사 대응을 지원합니다."),
      ("첸나이 외 지역 기업도 지원하나요?", "네. 많은 작업이 원격으로 가능하며, 필요할 때 현장을 방문합니다.")],
  },
},
"tech": {
  "img": "vision-team",
  "en": {
    "title": "CCTV, Wi-Fi & IT Support in Chennai | KLS",
    "desc": "CCTV, home Wi-Fi, smart home and IT support for expat homes and offices in Chennai. Service in Korean and English.",
    "h1": "Home and office IT support in Chennai",
    "lead": "KLS provides CCTV installation in Chennai, home Wi-Fi setup, smart home devices and IT support for expat homes and Korean offices. One call in Korean or English, and a technician who explains what was done.",
    "alt": "Concept visual of the KLS team",
    "cta": "Request IT support", "wa": "Hello KLS, I need IT / tech support.",
    "service_name": "CCTV, Wi-Fi and IT support in Chennai",
    "sections": [
      ("CCTV installation", "p", [
        "We plan camera positions, install and configure the recorder, and set up viewing on your phone, so you can check your home or office from anywhere, including from Korea."]),
      ("Home and office Wi-Fi", "p", [
        "New apartment, weak signal in the bedrooms, or an office that keeps dropping? We arrange the internet connection, place the right routers or mesh units, and secure the network."]),
      ("What else we fix", "ul", [
        ("Smart home:", "door locks, cameras, lighting and appliances set up and connected."),
        ("PC and laptop support:", "slow machines, software, printers and email."),
        ("Data backup:", "automatic backups for photos and work files, tested so they actually restore."),
        ("Office IT:", "network, user accounts and basic security for small offices.")]),
      ("How it works", "steps", [
        ("Message us", "Describe the problem on WhatsApp, with a photo if you can."),
        ("Visit or remote", "We fix it remotely where possible, or book a visit."),
        ("Explain", "We tell you in Korean what was done and what to watch for.")]),
    ],
    "faq": [
      ("Do you set up internet for a new apartment?", "Yes. We arrange the connection with a local provider and set up Wi-Fi in every room."),
      ("Can I view my CCTV from Korea?", "Yes. We configure secure mobile viewing that works from anywhere."),
      ("Do you support offices as well as homes?", "Yes. We support small and mid-size offices with network, security and day-to-day IT."),
      ("Which areas do you cover?", "Chennai city and the industrial belt around Sriperumbudur, Oragadam and Irungattukottai.")],
  },
  "ko": {
    "title": "첸나이 CCTV·인터넷·IT 지원 | KLS",
    "desc": "첸나이 집과 사무실의 CCTV, Wi-Fi, 스마트홈 설치와 IT 문제 해결. 한국어 상담.",
    "h1": "집과 사무실의 IT 문제, 한국어로 해결합니다",
    "lead": "KLS는 첸나이 주재원 가정과 한국 기업 사무실의 CCTV 설치, Wi-Fi·인터넷 설치, 스마트홈, IT 문제 해결을 지원합니다. 한국어로 요청하고, 무엇을 해결했는지 한국어로 설명드립니다.",
    "alt": "KLS 팀 콘셉트 이미지",
    "cta": "IT 지원 요청", "wa": "안녕하세요 KLS, IT·기술 지원이 필요합니다.",
    "service_name": "첸나이 CCTV·Wi-Fi·IT 지원",
    "sections": [
      ("CCTV 설치", "p", [
        "카메라 위치를 설계하고 녹화기를 설치·설정하며, 휴대폰으로 볼 수 있게 연결합니다. 한국에서도 집이나 사무실을 확인할 수 있습니다."]),
      ("집과 사무실 Wi-Fi", "p", [
        "새 아파트 인터넷 개통, 방마다 약한 신호, 자주 끊기는 사무실 네트워크까지. 인터넷 연결을 준비하고 공유기나 메시 장비를 알맞게 배치하며 네트워크 보안을 설정합니다."]),
      ("그 밖에 해결하는 일", "ul", [
        ("스마트홈:", "도어락, 카메라, 조명, 가전 설치와 연결."),
        ("PC·노트북:", "느린 컴퓨터, 소프트웨어, 프린터, 이메일 문제."),
        ("데이터 백업:", "사진과 업무 파일 자동 백업, 실제 복구까지 확인."),
        ("사무실 IT:", "소규모 사무실의 네트워크, 계정, 기본 보안.")]),
      ("진행 방식", "steps", [
        ("문의", "WhatsApp으로 문제를 알려주세요. 사진이 있으면 더 좋습니다."),
        ("원격 또는 방문", "가능하면 원격으로, 필요하면 방문 일정을 잡습니다."),
        ("설명", "무엇을 해결했고 무엇을 주의해야 하는지 한국어로 안내합니다.")]),
    ],
    "faq": [
      ("새 아파트 인터넷 개통도 해주나요?", "네. 현지 통신사 개통을 진행하고 모든 방에 Wi-Fi를 설정합니다."),
      ("한국에서도 CCTV를 볼 수 있나요?", "네. 어디서든 볼 수 있도록 안전한 모바일 보기 설정을 해드립니다."),
      ("가정뿐 아니라 사무실도 지원하나요?", "네. 중소 규모 사무실의 네트워크, 보안, 일상 IT를 지원합니다."),
      ("어느 지역까지 지원하나요?", "첸나이 시내와 스리페룸부두르, 오라가담, 이룽가투코타이 산업 벨트입니다.")],
  },
},
}


# ── Privacy policy (needed for the WhatsApp Business Platform / Meta app) ────
PRIVACY = {
    "en": {
        "title": "Privacy Policy | Korean Living Support",
        "desc": "How Korean Living Support (KLS) in Chennai collects, uses and protects the information you share with us on WhatsApp, email and phone.",
        "h1": "Privacy Policy",
        "updated": "Last updated: 21 October 2026",
        "lead": "This policy explains what information Korean Living Support (KLS) collects when you contact us, how we use it, and the choices you have.",
        "sections": [
            ("Who we are", ["Korean Living Support (KLS) is a business based in Chennai, India, that supports Korean companies and families with housing, FRRO and visa paperwork, translation and business support, security certification consulting and IT support."]),
            ("Information we collect", [
                "When you contact us on WhatsApp, by email or by phone, we collect the information you choose to share, such as:",
                ["Your name, phone number and email address", "Your company name",
                 "Details of the service you ask about, for example housing preferences, visa type, arrival dates or the IT problem you describe",
                 "The messages, photos and files you send us"]]),
            ("Our WhatsApp assistant", [
                "Our WhatsApp number uses an automated assistant, provided through the WhatsApp Business Platform by Meta, to welcome you and ask a few questions about your enquiry. It tells you it is the KLS assistant, and you can ask to talk to a person at any time. Your answers are passed to our team, who then contact you personally.",
                "WhatsApp messages are delivered by Meta (WhatsApp). Meta processes them under its own terms and privacy policy."]),
            ("How we use your information", [
                ["To reply to your enquiry and provide the service you request", "To follow up on your request and keep a record of our work for you",
                 "To meet legal and accounting obligations"],
                "We do not sell your personal information, and we do not send you marketing messages without your permission."]),
            ("Who we share it with", [
                "We share information only when it is needed to provide the service you asked for, or when the law requires it. This may include:",
                ["Property owners or agents, when you ask us to find a home",
                 "Government offices and portals, such as FRRO, when you ask us to handle an application for you",
                 "Trusted vendors who carry out work you have requested",
                 "Service providers that host our systems and email, under confidentiality"]]),
            ("How we protect and keep it", [
                "Your information is stored on secured systems with access limited to our team. We keep enquiry records only as long as needed to serve you and to meet legal record-keeping requirements, and then delete them."]),
            ("Your choices and data deletion", [
                "You can ask us at any time to see, correct or delete the information we hold about you, or to stop messaging you. Send your request by WhatsApp or email to the contact details below, and we will act on it within 30 days."]),
            ("Contact", ["Korean Living Support, Chennai, Tamil Nadu, India"]),
            ("Changes to this policy", ["We may update this policy from time to time. The latest version is always on this page, with the date at the top."]),
        ],
    },
    "ko": {
        "title": "개인정보 처리방침 | Korean Living Support",
        "desc": "첸나이 Korean Living Support(KLS)가 WhatsApp, 이메일, 전화로 받은 정보를 어떻게 수집·이용·보호하는지 안내합니다.",
        "h1": "개인정보 처리방침",
        "updated": "최종 업데이트: 2026년 10월 21일",
        "lead": "이 방침은 Korean Living Support(KLS)가 연락을 받을 때 어떤 정보를 수집하는지, 어떻게 이용하는지, 그리고 고객님이 선택할 수 있는 사항을 설명합니다.",
        "sections": [
            ("회사 소개", ["Korean Living Support(KLS)는 인도 첸나이에 있는 회사로, 한국 기업과 가족에게 주거, FRRO·비자 업무, 번역·기업 지원, 보안 인증 컨설팅, IT 지원을 제공합니다."]),
            ("수집하는 정보", [
                "WhatsApp, 이메일, 전화로 연락하실 때 고객님이 직접 알려주시는 정보를 수집합니다. 예:",
                ["성함, 전화번호, 이메일 주소", "회사명",
                 "문의하신 서비스에 관한 내용 (예: 희망 주거 조건, 비자 종류, 입국일, IT 문제 내용)",
                 "보내주신 메시지, 사진, 파일"]]),
            ("WhatsApp 안내 도우미", [
                "KLS의 WhatsApp 번호는 Meta의 WhatsApp Business Platform을 통한 자동 안내 도우미를 사용하여 인사를 드리고 문의 내용에 대해 몇 가지 질문을 드립니다. 도우미는 KLS 안내 도우미임을 밝히며, 언제든지 담당자와의 상담을 요청하실 수 있습니다. 답변 내용은 담당자에게 전달되며, 담당자가 직접 연락드립니다.",
                "WhatsApp 메시지는 Meta(WhatsApp)를 통해 전달되며, Meta는 자체 약관과 개인정보 처리방침에 따라 메시지를 처리합니다."]),
            ("정보의 이용 목적", [
                ["문의에 답변하고 요청하신 서비스를 제공하기 위해", "요청 사항을 후속 처리하고 업무 기록을 보관하기 위해",
                 "법률 및 회계상의 의무를 이행하기 위해"],
                "고객님의 개인정보를 판매하지 않으며, 동의 없이 마케팅 메시지를 보내지 않습니다."]),
            ("정보의 제공", [
                "요청하신 서비스 제공에 필요한 경우나 법률이 요구하는 경우에만 정보를 제공합니다. 예:",
                ["집 구하기를 요청하신 경우 집주인 또는 중개인", "신청 대행을 요청하신 경우 FRRO 등 정부 기관 및 포털",
                 "요청하신 작업을 수행하는 신뢰할 수 있는 협력업체", "비밀유지 조건으로 시스템과 이메일을 운영하는 서비스 제공업체"]]),
            ("정보의 보호 및 보관", [
                "고객님의 정보는 담당자만 접근할 수 있는 보안 시스템에 보관됩니다. 문의 기록은 서비스 제공과 법적 기록 보관에 필요한 기간 동안만 보관한 후 삭제합니다."]),
            ("고객님의 선택 및 정보 삭제", [
                "보유 중인 정보의 열람, 정정, 삭제 또는 메시지 수신 중단을 언제든지 요청하실 수 있습니다. 아래 연락처로 WhatsApp 또는 이메일을 보내주시면 30일 이내에 처리해 드립니다."]),
            ("연락처", ["Korean Living Support, 인도 타밀나두주 첸나이"]),
            ("방침의 변경", ["이 방침은 수시로 변경될 수 있으며, 최신 내용과 날짜는 항상 이 페이지에 게시됩니다."]),
        ],
    },
}

import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="정보통신공사 법령 판별기 Pro", layout="wide")
    st.title("🏗️ 정보통신공사 법령 판별 및 근거 조문 확인")
    st.markdown("건축물 용도와 스펙을 입력하면 관련 법령을 분석하고, **판별 근거가 되는 법령 조문**을 보여드립니다. ")

    # 사이드바 입력창
    st.sidebar.header("📝 1. 건축물 기본 정보")
    build_type = st.sidebar.radio("건축 행위", ["신축", "증축/개축/재축", "대수선"])
    total_area = st.sidebar.number_input("건축물 총 연면적 (㎡)", min_value=0.0, value=1000.0, step=10.0)
    floors = st.sidebar.number_input("건축물 층수 (지상층)", min_value=1, value=1, step=1)
    
    st.sidebar.header("🏢 2. 상세 용도 및 시설")
    building_usage_list = [
        "단독주택", "공동주택", "제1종 근린생활시설", "제2종 근린생활시설", "문화 및 집회시설",
        "종교시설", "판매시설", "운수시설", "의료시설", "교육연구시설",
        "노유자시설", "수련시설", "운동시설", "업무시설", "숙박시설",
        "위락시설", "공장", "창고시설", "위험물저장 및 처리시설", "자동차 관련시설",
        "동물 및 식물관련시설", "자원순환 관련시설", "교정 및 군사시설", "방송통신시설", "발전시설",
        "묘지관련시설", "관광휴게시설", "장례시설", "야영장시설"
    ]
    selected_usage = st.sidebar.selectbox("건축물 용도", building_usage_list)
    
    # --- 조건부 UI 로직 시작 ---
    is_no_telecom_demand = False
    
    # 주거 가능 용도 정의
    residential_list = ["단독주택", "공동주택"]
    
    # 주거용이 아닐 때만 '통신수요 제외' 체크박스 표시
    if selected_usage not in residential_list:
        is_no_telecom_demand = st.sidebar.checkbox("통신수요가 예상되지 아니하는 비주거용 건축물 (야외음악당, 축사, 차고, 창고 등)")
    # --- 조건부 UI 로직 끝 ---
    
    has_basement = st.sidebar.checkbox("지하층(주차장 등)이 포함됨")
    
    num_households = 0
    if selected_usage == "공동주택":
        num_households = st.sidebar.number_input("세대 수 (단지 합계)", min_value=0, value=0)

    st.sidebar.header("🛠️ 3. 공사 및 환경 정보")
    zone_type = st.sidebar.selectbox("용도 지역", ["도시지역", "관리지역", "농림지역", "자연환경보전지역"])
    is_special_zone = st.sidebar.checkbox("지구단위계획/방재지구 등 특수구역")
    
    telecom_purpose = st.sidebar.radio("공사 목적", [
        "일반 건축물의 정보통신·방송 설비",
        "전기통신사업자 역무 제공용",
        "철도/도로/항공 등 기반시설 제어용"
    ])
    
    if st.sidebar.button("🔍 확인하기", type="primary"):
        run_logic_with_law(
            build_type, total_area, floors, selected_usage, 
            has_basement, num_households, zone_type, 
            is_special_zone, telecom_purpose, is_no_telecom_demand
        )

    # 우측 하단 문의사항 추가
    st.markdown("<br><br><div style='text-align: right; color: gray; font-size: 0.8em;'>문의사항: ok043@korea.kr</div>", unsafe_allow_html=True)

def show_law_box(title, law_name, article, content):
    with st.expander(f"📜 근거 법령: {law_name} {article}"):
        st.caption(f"**[{article}] {title}**")
        st.write(content)

def run_logic_with_law(build_type, total_area, floors, selected_usage, has_basement, num_households, zone_type, is_special_zone, telecom_purpose, is_no_telecom_demand):
    st.subheader(f"📊 [{selected_usage}] 판별 결과")
    
    multi_use_list = ["문화 및 집회시설", "종교시설", "판매시설", "운수시설", "의료시설", "숙박시설"]

    is_report_target = False
    report_law_content = ""
    if build_type == "신축" and zone_type != "도시지역" and not is_special_zone and total_area < 200.0 and floors < 3:
        is_report_target = True
        report_law_content = "관리지역, 농림지역 또는 자연환경보전지역에서 연면적이 200제곱미터 미만이고 3층 미만인 건축물의 건축"
    elif build_type == "대수선" and total_area < 200.0 and floors < 3:
        is_report_target = True
        report_law_content = "연면적 200제곱미터 미만이고 3층 미만인 건축물의 대수선"
    
    is_permit_target = not is_report_target

    st.write("#### 1. 의무 설치 대상 설비 확인")
    
    # 구내통신선로 판별
    if is_no_telecom_demand:
        st.info("💡 **구내통신선로설비 설치 제외 대상**")
        show_law_box("구내통신선로설비의 설치대상", "방송통신설비의 기술기준에 관한 규정", "제17조", 
                     "다만, 야외음악당ㆍ축사ㆍ차고ㆍ창고 등 통신수요가 예상되지 아니하는 비주거용 건축물은 제외한다.")
    elif is_permit_target:
        st.success("✅ **구내통신선로설비** 설치 대상")
        show_law_box("구내통신선로설비의 설치대상", "방송통신설비의 기술기준에 관한 규정", "제17조", 
                     "「전기통신사업법」 제69조제1항에 따라 구내통신선로설비 등을 갖추어야 하는 건축물은 「건축법」 제11조제1항에 따라 허가를 받아 건축하는 건축물로 한다.")

    is_mobile = (total_area >= 1000 and (selected_usage in multi_use_list or floors >= 16 or has_basement)) or (num_households >= 500)
    if is_mobile:
        st.success("✅ **이동통신구내선로설비** 설치 대상")
        show_law_box("구내용 이동통신설비의 설치대상", "방송통신설비의 기술기준에 관한 규정", "제17조의2", 
                     "연면적 1,000㎡ 이상인 다중이용 건축물, 지하층이 있는 건축물 또는 500세대 이상의 주택단지 등은 이동통신 구내선로설비를 설치하여야 한다.")

    is_broad = (selected_usage == "공동주택") or (total_area >= 5000 and selected_usage in ["업무시설", "숙박시설"])
    if is_broad:
        st.success("✅ **방송공동수신설비** 설치 대상")
        show_law_box("건축설비 설치의 원칙", "건축법 시행령", "제87조", 
                     "공동주택, 바닥면적의 합계가 5천제곱미터 이상으로서 업무시설이나 숙박시설의 용도로 쓰는 건축물에는 방송 공동수신설비를 설치하여야 한다.")

    st.divider()

    st.write("#### 2. 행정 절차 및 감리 대상 확인")
    
    is_supervision = True
    if telecom_purpose == "일반 건축물의 정보통신·방송 설비":
        if floors < 6 and total_area < 5000.0:
            is_supervision = False
            
    if total_area <= 150.0 or is_report_target:
        st.info("🎉 **착공 전 설계도 확인 및 사용전검사 면제**")
        if is_report_target:
            show_law_box("건축신고", "건축법", "제14조", report_law_content)
        show_law_box("대상공사의 제외", "정보통신공사업법 시행령", "제35조 제1항", "연면적 150제곱미터 이하 또는 건축법 제14조에 따른 신고대상건축물은 제외한다.")
    else:
        st.warning("📋 **[착공 전 설계도 확인] 대상**")
        show_law_box("착공전 설계도 확인", "정보통신공사업법 시행령", "제35조 제1항", "구내통신·이동통신·방송공동수신설비 공사는 착공 전 설계도를 지자체에 제출하여 확인받아야 한다.")

        if is_supervision:
            st.success("✨ **[사용전검사] 면제 (감리결과보고서 대체)**")
            show_law_box("사용전검사의 제외", "정보통신공사업법 시행령", "제35조 제1항 제2호 나목", "감리를 실시한 공사는 사용전검사를 감리결과보고서 제출로 갈음한다.")
        else:
            st.error("🔍 **[사용전검사] 현장 검사 대상**")
            show_law_box("감리대상인 공사의 범위", "정보통신공사업법 시행령", "제8조", "감리 면제 대상 공사(6층 미만, 5,000㎡ 미만 등)는 지자체의 사용전검사를 직접 받아야 한다.")

    st.write("---")

if __name__ == "__main__":
    main()
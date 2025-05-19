import streamlit as st
st.title("Exams at UoW")

faqs = {
    "When are the exam periods?": "There are three main exam periods each academic year when the University runs on-site exams and online timed assessments.\n\n- January: Semester 1 exams\n- May: Semester 2 exams\n- Summer reassessment period\n\nFor all the key academic dates, please view our term dates.",
    
    "When and where will exam timetables be available?": "Exam timetables and their publication dates are provided on our Exam timetables page.\n\n- The timetable for exams taking place in January will be published in November.\n- The timetable for exams in May will be published in March.\n- The timetable for the reassessment period will be available after results are published in June.",
    
    "What days of the week are exams scheduled on?": "Exams are held Monday to Friday. There are no exams on weekends or public holidays.",
    
    "What time do exams start?": "Both on-site exams and online timed assessments normally start as follows, but check your exam timetable carefully in case of changes:\n\n- Monday-Thursday: 10 AM, 2 PM, and 6 PM\n- Friday: 10 AM and 2 PM\n\nYou may have an exam scheduled in any of these slots, including the evening, even if you only study during the day.",
    
    "What should I do if I have a clash in my exam timetable?": "Information about exam clashes is provided on our Exam Clashes page.",
    
    "What will happen if I require Individual Examination Arrangements (IEAs)?": "If you have a long-term disability or condition, register with Disability Learning Support so your needs can be assessed, and arrangements made in time. Refer to the Individual Exam Arrangements page for details.\n\n- If you are entitled to additional time for an on-site exam, this is already included in online assessments with a 24-hour submission window.\n- If your exam is a shorter time-limited assessment, you will be advised of any additional time allowed.\n- If you require a scribe/amanuensis, Disability Learning Services (DLS) will ensure assistive technology is available to support you.",
    
    "I've broken my arm, how will I take my exam?": "If you’ve had an accident that may affect your ability to sit exams, check our Individual Exam Arrangements for Temporary Conditions page for details on what to do next.",
    
    "I'm not well and have an exam later today, what should I do?": "If you feel too ill to sit the exam, follow the mitigating circumstances procedure.\n\nIf you decide to sit the exam, note that the University operates a 'fit to sit' policy. This means if you attend the exam, you are considered fit to do so and cannot later submit a mitigating circumstances claim for that assessment.",
    
    "Why do I have two exams in one day?": "Due to the large number of exams scheduled in a short timeframe, some students may have two exams in one day. However, you would not normally be expected to sit more than two exams in a single day."
}

for question, answer in faqs.items():
    with st.expander(question):
        st.write(answer)

% CampusMind - Student Eligibility Knowledge Base
% Rule: A student is eligible if attendance is at least 75% and CGPA is at least 6.5
eligible(Student) :-
    attendance(Student, Att),
    cgpa(Student, Cgpa),
    Att >= 75,
    Cgpa >= 6.5.

% Sample student facts: attendance (percentage), cgpa (scale 0-10)
attendance(aarav, 85).
cgpa(aarav, 8.2).

attendance(diya, 72).
cgpa(diya, 7.8).

attendance(rohan, 90).
cgpa(rohan, 6.1).

attendance(ananya, 78).
cgpa(ananya, 7.0).

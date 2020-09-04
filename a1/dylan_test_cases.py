from course import Student, Course
from survey import Answer, Question, MultipleChoiceQuestion, NumericQuestion, \
    YesNoQuestion, CheckboxQuestion, Survey
from criterion import HomogeneousCriterion, HeterogeneousCriterion, \
    LonelyMemberCriterion, InvalidAnswerError
from grouper import slice_list, windows, Grouper, AlphaGrouper, RandomGrouper, \
    GreedyGrouper, WindowGrouper, Grouping, Group

import pytest
from typing import List, Set, FrozenSet




def test___str__single_string() -> None:
    student = Student(5, "2")
    assert str(student) == "2"


def test___str__regular_string() -> None:
    student = Student(5, "Hello")
    assert str(student) == "Hello"


def test_has_answer() -> None:
    a1 = Answer(5)
    q1 = NumericQuestion(3, 'How old is Jio?', 5, 8)
    s1 = Student(1, 'Dylan')
    s1.set_answer(q1, a1)
    assert s1.has_answer(q1)


def test_has_answer_not() -> None:
    q1 = NumericQuestion(3, 'How old is Jio?', 5, 8)
    s1 = Student(1, 'Dylan')
    assert not s1.has_answer(q1)


def test_has_answer_not_valid() -> None:
    a1 = Answer(['Hello'])
    q1 = NumericQuestion(3, 'How old is Jio?', 5, 8)
    s1 = Student(1, 'Dylan')
    s1.set_answer(q1, a1)
    assert s1.has_answer(q1) == False


def test_set_answer_bool() -> None:
    a1 = Answer(True)
    q1 = YesNoQuestion(3, 'Is Dylan old?')
    s1 = Student(1, 'Dylan')
    s1.set_answer(q1, a1)
    assert s1.get_answer(q1) == a1


def test_set_answer_num() -> None:
    a1 = Answer(5)
    q1 = NumericQuestion(3, 'How old is Jio?', 5, 8)
    s1 = Student(1, 'Dylan')
    s1.set_answer(q1, a1)
    assert s1.get_answer(q1) == a1


def test_get_answer() -> None:
    s1 = Student(1, 'Dylan')
    a1 = Answer(True)
    q1 = YesNoQuestion(3, 'Is that it?')
    s1.set_answer(q1, a1)
    assert s1.get_answer(q1) == a1


def test_get_answer_when_none() -> None:
    s1 = Student(1, 'Dylan')
    q1 = YesNoQuestion(3, 'Is that it?')
    assert s1.get_answer(q1) is None


def test_enroll_students_was_empty() -> None:
    c1 = Course('CS148')
    s1 = Student(1, '1')
    s2 = Student(2, '1')
    s3 = Student(3, '1')
    c1.enroll_students([s1, s2, s3])
    assert c1.students == [s1, s2, s3]


# def test_enroll_students_two_in_argument() -> None:
#     c1 = Course('CS148')
#     s1 = Student(1, '1')
#     s2 = Student(2, '1')
#     s3 = Student(2, '1')
#     c1.enroll_students([s1, s2, s3])
#     assert c1.students == []


def test_enroll_students_1_in_argument_1_lst() -> None:
    c1 = Course('CS148')
    s1 = Student(1, '1')
    c1.enroll_students([s1])
    assert c1.students == [s1]
    s2 = Student(1, '1')
    s3 = Student(2, '1')
    c1.enroll_students([s2, s3])
    assert c1.students == [s1, s2, s3]


def test_all_answered() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 29, 31)
    q2 = YesNoQuestion(2, 'Is Dylan old?')
    a1 = Answer(30)
    a2 = Answer(True)
    a3 = Answer(False)
    a4 = Answer(29)
    sur = Survey([q1, q2])
    s1 = Student(1, 'Dylan')
    s2 = Student(2, 'Kelly')
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a4)
    s2.set_answer(q2, a3)
    c1 = Course('silly')
    c1.enroll_students([s1, s2])
    assert c1.all_answered(sur)


def test_all_answered_not() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 29, 31)
    q2 = YesNoQuestion(2, 'Is Dylan old?')
    a1 = Answer(30)
    a2 = Answer(True)
    a3 = Answer(29)
    a4 = Answer(False)
    a5 = Answer(31)
    sur = Survey([q1, q2])
    s1 = Student(1, 'Dylan')
    s2 = Student(2, 'Kelly')
    s3 = Student(3, 'Steve')
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a4)
    c1 = Course('silly')
    c1.enroll_students([s1, s2, s3])
    assert not c1.all_answered(sur)


def test_all_answered_one_invalid() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 29, 31)
    q2 = YesNoQuestion(2, 'Is Dylan old?')
    a1 = Answer(30)
    a2 = Answer(True)
    a3 = Answer(29)
    a4 = Answer(False)
    a5 = Answer(31)
    sur = Survey([q1, q2])
    s1 = Student(1, 'Dylan')
    s2 = Student(2, 'Kelly')
    s3 = Student(3, 'Steve')
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s3.set_answer(q1, a4)
    s3.set_answer(q2, a5)
    c1 = Course('silly')
    c1.enroll_students([s1, s2, s3])
    assert c1.all_answered(sur) == False


def test_get_students_some() -> None:
    c1 = Course('CS148')
    s1 = Student(6, '6')
    s2 = Student(5, '5')
    s3 = Student(7, '7')
    s4 = Student(4, '4')
    s5 = Student(10, '10')
    c1.enroll_students([s1, s2, s3, s4, s5])
    assert c1.students == [s1, s2, s3, s4, s5]
    assert c1.get_students() == (s4, s2, s1, s3, s5)


def test_get_students_one() -> None:
    c1 = Course('CS148')
    s1 = Student(6, '6')
    c1.enroll_students([s1])
    assert c1.students == [s1]
    assert c1.get_students() == (s1,)


def test_get_students_empty() -> None:
    c1 = Course('CS148')
    assert c1.get_students() == ()


# def test_mcq_str_() -> None:
#     options = ['March 16, 1990', 'March 18, 2019']
#     txt1 = 'When was Dylan Hollohan born?'
#     mcq = MultipleChoiceQuestion(1, txt1, options)
#     str1 = str(mcq)
#     str2 = '1. When was Dylan Hollohan born? Your answer should be one of' \
#            ' those below:\n1. March 16, 1990\n2. March 18, 2019'
#     assert str1 == str2


def test_mcq_validate_ans_not_valid() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('March 20')
    assert mcq.validate_answer(a1) == False


def test_mcq_validate_ans_valid() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('March 18, 2019')
    assert mcq.validate_answer(a1)


def test_mcq_validate_ans__not_valid2() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer(True)
    assert mcq.validate_answer(a1) == False


def test_mcq_get_similarity_same() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('March 16, 1990')
    a2 = Answer('March 16, 1990')
    assert mcq.get_similarity(a1, a2) == 1.0


def test_mcq_get_similarity_diff() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('March 16, 1990')
    a2 = Answer('March 18, 1990')
    assert mcq.get_similarity(a1, a2) == 0.0


# def test_numq_str_() -> None:
#     txt1 = 'When was Dylan Hollohan born?'
#     numq = NumericQuestion(1, txt1, 16, 18)
#     str1 = str(numq)
#     str2 = str(numq.id) + '. ' + numq.text + ' Your answer should be an ' \
#                                              'integer between ' + str(16) + \
#         ' and ' + str(18) + '.'
#     assert str1 == str2


def test_numq_validate_ans_valid_edge() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 17)
    a1 = Answer(15)
    assert numq.validate_answer(a1)


def test_numq_validate_ans_valid_mid() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 17)
    a1 = Answer(16)
    assert numq.validate_answer(a1)


def test_numq_validate_ans_valid_end() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 17)
    a1 = Answer(17)
    assert numq.validate_answer(a1)


def test_numq_validate_ans_not_valid() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 17)
    a1 = Answer(18)
    assert numq.validate_answer(a1) == False


def test_numq_validate_ans_not_valid_not_num() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 17)
    a1 = Answer('hello')
    assert numq.validate_answer(a1) == False


def test_numq_get_similarity_same() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 19)
    a1 = Answer(15)
    a2 = Answer(15)
    assert numq.get_similarity(a1, a2) == 1.0


def test_numq_get_similarity_max_min() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 19)
    a1 = Answer(15)
    a2 = Answer(19)
    assert numq.get_similarity(a1, a2) == 0.0


def test_numq_get_similarity_mid() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 19)
    a1 = Answer(17)
    a2 = Answer(19)
    assert numq.get_similarity(a1, a2) == 0.5


def test_numq_get_similarity_mid_mid() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 15, 19)
    a1 = Answer(17)
    a2 = Answer(18)
    assert numq.get_similarity(a1, a2) == 0.75


# def test_yn_str() -> None:
#     txt1 = 'Was Dylan Hollohan born?'
#     ynq = YesNoQuestion(1, txt1)
#     str1 = str(ynq)
#     str2 = str(ynq.id) + '. ' + ynq.text + " Your answer should be a boolean." \
#                                            " True means 'yes' and False means" \
#                                            " 'no'."
#     assert str1 == str2


def test_ynq_validate_ans_valid() -> None:
    txt1 = 'Was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer(True)
    assert ynq.validate_answer(a1)


def test_ynq_validate_ans_valid1() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer(False)
    assert ynq.validate_answer(a1)


def test_ynq_validate_ans_not_valid() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer('Hello')
    with pytest.raises(InvalidAnswerError):
        ynq.validate_answer(a1)


def test_ynq_validate_ans_not_valid() -> None:
    txt1 = 'Was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer(3)
    assert ynq.validate_answer(a1) == False


def test_ysq_get_similarity_same() -> None:
    txt1 = 'Was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1, )
    a1 = Answer(True)
    a2 = Answer(True)
    assert ynq.get_similarity(a1, a2) == 1.0


def test_ysq_get_similarity_not_same() -> None:
    txt1 = 'Was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1, )
    a1 = Answer(True)
    a2 = Answer(False)
    assert ynq.get_similarity(a1, a2) == 0.0


def test_ysq_get_similarity_not_same2() -> None:
    txt1 = 'Was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1, )
    a1 = Answer(False)
    a2 = Answer(True)
    assert ynq.get_similarity(a1, a2) == 0.0


# def test_cbq_str_() -> None:
#     options = ['March 16, 1990', 'March 18, 2019']
#     txt1 = 'When was Dylan Hollohan born (twice)?'
#     cbq = CheckboxQuestion(1, txt1, options)
#     str1 = str(cbq)
#     str2 = '1. When was Dylan Hollohan born (twice)? Choose the correct ' \
#            'answer(s) below:\n1. March 16, 1990\n2. March 18, 2019'
#     assert str1 == str2


def test_cbq_validate_ans_valid() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 16, 1990', 'March 18, 2019'])
    assert cbq.validate_answer(a1)


def test_cbq_validate_ans_valid_second() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 18, 2019'])
    assert cbq.validate_answer(a1)


def test_cbq_validate_ans_valid_third() -> None:
    options = ['March 16, 1990', 'March 18, 2019', 'March 20, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 16, 1990', 'March 20, 2019'])
    assert cbq.validate_answer(a1)


def test_cbq_validate_ans_not_valid() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 16, 1990', 'March 19, 2019'])
    assert cbq.validate_answer(a1) == False


def test_cbq_validate_ans_not_valid_input() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 16, 2019'])
    assert cbq.validate_answer(a1) == False


def test_cbq_validate_ans_not_valid_dupl() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['March 16, 1990', 'March 16, 1990'])
    assert cbq.validate_answer(a1) == False


def test_cbq_validate_ans_not_valid_empty() -> None:
    options = ['March 16, 1990', 'March 18, 2019']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer([])
    assert cbq.validate_answer(a1) == False


def test_cbq_get_similarity_same() -> None:
    options = ['1', '2', '3', '4']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['1', '3'])
    a2 = Answer(['1', '3'])
    assert cbq.get_similarity(a1, a2) == 1.0


def test_cbq_get_similarity_tot_diff() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['a', 'b'])
    a2 = Answer(['c', 'd'])
    assert cbq.get_similarity(a1, a2) == 0.0


def test_cbq_get_similarity_one_four() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['a', 'b'])
    a2 = Answer(['b', 'c', 'd'])
    assert cbq.get_similarity(a1, a2) == .25


def test_cbq_get_similarity_two_five() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['a', 'b', 'e'])
    a2 = Answer(['a', 'b', 'c', 'd'])
    assert cbq.get_similarity(a1, a2) == .40


def test_answer_is_valid_cbq_true() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['a', 'b'])
    assert a1.is_valid(cbq)


def test_answer_is_valid_cbq_false() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born (twice)?'
    cbq = CheckboxQuestion(1, txt1, options)
    a1 = Answer(['a', 'f'])
    assert a1.is_valid(cbq) == False


def test_answer_is_valid_mcq_true() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('a')
    assert a1.is_valid(mcq)


def test_answer_is_valid_mcq_false() -> None:
    options = ['a', 'b', 'c', 'd', 'e']
    txt1 = 'When was Dylan Hollohan born?'
    mcq = MultipleChoiceQuestion(1, txt1, options)
    a1 = Answer('f')
    assert a1.is_valid(mcq) == False


def test_answer_is_valid_yn_true() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer(True)
    assert a1.is_valid(ynq)


def test_answer_is_valid_yn_false_list() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer([False])
    assert a1.is_valid(ynq) == False


def test_answer_is_valid_yn_false_num() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    ynq = YesNoQuestion(1, txt1)
    a1 = Answer(5)
    assert a1.is_valid(ynq) == False


def test_answer_is_valid_num_true() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 10, 15)
    a1 = Answer(13)
    assert a1.is_valid(numq)


def test_answer_is_valid_num_false() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 10, 15)
    a1 = Answer('a')
    assert a1.is_valid(numq) == False


def test_answer_is_valid_num_false_outside() -> None:
    txt1 = 'When was Dylan Hollohan born?'
    numq = NumericQuestion(1, txt1, 10, 15)
    a1 = Answer(16)
    assert a1.is_valid(numq) == False


# def test_answer_is_valid_general() -> None:
#     txt1 = 'When was Dylan Hollohan born?'
#     genq = Question(1, txt1)
#     a1 = Answer(16)
#     assert not a1.is_valid(genq)


def test_score_answers_homogeneous() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c', 'd'])
    ans = [a1, a2, a3, a4]
    h = HomogeneousCriterion()
    assert h.score_answers(q1, ans) == .50


def test_score_answers_homogeneous_other() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HomogeneousCriterion()
    assert round(h.score_answers(q1, ans), 3) == .583


def test_score_answers_homogeneous_error_not_in() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'e'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HomogeneousCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_score_answers_homogeneous_error_bad_input() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(True)
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HomogeneousCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_heterogeneous_score_answers() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c', 'd'])
    ans = [a1, a2, a3, a4]
    h = HeterogeneousCriterion()
    assert h.score_answers(q1, ans) == .50


def test_heterogeneous_score_answers_other() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HeterogeneousCriterion()
    assert round(h.score_answers(q1, ans), 3) == 0.417


def test_score_answers_heterogeneous_error_not_in() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'e'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HeterogeneousCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_score_answers_heterogeneous_error_bad_input() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(True)
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = HeterogeneousCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_lonely_member_score_answers() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a', 'b'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    assert h.score_answers(q1, ans) == 0.0


def test_lonely_member_score_answers_other() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a'])
    a3 = Answer(['a', 'b', 'c'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    assert h.score_answers(q1, ans) == 1.0


def test_lonely_member_score_answers_bools_works() -> None:
    q1 = YesNoQuestion(1, 'Which sports..?')
    a1 = Answer(True)
    a2 = Answer(True)
    a3 = Answer(False)
    a4 = Answer(False)
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    assert h.score_answers(q1, ans) == 1.0


def test_lonely_member_score_answers_bools_fails() -> None:
    q1 = YesNoQuestion(1, 'Which sports..?')
    a1 = Answer(True)
    a2 = Answer(False)
    a3 = Answer(False)
    a4 = Answer(False)
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    assert h.score_answers(q1, ans) == 0.0


def test_lonely_member_score_answers_bools_error() -> None:
    q1 = YesNoQuestion(1, 'Which sports..?')
    a1 = Answer(True)
    a2 = Answer(False)
    a3 = Answer('Hello')
    a4 = Answer(False)
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_lonely_member_another_error() -> None:
    options = ['a', 'b', 'c', 'd']
    q1 = CheckboxQuestion(1, 'Which sports..?', options)
    a1 = Answer(['a'])
    a2 = Answer(['a'])
    a3 = Answer(['a', 'b', 'e'])
    a4 = Answer(['a', 'b', 'c'])
    ans = [a1, a2, a3, a4]
    h = LonelyMemberCriterion()
    with pytest.raises(InvalidAnswerError):
        h.score_answers(q1, ans)


def test_group_init() -> None:
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    s3 = Student(3, '3')
    lst_of_stu = [s1, s2, s3]
    g = Group(lst_of_stu)
    assert g.get_members() == [s1, s2, s3]


# def test_group_init_dup() -> None:
#     s1 = Student(1, '1')
#     s2 = Student(1, '2')
#     s3 = Student(3, '3')
#     lst_of_stu = [s1, s2, s3]
#     g = Group(lst_of_stu)
#     assert g.get_members() == [s1, s3]


# def test_group_init_mult_dup() -> None:
#     s1 = Student(1, '1')
#     s2 = Student(1, '2')
#     s3 = Student(3, '3')
#     s4 = Student(4, '4')
#     s5 = Student(5, '5')
#     s6 = Student(5, '5')
#     s7 = Student(6, '6')
#     lst_of_stu = [s1, s2, s3, s4, s5, s6, s7]
#     g = Group(lst_of_stu)
#     assert g.get_members() == [s1, s3, s4, s5, s7]


def test_group_len() -> None:
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    s3 = Student(3, '3')
    lst_of_stu = [s1, s2, s3]
    g = Group(lst_of_stu)
    assert len(g) == 3


# def test_group_len_w_duplicate() -> None:
#     s1 = Student(1, '1')
#     s2 = Student(1, '2')
#     s3 = Student(3, '3')
#     lst_of_stu = [s1, s2, s3]
#     g = Group(lst_of_stu)
#     assert len(g) == 2


def test_group_contains() -> None:
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    s3 = Student(3, '3')
    lst_of_stu = [s1, s2, s3]
    g = Group(lst_of_stu)
    assert s2 in g


def test_group_contains_not() -> None:
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    s3 = Student(3, '3')
    s4 = Student(4, '4')
    lst_of_stu = [s1, s2, s3]
    g = Group(lst_of_stu)
    assert s4 not in g


# def test_group_str() -> None:
#     s1 = Student(1, 'Dylan Hollohan')
#     s2 = Student(2, 'Kelly L')
#     s3 = Student(3, 'Anirudh C')
#     s4 = Student(4, 'Arjun B')
#     lst_of_stu = [s1, s2, s3, s4]
#     g = Group(lst_of_stu)
#     str1 = 'Dylan Hollohan, Kelly L, Anirudh C, Arjun B'
#     assert str(g) == str1


def test_group_get_members() -> None:
    s1 = Student(1, 'Dylan Hollohan')
    s2 = Student(2, 'Kelly L')
    s3 = Student(3, 'Anirudh C')
    s4 = Student(4, 'Arjun B')
    lst_of_stu = [s1, s2, s3, s4]
    g = Group(lst_of_stu)
    assert g.get_members() == [s1, s2, s3, s4]
    assert id(g.get_members()) != id(lst_of_stu)


def test_grouping_len() -> None:
    s1 = Student(1, 'Dylan Hollohan')
    s2 = Student(2, 'Kelly L')
    s3 = Student(3, 'Anirudh C')
    s4 = Student(4, 'Arjun B')
    lst1 = [s1, s2]
    lst2 = [s3, s4]
    g1 = Group(lst1)
    g2 = Group(lst2)
    g3 = Grouping()
    assert len(g3) == 0
    g3.add_group(g1)
    g3.add_group(g2)
    assert len(g3) == 2


# def test_grouping_str_one_group() -> None:
#     s1 = Student(1, 'Dylan Hollohan')
#     s2 = Student(2, 'Kelly L')
#     s3 = Student(3, 'Anirudh C')
#     s4 = Student(4, 'Arjun B')
#     lst1 = [s1, s2, s3, s4]
#     g1 = Group(lst1)
#     g3 = Grouping()
#     g3.add_group(g1)
#     assert str(g3) == 'Dylan Hollohan, Kelly L, Anirudh C, Arjun B'


# def test_grouping_str_two_groups() -> None:
#     s1 = Student(1, 'Dylan Hollohan')
#     s2 = Student(2, 'Kelly L')
#     s3 = Student(3, 'Anirudh C')
#     s4 = Student(4, 'Arjun B')
#     lst1 = [s1, s2]
#     lst2 = [s3, s4]
#     g1 = Group(lst1)
#     g2 = Group(lst2)
#     g3 = Grouping()
#     g3.add_group(g1)
#     g3.add_group(g2)
#     assert str(g3) == 'Dylan Hollohan, Kelly L\nAnirudh C, Arjun B'


def test_grouping_add_group_1() -> None:
    s1 = Student(1, 'Dylan Hollohan')
    s2 = Student(2, 'Kelly L')
    s3 = Student(3, 'Anirudh C')
    s4 = Student(4, 'Arjun B')
    lst1 = [s1, s2, s3, s4]
    g1 = Group(lst1)
    g3 = Grouping()
    assert g3.add_group(g1)


def test_grouping_add_groups_two_groups() -> None:
    s1 = Student(1, 'Dylan Hollohan')
    s2 = Student(2, 'Kelly L')
    s3 = Student(3, 'Anirudh C')
    s4 = Student(4, 'Arjun B')
    lst1 = [s1, s2]
    lst2 = [s3, s4]
    g1 = Group(lst1)
    g2 = Group(lst2)
    g3 = Grouping()
    assert g3.add_group(g1)
    assert g3.add_group(g2)


def test_grouping_get_groups_two_groups() -> None:
    s1 = Student(1, 'Dylan Hollohan')
    s2 = Student(2, 'Kelly L')
    s3 = Student(3, 'Anirudh C')
    s4 = Student(4, 'Arjun B')
    lst1 = [s1, s2]
    lst2 = [s3, s4]
    g1 = Group(lst1)
    g2 = Group(lst2)
    g3 = Grouping()
    g3.add_group(g1)
    g3.add_group(g2)
    assert g3.get_groups() == [g1, g2]


def test_survey_len() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    ynq = YesNoQuestion(3, '3')
    cbq = CheckboxQuestion(4, '4', ['4', '5', '6'])
    lst = [mcq, numq, ynq, cbq]
    sur = Survey(lst)
    assert len(sur) == 4


def test_survey_len_zero() -> None:
    lst = []
    sur = Survey(lst)
    assert len(sur) == 0


def test_survey_contains_does() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    ynq = YesNoQuestion(3, '3')
    cbq = CheckboxQuestion(4, '4', ['4', '5', '6'])
    other = Question(2, '2')
    lst = [mcq, numq, ynq, cbq]
    sur = Survey(lst)
    assert other in sur


def test_survey_contains_does_not() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    ynq = YesNoQuestion(3, '3')
    cbq = CheckboxQuestion(4, '4', ['4', '5', '6'])
    other = Question(5, '10')
    lst = [mcq, numq, ynq, cbq]
    sur = Survey(lst)
    assert other not in sur


# def test_survey_str() -> None:
#
#     numq = NumericQuestion(1, 'How much?', 5, 10)
#     numq1 = NumericQuestion(2, 'How much?', 6, 11)
#     numq2 = NumericQuestion(3, 'How much?', 7, 12)
#     lst = [numq, numq1, numq2]
#     sur = Survey(lst)
#     str2 = '1. How much? Your answer should be an integer between 5 and ' \
#            '10.\n2. How much? Your answer should be an integer between 6 and' \
#            ' 11.\n3. How much? Your answer should be an integer between 7 and' \
#            ' 12.\n'
#     assert str(sur) == str2


def test_survey_get_questions_various() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    ynq = YesNoQuestion(3, '3')
    cbq = CheckboxQuestion(4, '4', ['4', '5', '6'])
    lst = [mcq, numq, ynq, cbq]
    sur = Survey(lst)
    assert sur.get_questions() == [mcq, numq, ynq, cbq]


def test_survey_get_questions_num_only() -> None:
    numq = NumericQuestion(1, 'How much?', 5, 10)
    numq1 = NumericQuestion(2, 'How much?', 6, 11)
    numq2 = NumericQuestion(3, 'How much?', 7, 12)
    lst = [numq, numq1, numq2]
    sur = Survey(lst)
    assert sur.get_questions() == [numq, numq1, numq2]


def test_survey_get_criterion_defaults() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    sur = Survey(lst)
    h = HomogeneousCriterion()
    assert type(sur._get_criterion(mcq)) == type(h)
    assert type(sur._get_criterion(numq)) == type(h)


def test_survey_set_criterion() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    survey = Survey(lst)
    het = HeterogeneousCriterion()
    lone = LonelyMemberCriterion()
    assert survey.set_criterion(het, mcq)
    assert survey.set_criterion(lone, numq)


def test_survey_set_criterion_fail() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq]
    survey = Survey(lst)
    het = HeterogeneousCriterion()
    lone = LonelyMemberCriterion()
    assert survey.set_criterion(het, mcq)
    assert not survey.set_criterion(lone, numq)


def test_survey_get_criterion_not_default() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    survey = Survey(lst)
    het = HeterogeneousCriterion()
    lone = LonelyMemberCriterion()
    assert survey.set_criterion(het, mcq)
    assert survey.set_criterion(lone, numq)
    assert type(survey._get_criterion(mcq)) == type(het)
    assert type(survey._get_criterion(numq)) == type(lone)


def test_survey_get_weight_defaults() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    sur = Survey(lst)
    assert sur._get_weight(mcq) == 1
    assert sur._get_weight(numq) == 1


def test_survey_set_weight() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    survey = Survey(lst)
    assert survey.set_weight(5, mcq)
    assert survey.set_weight(10, numq)


def test_survey_set_weight_fail_one() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    q = Question(3, '3')
    lst = [mcq, numq]
    survey = Survey(lst)
    assert survey.set_weight(5, mcq)
    assert survey.set_weight(10, numq)
    assert not survey.set_weight(15, q)


def test_survey_set_weight_fail_negative() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    survey = Survey(lst)
    assert survey.set_weight(5, mcq)
    assert not survey.set_weight(-2, numq)


def test_survey_get_weight_not_default() -> None:
    mcq = MultipleChoiceQuestion(1, '1', ['1', '2', '3'])
    numq = NumericQuestion(2, '2', 5, 10)
    lst = [mcq, numq]
    survey = Survey(lst)
    assert survey.set_weight(5, mcq)
    assert survey.set_weight(10, numq)
    assert survey._get_weight(mcq) == 5
    assert survey._get_weight(numq) == 10


# def test_add_score_one_question_score_first() -> None:
#     q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
#     q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
#     tot_q_score = [0]
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     a1 = Answer(20)
#     a2 = Answer(5)
#     a3 = Answer(30)
#     a4 = Answer(10)
#     s1.set_answer(q1, a1)
#     s1.set_answer(q2, a2)
#     s2.set_answer(q1, a3)
#     s2.set_answer(q2, a4)
#     students = [s1, s2]
#     questions = [q1, q2]
#     survey = Survey(questions)
#     assert survey._add_score_one_question(q1, tot_q_score, students)
#     assert tot_q_score[0] == 0.5
#
#
# def test_add_score_one_question_score_second() -> None:
#     q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
#     q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
#     tot_q_score = [0]
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     a1 = Answer(20)
#     a2 = Answer(5)
#     a3 = Answer(30)
#     a4 = Answer(10)
#     s1.set_answer(q1, a1)
#     s1.set_answer(q2, a2)
#     s2.set_answer(q1, a3)
#     s2.set_answer(q2, a4)
#     students = [s1, s2]
#     questions = [q1, q2]
#     survey = Survey(questions)
#     assert survey._add_score_one_question(q2, tot_q_score, students)
#     assert round(tot_q_score[0], 2) == 0.44
#
#
# def test_add_score_one_question_score_invalid() -> None:
#     q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
#     q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
#     tot_q_score = [0]
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     a1 = Answer(20)
#     a2 = Answer(5)
#     a3 = Answer(30)
#     a4 = Answer(15)
#     s1.set_answer(q1, a1)
#     s1.set_answer(q2, a2)
#     s2.set_answer(q1, a3)
#     s2.set_answer(q2, a4)
#     students = [s1, s2]
#     questions = [q1, q2]
#     survey = Survey(questions)
#     assert not survey._add_score_one_question(q2, tot_q_score, students)
#
#
# def test_add_score_one_question_score_invalid_other() -> None:
#     q1 = CheckboxQuestion(1, 'How old is Dylan?', ['a', 'b', 'c'])
#     tot_q_score = [0]
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     a1 = Answer(['a', 'b'])
#     a2 = Answer(['a', 'd'])
#     s1.set_answer(q1, a1)
#     s2.set_answer(q1, a2)
#     students = [s1, s2]
#     questions = [q1]
#     survey = Survey(questions)
#     assert not survey._add_score_one_question(q1, tot_q_score, students)


def test_add_score_students_defaults() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(20)
    a2 = Answer(5)
    a3 = Answer(30)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    students = [s1, s2]
    questions = [q1, q2]
    survey = Survey(questions)
    assert round(survey.score_students(students), 2) == 0.47


def test_add_score_students_het() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(20)
    a2 = Answer(5)
    a3 = Answer(30)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    students = [s1, s2]
    questions = [q1, q2]
    survey = Survey(questions)
    h = HeterogeneousCriterion()
    survey.set_criterion(h, q1)
    survey.set_criterion(h, q2)
    assert round(survey.score_students(students), 2) == 0.53


def test_add_score_students_het_heavy() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(20)
    a2 = Answer(5)
    a3 = Answer(30)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    students = [s1, s2]
    questions = [q1, q2]
    survey = Survey(questions)
    h = HeterogeneousCriterion()
    survey.set_criterion(h, q1)
    survey.set_criterion(h, q2)
    survey.set_weight(2, q1)
    survey.set_weight(3, q2)
    assert round(survey.score_students(students), 2) == 1.33


def test_add_score_students_lonely_heavy() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 1, 10)
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(20)
    a2 = Answer(10)
    a3 = Answer(30)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    students = [s1, s2]
    questions = [q1, q2]
    survey = Survey(questions)
    l = LonelyMemberCriterion()
    survey.set_criterion(l, q1)
    survey.set_criterion(l, q2)
    survey.set_weight(3, q1)
    survey.set_weight(2, q2)
    assert round(survey.score_students(students), 2) == 1.00


def test_score_grouping_defaults() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, '1')
    a1 = Answer(20)
    a2 = Answer(5)
    s2 = Student(2, '2')
    a3 = Answer(30)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    grp1 = Group([s1, s2])
    s3 = Student(3, '3')
    a5 = Answer(20)
    a6 = Answer(5)
    s4 = Student(4, '4')
    a7 = Answer(30)
    a8 = Answer(10)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a6)
    s4.set_answer(q1, a7)
    s4.set_answer(q2, a8)
    grp2 = Group([s3, s4])
    s5 = Student(5, '5')
    a9 = Answer(20)
    a10 = Answer(5)
    s6 = Student(6, '6')
    a11 = Answer(30)
    a12 = Answer(10)
    s5.set_answer(q1, a9)
    s5.set_answer(q2, a10)
    s6.set_answer(q1, a11)
    s6.set_answer(q2, a12)
    grp3 = Group([s5, s6])
    g = Grouping()
    g.add_group(grp1)
    g.add_group(grp2)
    g.add_group(grp3)
    questions = [q1, q2]
    survey = Survey(questions)
    assert round(survey.score_grouping(g), 2) == 0.50


def test_score_grouping_one_diff() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, '1')
    a1 = Answer(20)
    a2 = Answer(0)
    s2 = Student(2, '2')
    a3 = Answer(40)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    grp1 = Group([s1, s2])
    s3 = Student(3, '3')
    a5 = Answer(20)
    a6 = Answer(5)
    s4 = Student(4, '4')
    a7 = Answer(30)
    a8 = Answer(10)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a6)
    s4.set_answer(q1, a7)
    s4.set_answer(q2, a8)
    grp2 = Group([s3, s4])
    s5 = Student(5, '5')
    a9 = Answer(20)
    a10 = Answer(5)
    s6 = Student(6, '6')
    a11 = Answer(30)
    a12 = Answer(10)
    s5.set_answer(q1, a9)
    s5.set_answer(q2, a10)
    s6.set_answer(q1, a11)
    s6.set_answer(q2, a12)
    grp3 = Group([s5, s6])
    g = Grouping()
    g.add_group(grp1)
    g.add_group(grp2)
    g.add_group(grp3)
    questions = [q1, q2]
    survey = Survey(questions)
    assert round(survey.score_grouping(g), 2) == 0.33


def test_score_grouping_none() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    g = Grouping()
    questions = [q1, q2]
    survey = Survey(questions)
    assert round(survey.score_grouping(g), 2) == 0.00


def test_slice_list_mod() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    new_lst = slice_list(lst, 3)
    assert new_lst == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_slice_list_uneven() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    new_lst = slice_list(lst, 3)
    assert new_lst == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]


def test_slice_list_uneven_bigger() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    new_lst = slice_list(lst, 3)
    assert new_lst == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11]]


def test_slice_list_even_bigger() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    new_lst = slice_list(lst, 4)
    assert new_lst == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11]]


def test_slice_list_even_mod() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8]
    new_lst = slice_list(lst, 4)
    assert new_lst == [[1, 2, 3, 4], [5, 6, 7, 8]]


def test_slice_list_same_as_len() -> None:
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    new_lst = slice_list(lst, 10)
    assert new_lst == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]


def test_windows_3() -> None:
    lst = [1, 2, 3, 4, 5, 6]
    new_lst = windows(lst, 3)
    assert new_lst == [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]


def test_windows_4() -> None:
    lst = [1, 2, 3, 4, 5, 6]
    new_lst = windows(lst, 4)
    assert new_lst == [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]


def test_windows_1() -> None:
    lst = [1, 2, 3, 4]
    new_lst = windows(lst, 1)
    assert new_lst == [[1], [2], [3], [4]]


def test_alpha_grouper_make_grouping_uneven() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, 'f')
    s2 = Student(2, 'b')
    s3 = Student(3, 'j')
    s4 = Student(4, 'z')
    s5 = Student(5, 'a')
    s6 = Student(6, 'n')
    c1 = Course('Course')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    questions = [q1, q2]
    survey = Survey(questions)
    grouper = AlphaGrouper(4)
    grouping = grouper.make_grouping(c1, survey)
    assert grouping.get_groups()[0].get_members() == [s5, s2, s1, s3]
    assert grouping.get_groups()[1].get_members() == [s6, s4]


def test_alpha_grouper_make_grouping_1() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, 'f')
    s2 = Student(2, 'b')
    s3 = Student(3, 'j')
    s4 = Student(4, 'z')
    s5 = Student(5, 'a')
    s6 = Student(6, 'n')
    c1 = Course('Course')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    questions = [q1, q2]
    survey = Survey(questions)
    grouper = AlphaGrouper(1)
    grouping = grouper.make_grouping(c1, survey)
    assert grouping.get_groups()[0].get_members() == [s5]
    assert grouping.get_groups()[1].get_members() == [s2]
    assert grouping.get_groups()[2].get_members() == [s1]
    assert grouping.get_groups()[3].get_members() == [s3]
    assert grouping.get_groups()[4].get_members() == [s6]
    assert grouping.get_groups()[5].get_members() == [s4]


def test_random_grouper_make_grouping_uneven() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, 'f')
    s2 = Student(2, 'b')
    s3 = Student(3, 'j')
    s4 = Student(4, 'z')
    s5 = Student(5, 'a')
    s6 = Student(6, 'n')
    c1 = Course('Course')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    questions = [q1, q2]
    survey = Survey(questions)
    grouper = RandomGrouper(4)
    grouping = grouper.make_grouping(c1, survey)
    remove_me = [s1, s2, s3, s4, s5, s6]
    assert len(grouping.get_groups()) == 2
    assert len(grouping.get_groups()[0].get_members()) == 4
    assert len(grouping.get_groups()[1].get_members()) == 2
    for group in grouping.get_groups():
        for student in group.get_members():
            remove_me.remove(student)
    assert remove_me == []


def test_random_grouper_make_grouping_even() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    s1 = Student(1, 'f')
    s2 = Student(2, 'b')
    s3 = Student(3, 'j')
    s4 = Student(4, 'z')
    s5 = Student(5, 'a')
    s6 = Student(6, 'n')
    c1 = Course('Course')
    c1.enroll_students([s1, s2, s3, s4, s5, s6])
    questions = [q1, q2]
    survey = Survey(questions)
    grouper = RandomGrouper(3)
    grouping = grouper.make_grouping(c1, survey)
    remove_me = [s1, s2, s3, s4, s5, s6]
    assert len(grouping.get_groups()) == 2
    assert len(grouping.get_groups()[0].get_members()) == 3
    assert len(grouping.get_groups()[1].get_members()) == 3
    for group in grouping.get_groups():
        for student in group.get_members():
            remove_me.remove(student)
    assert remove_me == []


# def test_greedy_find_next_best() -> None:
#     q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
#     q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
#     survey = Survey([q1, q2])
#     s1 = Student(1, '1')
#     a1 = Answer(20)
#     a2 = Answer(0)
#     s2 = Student(2, '2')
#     a3 = Answer(40)
#     a4 = Answer(10)
#     s1.set_answer(q1, a1)
#     s1.set_answer(q2, a2)
#     s2.set_answer(q1, a3)
#     s2.set_answer(q2, a4)
#     s3 = Student(3, '3')
#     a5 = Answer(39)
#     a6 = Answer(9)
#     s4 = Student(4, '4')
#     a7 = Answer(21)
#     a8 = Answer(1)
#     s3.set_answer(q1, a5)
#     s3.set_answer(q2, a6)
#     s4.set_answer(q1, a7)
#     s4.set_answer(q2, a8)
#     s5 = Student(5, '5')
#     a9 = Answer(33)
#     a10 = Answer(4)
#     s6 = Student(6, '6')
#     a11 = Answer(31)
#     a12 = Answer(2)
#     s5.set_answer(q1, a9)
#     s5.set_answer(q2, a10)
#     s6.set_answer(q1, a11)
#     s6.set_answer(q2, a12)
#     lst = [s1, s2, s3, s4, s5, s6]
#     greedy_grouper = GreedyGrouper(4)
#     next_best_group = greedy_grouper._find_next_best(lst, survey)
#     assert next_best_group == [s1, s4, s6, s5]


def test_greedy_grouper_make_grouping() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    survey = Survey([q1, q2])
    s1 = Student(1, '1')
    a1 = Answer(20)
    a2 = Answer(0)
    s2 = Student(2, '2')
    a3 = Answer(40)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    s3 = Student(3, '3')
    a5 = Answer(39)
    a6 = Answer(9)
    s4 = Student(4, '4')
    a7 = Answer(21)
    a8 = Answer(1)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a6)
    s4.set_answer(q1, a7)
    s4.set_answer(q2, a8)
    s5 = Student(5, '5')
    a9 = Answer(33)
    a10 = Answer(4)
    s6 = Student(6, '6')
    a11 = Answer(31)
    a12 = Answer(2)
    s5.set_answer(q1, a9)
    s5.set_answer(q2, a10)
    s6.set_answer(q1, a11)
    s6.set_answer(q2, a12)
    lst = [s1, s2, s3, s4, s5, s6]
    course = Course('A course')
    course.enroll_students(lst)
    greedy_grouper = GreedyGrouper(4)
    grouping1 = greedy_grouper.make_grouping(course, survey)
    group1 = Group([s1, s4, s6, s5])
    group2 = Group([s2, s3])
    grouping2 = Grouping()
    grouping2.add_group(group1)
    grouping2.add_group(group2)
    i = 0
    while i < len(grouping1.get_groups()):
        j = 0
        while j < len(grouping1.get_groups()[i].get_members()):
            assert grouping1.get_groups()[i].get_members()[j] == \
                   grouping2.get_groups()[i].get_members()[j]
            j += 1
        i += 1


# def test_window_grouper_make_group() -> None:
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     s3 = Student(3, '3')
#     s4 = Student(4, '4')
#     s5 = Student(5, '5')
#     s6 = Student(6, '6')
#     lst = [s1, s2, s3, s4, s5, s6]
#     g1 = Grouping()
#     window_grouper = WindowGrouper(4)
#     window_grouper._make_group(2, lst, g1)
#     group = Group([s3, s4, s5, s6])
#     g2 = Grouping()
#     g2.add_group(group)
#     assert len(g1) == len(g2)
#     i = 0
#     while i < len(g1.get_groups()[0].get_members()):
#         assert g1.get_groups()[0].get_members()[i] == \
#                g2.get_groups()[0].get_members()[i]
#         i += 1


# def test_window_grouper_make_group_single() -> None:
#     s1 = Student(1, '1')
#     s2 = Student(2, '2')
#     s3 = Student(3, '3')
#     s4 = Student(4, '4')
#     lst = [s1, s2, s3, s4]
#     g1 = Grouping()
#     window_grouper = WindowGrouper(1)
#     window_grouper._make_group(2, lst, g1)
#     group = Group([s3])
#     g2 = Grouping()
#     g2.add_group(group)
#     assert len(g1) == len(g2)
#     i = 0
#     while i < len(g1.get_groups()[0].get_members()):
#         assert g1.get_groups()[0].get_members()[i] == \
#                g2.get_groups()[0].get_members()[i]
#         i += 1
#

def test_window_grouper_make_grouping_2_even() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    survey = Survey([q1, q2])
    s1 = Student(1, '1')
    a1 = Answer(20)
    a2 = Answer(0)
    s2 = Student(2, '2')
    a3 = Answer(40)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    s3 = Student(3, '3')
    a5 = Answer(39)
    a6 = Answer(9)
    s4 = Student(4, '4')
    a7 = Answer(21)
    a8 = Answer(1)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a6)
    s4.set_answer(q1, a7)
    s4.set_answer(q2, a8)
    s5 = Student(5, '5')
    a9 = Answer(33)
    a10 = Answer(4)
    s6 = Student(6, '6')
    a11 = Answer(31)
    a12 = Answer(2)
    s5.set_answer(q1, a9)
    s5.set_answer(q2, a10)
    s6.set_answer(q1, a11)
    s6.set_answer(q2, a12)
    lst = [s1, s2, s3, s4, s5, s6]
    course = Course('a course')
    course.enroll_students(lst)
    window_grouper = WindowGrouper(2)
    grouping1 = window_grouper.make_grouping(course, survey)
    grouping2 = Grouping()
    group1 = Group([s2, s3])
    group2 = Group([s1, s4])
    group3 = Group([s5, s6])
    grouping2.add_group(group1)
    grouping2.add_group(group2)
    grouping2.add_group(group3)
    i = 0
    while i < len(grouping1):
        j = 0
        while j < len(grouping1.get_groups()[i].get_members()):
            assert grouping1.get_groups()[i].get_members()[j] \
                   == grouping2.get_groups()[i].get_members()[j]
            j += 1
        i += 1


def test_window_grouper_make_grouping_3_even() -> None:
    q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
    q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
    survey = Survey([q1, q2])
    s1 = Student(1, '1')
    a1 = Answer(20)
    a2 = Answer(5)
    s2 = Student(2, '2')
    a3 = Answer(40)
    a4 = Answer(10)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a3)
    s2.set_answer(q2, a4)
    s3 = Student(3, '3')
    a5 = Answer(35)
    a6 = Answer(10)
    s4 = Student(4, '4')
    a7 = Answer(20)
    a8 = Answer(0)
    s3.set_answer(q1, a5)
    s3.set_answer(q2, a6)
    s4.set_answer(q1, a7)
    s4.set_answer(q2, a8)
    s5 = Student(5, '5')
    a9 = Answer(35)
    a10 = Answer(5)
    s6 = Student(6, '6')
    a11 = Answer(30)
    a12 = Answer(0)
    s5.set_answer(q1, a9)
    s5.set_answer(q2, a10)
    s6.set_answer(q1, a11)
    s6.set_answer(q2, a12)
    lst = [s1, s2, s3, s4, s5, s6]
    course = Course('a course')
    course.enroll_students(lst)
    window_grouper = WindowGrouper(3)
    grouping1 = window_grouper.make_grouping(course, survey)
    grouping2 = Grouping()
    group1 = Group([s1, s2, s3])
    group2 = Group([s4, s5, s6])
    grouping2.add_group(group1)
    grouping2.add_group(group2)
    i = 0
    while i < len(grouping1):
        j = 0
        while j < len(grouping1.get_groups()[i].get_members()):
            assert grouping1.get_groups()[i].get_members()[j] \
                   == grouping2.get_groups()[i].get_members()[j]
            j += 1
        i += 1

#
# def test_window_grouper_make_grouping_4_uneven() -> None:
#     q1 = NumericQuestion(1, 'How old is Dylan?', 20, 40)
#     q2 = NumericQuestion(2, 'How much is a Mars bar?', 0, 10)
#     survey = Survey([q1, q2])
#     s1 = Student(1, '1')
#     a1 = Answer(20)
#     a2 = Answer(5)
#     s2 = Student(2, '2')
#     a3 = Answer(40)
#     a4 = Answer(10)
#     s1.set_answer(q1, a1)
#     s1.set_answer(q2, a2)
#     s2.set_answer(q1, a3)
#     s2.set_answer(q2, a4)
#     s3 = Student(3, '3')
#     a5 = Answer(40)
#     a6 = Answer(10)
#     s4 = Student(4, '4')
#     a7 = Answer(35)
#     a8 = Answer(10)
#     s3.set_answer(q1, a5)
#     s3.set_answer(q2, a6)
#     s4.set_answer(q1, a7)
#     s4.set_answer(q2, a8)
#     s5 = Student(5, '5')
#     a9 = Answer(35)
#     a10 = Answer(10)
#     s6 = Student(6, '6')
#     a11 = Answer(20)
#     a12 = Answer(0)
#     s5.set_answer(q1, a9)
#     s5.set_answer(q2, a10)
#     s6.set_answer(q1, a11)
#     s6.set_answer(q2, a12)
#     lst = [s1, s2, s3, s4, s5, s6]
#     course = Course('a course')
#     course.enroll_students(lst)
#     window_grouper = WindowGrouper(4)
#     grouping1 = window_grouper.make_grouping(course, survey)
#     grouping2 = Grouping()
#     group1 = Group([s2, s3, s4, s5])
#     group2 = Group([s1, s6])
#     grouping2.add_group(group1)
#     grouping2.add_group(group2)
#     i = 0
#     while i < len(grouping1):
#         j = 0
#         while j < len(grouping1.get_groups()[i].get_members()):
#             assert grouping1.get_groups()[i].get_members()[j] \
#                    == grouping2.get_groups()[i].get_members()[j]
#             j += 1
#         i += 1


if __name__ == '__main__':
    import pytest

    pytest.main(['tests.py'])


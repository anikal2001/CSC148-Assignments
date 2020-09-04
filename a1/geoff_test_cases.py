import course
import survey
import criterion
import grouper
import pytest
from typing import List, Set, FrozenSet


# TESTS FOR COURSE.PY
# TESTS FOR STUDENT CLASS
def test_str_student() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    assert str(student_one) == 'Geoff Yuen'


def test_has_answer_no_answer() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    assert student_one.has_answer(question) is False


def test_has_answer_invalid_answer_different_type() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer(False)
    student_one.set_answer(question, answer)
    assert student_one.has_answer(question) is False


def test_has_answer_has_answer() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer('Good')
    student_one.set_answer(question, answer)
    assert student_one.has_answer(question) is True


def test_has_answer_different_question_id() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    question_two = survey.MultipleChoiceQuestion(2, 'What is your name?',
                                                 ['No', 'Yes'])
    answer = survey.Answer('Yes')
    student_one.set_answer(question_two, answer)
    assert student_one.has_answer(question) is False


def test_set_answer_valid_answer() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer('Good')
    student_one.set_answer(question, answer)
    assert student_one.has_answer(question) is True


def test_set_answer_invalid_answer() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer(False)
    student_one.set_answer(question, answer)
    assert student_one.get_answer(question) == answer


def test_set_answer_replace_old() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer(False)
    student_one.set_answer(question, answer)
    answer_two = survey.Answer('Bad')
    student_one.set_answer(question, answer_two)
    assert student_one.has_answer(question) is True


def test_get_answer_no_answer() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    student_one = course.Student(1, 'Geoff Yuen')
    assert student_one.get_answer(question) is None


def test_get_answer_invalid_answer() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    student_one = course.Student(1, 'Geoff Yuen')
    answer = survey.Answer(2)
    student_one.set_answer(question, answer)
    assert student_one.get_answer(question) == answer


def test_get_answer_has_answer() -> None:
    student_one = course.Student(1, 'Geoff Yuen')
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer('Good')
    student_one.set_answer(question, answer)
    assert student_one.get_answer(question) == answer


# End of Student Class
###############################################################################
# TESTS FOR COURSE CLASS


def test_helper_get_id() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(2, 'Marian Kondo')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob Dylan')
    course1.enroll_students([student_one, student_two,
                             student_three, student_four])
    assert course1.helper_get_id() == [1, 2, 3, 4]


def test_helper_get_id_no_students() -> None:
    course1 = course.Course('CSC148')
    assert course1.helper_get_id() == []


def test_enroll_students_students() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(2, 'Marian Kondo')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob Dylan')
    list_of_students = [student_one, student_two, student_three, student_four]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == (student_one, student_two,
                                      student_three, student_four)


def test_enroll_students_students_same_id() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(1, 'Marian Kondo')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob Dylan')
    list_of_students = [student_one, student_two, student_three, student_four]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == ()


def test_enroll_students_student_already_in_list() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, 'Geoff Yuen')
    student_three = course.Student(2, 'Charlie Brown')
    list_of_students = [student_one, student_three]
    course1.enroll_students(list_of_students)
    student_two = course.Student(1, 'Marian Kondo')
    list_of_students = [student_two]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == (student_one, student_three)


def test_enroll_students_students_name_is_empty_string() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(2, '')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob Dylan')
    list_of_students = [student_one, student_two, student_three, student_four]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == ()
    course1.enroll_students([student_one, student_three])
    assert course1.get_students() == (student_one, student_three)


def test_all_answered_has_valid_answers_for_all_questions() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(0)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    student_three = course.Student(3, 'Charlie Brown')
    answer1_3 = survey.Answer('Bad')
    answer2_3 = survey.Answer(3)
    answer3_3 = survey.Answer(True)
    answer4_3 = survey.Answer(['Dance', 'Sing'])
    student_three.set_answer(question1, answer1_3)
    student_three.set_answer(question2, answer2_3)
    student_three.set_answer(question3, answer3_3)
    student_three.set_answer(question4, answer4_3)
    list_of_students = [student_one, student_two, student_three]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is True


def test_all_answered_non_unique_answers_for_checkbox_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(0)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie', 'Movie'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_no_answer_for_checkbox_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(0)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer([])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_wrong_answers_for_multiple_choice_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Happy')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(0)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie', 'Dance'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_no_answers_for_multiple_choice_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('')
    answer2_2 = survey.Answer(0)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie', 'Dance'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_more_max_for_numeric_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(7)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie', 'Movie'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_less_min_for_numeric_question() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer2_1 = survey.Answer(2)
    answer3_1 = survey.Answer(False)
    answer4_1 = survey.Answer(['Movie', 'Dance'])
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer2_1)
    student_one.set_answer(question3, answer3_1)
    student_one.set_answer(question4, answer4_1)
    student_two = course.Student(2, 'Marian Kondo')
    answer1_2 = survey.Answer('Bad')
    answer2_2 = survey.Answer(-1)
    answer3_2 = survey.Answer(False)
    answer4_2 = survey.Answer(['Movie', 'Movie'])
    student_two.set_answer(question1, answer1_2)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer3_2)
    student_two.set_answer(question4, answer4_2)
    list_of_students = [student_one, student_two]
    course1.enroll_students(list_of_students)
    assert course1.all_answered(s1) is False


def test_all_answered_no_students() -> None:
    course1 = course.Course('CSC148')
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    question3 = survey.YesNoQuestion(3, 'Happy?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    assert course1.all_answered(s1) is True


def test_get_students_no_students() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(1, '')
    list_of_students = [student_one]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == ()


def test_get_students_reverse_id() -> None:
    course1 = course.Course('CSC148')
    student_one = course.Student(99, 'Geoff Yuen')
    student_two = course.Student(98, 'Marian Kondo')
    student_three = course.Student(10, 'Charlie Brown')
    student_four = course.Student(1, 'Bob Dylan')
    list_of_students = [student_one, student_two, student_three, student_four]
    course1.enroll_students(list_of_students)
    assert course1.get_students() == (student_four,
                                      student_three,
                                      student_two,
                                      student_one)


# End of Course Class
###############################################################################
# TEST CASES FOR SURVEY.PY
# TESTS FOR Question CLASS


def test_is_instance_object() -> None:
    question1 = survey.Question(1, 'How are you?')
    assert isinstance(question1, object) is True


###############################################################################
# TESTS FOR MultipleChoiceQuestion CLASS


def test_is_isinstance_multiple_choice_question() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert isinstance(question1, survey.Question) is True


def test_str_multiple_choice_question() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert 'How are you?' in str(question1)
    assert 'Good' in str(question1)
    assert 'Bad' in str(question1)


def test_validate_answer_multiple_choice_question_invalid_answer() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert question1.validate_answer(survey.Answer(False)) is False
    assert question1.validate_answer(survey.Answer('bad')) is False
    assert question1.validate_answer(survey.Answer(1)) is False


def test_validate_answer_multiple_choice_question_valid_answer() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert question1.validate_answer(survey.Answer('Good')) is True


def test_get_similarity_multiple_choice_question_equal() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert question1.get_similarity(survey.Answer('Good'),
                                    survey.Answer('Good')) == 1.0


def test_get_similarity_multiple_choice_question_not_equal() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    assert question1.get_similarity(survey.Answer('Good'),
                                    survey.Answer('Bad')) == 0.0


# End of MultipleChoiceQuestion Class
###############################################################################
# TESTS for NumericQuestion CLASS


def test_is_isinstance_numeric_question() -> None:
    question1 = survey.NumericQuestion(1, 'How are you?', 1, 2)
    assert isinstance(question1, survey.Question) is True


def test_str_numeric_question() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert 'How old?' in str(question2)
    assert '0' in str(question2)
    assert '3' in str(question2)


def test_validate_answer_numeric_question_valid() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert question2.validate_answer(survey.Answer(2)) is True


def test_validate_answer_numeric_question_invalid() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert question2.validate_answer(survey.Answer(8)) is False


def test_validate_answer_numeric_question_invalid_type_float() -> None:
    question = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert question.validate_answer(survey.Answer(2.5)) is False


def test_get_similarity_numeric_question_max() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert question2.get_similarity(survey.Answer(2),
                                    survey.Answer(2)) == 1.0


def test_get_similarity_numeric_question_similarity_zero() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert question2.get_similarity(survey.Answer(0),
                                    survey.Answer(3)) == 0.0


def test_get_similarity_numeric_question_similarity_some() -> None:
    question2 = survey.NumericQuestion(2, 'How old?', 0, 3)
    assert round(question2.get_similarity(survey.Answer(1),
                                          survey.Answer(2)), 2) == round(2 / 3,
                                                                         2)


# End of NumericQuestion Class
###############################################################################
# TESTS for YesNoQuestion CLASS


def test_str_yes_no_question() -> None:
    question3 = survey.YesNoQuestion(3, 'Happy?')
    assert 'Happy?' in str(question3)
    assert 'True' in str(question3)
    assert 'True' in str(question3)


def test_validate_answer_yes_no_question_valid() -> None:
    question3 = survey.YesNoQuestion(3, 'Happy?')
    assert question3.validate_answer(survey.Answer(False)) is True


def test_validate_answer_yes_no_question_invalid() -> None:
    question3 = survey.YesNoQuestion(3, 'Happy?')
    assert question3.validate_answer(survey.Answer('No')) is False


def test_get_similarity_yes_no_question_equal() -> None:
    question1 = survey.YesNoQuestion(1, 'How are you?')
    assert question1.get_similarity(survey.Answer(True),
                                    survey.Answer(True)) == 1.0


def test_get_similarity_yes_no_question_not_equal() -> None:
    question1 = survey.YesNoQuestion(1, 'How are you?')
    assert question1.get_similarity(survey.Answer(True),
                                    survey.Answer(False)) == 0.0


# End of YesNoQuestion class
###############################################################################
# TESTS for CheckboxQuestion CLASS

def test_str_checkbox_question() -> None:
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert 'Hobbies?' in str(question4)
    assert 'Dance' in str(question4)


def test_validate_answer_checkbox_question_empty_list() -> None:
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert question4.validate_answer(survey.Answer([])) is False


def test_validate_answer_checkbox_question() -> None:
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert question4.validate_answer(survey.Answer(['Movie', 'Sing'])) is True


def test_validate_answer_checkbox_question_unique_answers() -> None:
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert question4.validate_answer(survey.Answer(['Movie', 'Movie'])) is False


def test_helper_get_similarity() -> None:
    question1 = survey.CheckboxQuestion(1, 'How are you?', ['a', 'b', 'c', 'd'])
    answer1 = survey.Answer(['a', 'b', 'c', 'd'])
    answer2 = survey.Answer(['a', 'c'])
    assert question1.helper_get_similarity(answer1, answer2) == 2


def test_get_similarity_checkbox_question_more_unique_than_common() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert question1.get_similarity(survey.Answer(['Movie', 'Sing', 'Dance']),
                                    survey.Answer(['Movie'])) == (1 / 3)


def test_get_similarity_checkbox_question_zero_unique() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    assert question1.get_similarity(survey.Answer(['Movie']),
                                    survey.Answer(['Movie'])) == 1 / 1


def test_get_similarity_checkbox_question_more_common_than_odd() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['a', 'b', 'c', 'd', 'e', 'f'
                                                                  'g', 'h',
                                         'i'])
    assert (question1.get_similarity(survey.Answer(['a', 'b', 'c',
                                                    'd', 'e', 'f', 'g']),
                                     survey.Answer(['a', 'b', 'c', 'd', 'e',
                                                    'f', 'g', 'h', 'i'])) ==
            (7 / 9))


def test_get_similarity_checkbox_question_len_answer1_longer() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['a', 'b', 'c', 'd', 'e', 'f'
                                                                  'g', 'h',
                                         'i'])
    assert question1.get_similarity(survey.Answer(['a', 'b', 'c',
                                                   'd', 'e', 'f', 'g', 'h']),
                                    survey.Answer(['a', 'b', 'c'])) == (3 / 8)


def test_get_similarity_checkbox_question_zero_common() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['a', 'b', 'c', 'd', 'e', 'f'
                                                                  'g', 'h',
                                         'i'])
    assert question1.get_similarity(survey.Answer(['a']),
                                    survey.Answer(['b'])) == 0.0


# End of CheckBoxQuestion class
###############################################################################
# TEST CASES FOR ANSWER class


def test_is_valid() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer('Good')
    assert answer.is_valid(question) is True


def test_is_valid_invalid() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    answer = survey.Answer(False)
    assert answer.is_valid(question) is False


# End of Answer class
################################################################################
# TEST FOR SURVEY CLASS


def test_len() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    question4 = survey.YesNoQuestion(4, 'you?')
    s1 = survey.Survey([question1, question2, question3, question4])
    assert len(s1) == 4


def test_len_empty() -> None:
    s1 = survey.Survey([])
    assert len(s1) == 0


def test_contains() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    question4 = survey.YesNoQuestion(4, 'you?')
    s1 = survey.Survey([question1, question2, question3])
    assert (question4 in s1) is False
    assert (question3 in s1) is True


def test_str() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    s1 = survey.Survey([question1, question2, question3])
    assert 'How are you?' in str(s1)
    assert 'Why are you?' in str(s1)
    assert 'How old?' in str(s1)
    assert '0' in str(s1)
    assert '4' in str(s1)


def test_get_questions() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    s1 = survey.Survey([question1, question2, question3])
    assert s1.get_questions() == [question1, question2, question3]


def test_get_criterion() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    s1 = survey.Survey([question1, question2])
    c1 = criterion.HeterogeneousCriterion()
    assert s1._get_criterion(question1) == s1._default_criterion
    s1.set_criterion(c1, question2)
    assert s1._get_criterion(question2) == c1


def test_get_criterion_set() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    s1 = survey.Survey([question1])
    assert s1.set_criterion(criterion.HeterogeneousCriterion(),
                            question1) is True
    assert s1.set_criterion(criterion.HeterogeneousCriterion(),
                            question2) is False


def test_get_weight() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    question4 = survey.YesNoQuestion(4, 'you?')
    s1 = survey.Survey([question1, question2, question3, question4])
    s1.set_weight(30, question2)
    assert s1._get_weight(question1) == 1
    assert s1._get_weight(question2) == 30


def test_set_weight_occurs() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    s1 = survey.Survey([question1])
    assert s1.set_weight(30, question1) is True
    assert s1.set_weight(30, question2) is False


def test_set_criterion_occurs() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    s1 = survey.Survey([question1])
    c1 = criterion.LonelyMemberCriterion()
    assert s1.set_criterion(c1, question1) is True
    assert s1._get_criterion(question1) == c1


def test_set_criterion_does_not_occurs() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    s1 = survey.Survey([question1])
    assert s1.set_criterion(criterion.LonelyMemberCriterion(),
                            question2) is False


def test_score_student() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    question4 = survey.YesNoQuestion(4, 'you?')
    s1 = survey.Survey([question1, question2, question3, question4])
    s1.set_criterion(criterion.HeterogeneousCriterion(), question2)
    s1.set_criterion(criterion.LonelyMemberCriterion(), question3)
    student_one = course.Student(1, 'Geoff Yuen')
    answer1_1 = survey.Answer('Good')
    answer1_2 = survey.Answer('Good')
    answer1_3 = survey.Answer(0)
    answer1_4 = survey.Answer(True)
    student_one.set_answer(question1, answer1_1)
    student_one.set_answer(question2, answer1_2)
    student_one.set_answer(question3, answer1_3)
    student_one.set_answer(question4, answer1_4)
    student_two = course.Student(2, 'Marian Kondo')
    answer2_1 = survey.Answer('Bad')
    answer2_2 = survey.Answer('Bad')
    answer2_3 = survey.Answer(3)
    answer2_4 = survey.Answer(False)
    student_two.set_answer(question1, answer2_1)
    student_two.set_answer(question2, answer2_2)
    student_two.set_answer(question3, answer2_3)
    student_two.set_answer(question4, answer2_4)
    student_three = course.Student(3, 'Charlie Brown')
    answer3_1 = survey.Answer('Good')
    answer3_2 = survey.Answer('Good')
    answer3_3 = survey.Answer(2)
    answer3_4 = survey.Answer(False)
    student_three.set_answer(question1, answer3_1)
    student_three.set_answer(question2, answer3_2)
    student_three.set_answer(question3, answer3_3)
    student_three.set_answer(question4, answer3_4)
    student_four = course.Student(4, 'Bob')
    answer4_1 = survey.Answer('Good')
    answer4_2 = survey.Answer('Bad')
    answer4_3 = survey.Answer(1)
    answer4_4 = survey.Answer(False)
    student_four.set_answer(question1, answer4_1)
    student_four.set_answer(question2, answer4_2)
    student_four.set_answer(question3, answer4_3)
    student_four.set_answer(question4, answer4_4)
    student_five = course.Student(5, 'Boab')
    answer5_1 = survey.Answer('Good')
    answer5_2 = survey.Answer('Bad')
    answer5_3 = survey.Answer(4)
    answer5_4 = survey.Answer(False)
    student_five.set_answer(question1, answer5_1)
    student_five.set_answer(question2, answer5_2)
    student_five.set_answer(question3, answer5_3)
    student_five.set_answer(question4, answer5_4)
    answer_list1 = [answer1_1, answer2_1, answer3_1, answer4_1, answer5_1]
    answer_list2 = [answer1_2, answer2_2, answer3_2, answer4_2, answer5_2]
    answer_list3 = [answer1_3, answer2_3, answer3_3, answer4_3, answer5_3]
    answer_list4 = [answer1_4, answer2_4, answer3_4, answer4_4, answer5_4]
    s1.set_weight(2, question1)
    s1.set_weight(3, question2)
    value1 = criterion.HomogeneousCriterion().score_answers(question1,
                                                            answer_list1) * 2
    value2 = criterion.HeterogeneousCriterion().score_answers(question2,
                                                              answer_list2) * 3
    value3 = criterion.LonelyMemberCriterion().score_answers(question3,
                                                             answer_list3)
    value4 = criterion.HomogeneousCriterion().score_answers(question4,
                                                            answer_list4)
    total_value = sum([value1, value2, value3, value4]) / 4
    assert s1.score_students(
        [student_one, student_two, student_three, student_four,
         student_five]) == total_value


def test_score_students_invalid_answer_error() -> None:
    q1 = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    q2 = survey.YesNoQuestion(2, 'Is the sky blue?')

    c1 = criterion.HeterogeneousCriterion()

    s1 = survey.Survey([q1, q2])
    s1.set_criterion(c1, q2)

    student1 = course.Student(1, 'Geoff')
    student1_q1 = survey.Answer('Good')
    student1_q2 = survey.Answer(False)
    student1.set_answer(q1, student1_q1)
    student1.set_answer(q2, student1_q2)

    student2 = course.Student(1, 'Geoff')
    student2_q1 = survey.Answer('Bad')
    student2_q2 = survey.Answer('True')
    student2.set_answer(q1, student2_q1)
    student2.set_answer(q2, student2_q2)

    assert s1.score_students([student1, student2]) == 0


def test_score_students_no_questions() -> None:
    q1 = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    q2 = survey.YesNoQuestion(2, 'Is the sky blue?')

    c1 = criterion.HeterogeneousCriterion()

    s1 = survey.Survey([])
    s1.set_criterion(c1, q2)

    student1 = course.Student(1, 'Geoff')
    student1_q1 = survey.Answer('Good')
    student1_q2 = survey.Answer(False)
    student1.set_answer(q1, student1_q1)
    student1.set_answer(q2, student1_q2)

    student2 = course.Student(1, 'Geoff')
    student2_q1 = survey.Answer('Bad')
    student2_q2 = survey.Answer('True')
    student2.set_answer(q1, student2_q1)
    student2.set_answer(q2, student2_q2)

    assert s1.score_students([student1, student2]) == 0


def test_score_grouping_no_groups() -> None:
    grouping_1 = grouper.Grouping()
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.MultipleChoiceQuestion(2, 'Why are you?',
                                              ['Good', 'Bad'])
    question3 = survey.NumericQuestion(3, 'How old?', 0, 4)
    question4 = survey.YesNoQuestion(4, 'you?')
    s1 = survey.Survey([question1, question2, question3, question4])
    assert s1.score_grouping(grouping_1) == 0.0


def test_score_grouping() -> None:
    q1 = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    q2 = survey.YesNoQuestion(2, 'Is the sky blue?')
    q3 = survey.NumericQuestion(3, 'How old are you?', 1, 20)
    s1 = survey.Survey([q1, q2, q3])

    c1 = criterion.LonelyMemberCriterion()
    c2 = criterion.HeterogeneousCriterion()

    s1.set_criterion(c1, q1)
    s1.set_criterion(c2, q3)

    student1 = course.Student(1, 'Geoff')
    student1_q1 = survey.Answer('Good')
    student1_q2 = survey.Answer(True)
    student1_q3 = survey.Answer(14)
    student1.set_answer(q1, student1_q1)
    student1.set_answer(q2, student1_q2)
    student1.set_answer(q3, student1_q3)

    student2 = course.Student(2, 'Marian')
    student2_q1 = survey.Answer('Good')
    student2_q2 = survey.Answer(False)
    student2_q3 = survey.Answer(6)
    student2.set_answer(q1, student2_q1)
    student2.set_answer(q2, student2_q2)
    student2.set_answer(q3, student2_q3)

    student3 = course.Student(3, 'Charlie Brown')
    student3_q1 = survey.Answer('Good')
    student3_q2 = survey.Answer(True)
    student3_q3 = survey.Answer(18)
    student3.set_answer(q1, student3_q1)
    student3.set_answer(q2, student3_q2)
    student3.set_answer(q3, student3_q3)

    student4 = course.Student(4, 'Donald Duck')
    student4_q1 = survey.Answer('Bad')
    student4_q2 = survey.Answer(True)
    student4_q3 = survey.Answer(18)
    student4.set_answer(q1, student4_q1)
    student4.set_answer(q2, student4_q2)
    student4.set_answer(q3, student4_q3)

    small_group1 = grouper.Group([student1, student2])
    small_group2 = grouper.Group([student3, student4])

    big_group = grouper.Grouping()
    big_group.add_group(small_group1)
    big_group.add_group(small_group2)

    assert round(s1.score_students([student1, student2]), 2) == 0.47
    assert round(s1.score_students([student3, student4]), 2) == 0.33
    assert round(s1.score_grouping(big_group), 2) == 0.4


# End of Survey class
###############################################################################
# TEST CASES FOR CRITERION.PY
# score answers for each criterion type and also each type of question


def test_criterion_score_answers_homo_one_answer() -> None:
    question1 = survey.MultipleChoiceQuestion(1, 'How are you?',
                                              ['Good', 'Bad'])
    question2 = survey.NumericQuestion(2, 'How are you?', 0, 20)
    question3 = survey.YesNoQuestion(3, 'How are you?')
    question4 = survey.CheckboxQuestion(4, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1, question2, question3, question4])
    s1.set_criterion(criterion.HomogeneousCriterion(), question1)
    s1.set_criterion(criterion.HomogeneousCriterion(), question2)
    s1.set_criterion(criterion.HomogeneousCriterion(), question3)
    s1.set_criterion(criterion.HomogeneousCriterion(), question4)
    answer1 = survey.Answer('Good')
    answer2 = survey.Answer(2)
    answer3 = survey.Answer(False)
    answer4 = survey.Answer(['Movie', 'Sing'])
    assert (criterion.HomogeneousCriterion().score_answers(question1,
                                                           [answer1]) == 1.0)
    assert (criterion.HomogeneousCriterion().score_answers(question2,
                                                           [answer2]) == 1.0)
    assert (criterion.HomogeneousCriterion().score_answers(question3,
                                                           [answer3]) == 1.0)
    assert (criterion.HomogeneousCriterion().score_answers(question4,
                                                           [answer4]) == 1.0)


def test_criterion_score_answers_hetero_multiple_choice_question() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    s1 = survey.Survey([question])
    s1.set_criterion(criterion.HeterogeneousCriterion(), question)
    student_one = course.Student(1, 'Geoff Yuen')
    answer = survey.Answer('Good')
    student_one.set_answer(question, answer)
    student_two = course.Student(2, 'Marian Kondo')
    answer2 = survey.Answer('Bad')
    student_two.set_answer(question, answer2)
    student_three = course.Student(3, 'Charlie Brown')
    answer3 = survey.Answer('Good')
    student_three.set_answer(question, answer3)
    student_four = course.Student(4, 'Bob')
    answer4 = survey.Answer('Good')
    student_four.set_answer(question, answer4)
    student_five = course.Student(5, 'Boab')
    answer5 = survey.Answer('Good')
    student_five.set_answer(question, answer5)
    answer_list = [answer, answer2, answer3, answer4, answer5]
    assert question.get_similarity(answer, answer2) == 0.0
    assert question.get_similarity(answer3, answer4) == 1.0
    assert criterion.HeterogeneousCriterion().score_answers(question,
                                                            answer_list) == 4 / 10


def test_criterion_score_answers_homo_multiple_choice_question() -> None:
    question = survey.MultipleChoiceQuestion(1, 'How are you?', ['Good', 'Bad'])
    s1 = survey.Survey([question])
    s1.set_criterion(criterion.HomogeneousCriterion(), question)
    student_one = course.Student(1, 'Geoff Yuen')
    answer = survey.Answer('Good')
    student_one.set_answer(question, answer)
    student_two = course.Student(2, 'Marian Kondo')
    answer2 = survey.Answer('Bad')
    student_two.set_answer(question, answer2)
    student_three = course.Student(3, 'Charlie Brown')
    answer3 = survey.Answer('Good')
    student_three.set_answer(question, answer3)
    student_four = course.Student(4, 'Bob')
    answer4 = survey.Answer('Good')
    student_four.set_answer(question, answer4)
    student_five = course.Student(5, 'Boab')
    answer5 = survey.Answer('Good')
    student_five.set_answer(question, answer5)
    answer_list = [answer, answer2, answer3, answer4, answer5]
    assert question.get_similarity(answer, answer2) == 0.0
    assert question.get_similarity(answer3, answer4) == 1.0
    assert criterion.HomogeneousCriterion().score_answers(question,
                                                          answer_list) == 6 / 10


def test_criterion_score_answers_homo_numeric_question() -> None:
    c1 = criterion.HomogeneousCriterion()
    question1 = survey.NumericQuestion(1, 'How are you?', 0, 20)
    answer1 = survey.Answer(1)
    answer2 = survey.Answer(5)
    answer_list = [answer1, answer2]
    assert c1.score_answers(question1, answer_list) == 0.8


def test_criterion_score_answers_hetero_numeric_question() -> bool:
    c1 = criterion.HeterogeneousCriterion()
    question1 = survey.NumericQuestion(1, 'How are you?', 0, 20)
    answer1 = survey.Answer(1)
    answer2 = survey.Answer(5)
    answer_list = [answer1, answer2]
    assert round(c1.score_answers(question1, answer_list), 2) == 0.2


def test_criterion_score_answers_lonely_member_numeric_question() -> bool:
    c1 = criterion.LonelyMemberCriterion()
    question1 = survey.NumericQuestion(1, 'How are you?', 0, 20)
    answer1 = survey.Answer(1)
    answer2 = survey.Answer(5)
    answer_list = [answer1, answer2]
    assert c1.score_answers(question1, answer_list) == 0


def test_criterion_score_answers_lonely_member_numeric_question_else() -> bool:
    c1 = criterion.LonelyMemberCriterion()
    question1 = survey.NumericQuestion(1, 'How are you?', 0, 20)
    answer1 = survey.Answer(1)
    answer2 = survey.Answer(19)
    answer3 = survey.Answer(1)
    answer_list = [answer1, answer2, answer3]
    assert c1.score_answers(question1, answer_list) == 0


def test_criterion_score_answers_lonely_member_numeric_question_want_one() -> bool:
    c1 = criterion.LonelyMemberCriterion()
    question1 = survey.NumericQuestion(1, 'How are you?', 0, 20)
    answer1 = survey.Answer(1)
    answer2 = survey.Answer(1)
    answer_list = [answer1, answer2]
    assert c1.score_answers(question1, answer_list) == 1


def test_criterion_score_answers_homo_checkbox_question() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1])
    s1.set_criterion(criterion.HomogeneousCriterion(), question1)
    answer1 = survey.Answer(['Movie', 'Sing'])
    answer2 = survey.Answer(['Sing', 'Dance', 'Game'])
    answer3 = survey.Answer(['Dance', 'Game'])
    answer4 = survey.Answer(['Movie', 'Game'])
    answer_list = [answer1, answer2, answer3, answer4]
    assert round(question1.get_similarity(answer1, answer2), 2) == round(1 / 4,
                                                                         2)
    assert question1.get_similarity(answer1, answer3) == 0.0
    assert round(question1.get_similarity(answer1, answer4), 2) == round(1 / 3,
                                                                         2)
    assert round(question1.get_similarity(answer2, answer3), 2) == round(2 / 3,
                                                                         2)
    assert round(question1.get_similarity(answer2, answer4), 2) == round(1 / 4,
                                                                         2)
    assert round(question1.get_similarity(answer3, answer4), 2) == round(1 / 3,
                                                                         2)
    assert (round(criterion.HomogeneousCriterion().score_answers(question1,
                                                                 answer_list),
                  2)
            == round(11 / 36, 2))


def test_criterion_score_answers_homo_checkbox_question() -> None:
    question1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                        ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([question1])
    s1.set_criterion(criterion.HomogeneousCriterion(), question1)
    answer1 = survey.Answer(['Movie', 'Sing'])
    assert (criterion.HomogeneousCriterion().score_answers(question1,
                                                           [answer1]) == 1.0)


# End of Criterion class
###############################################################################
# TEST CASES FOR GROUPER.PY
# TESTS FOR HELPERS


def test_slice_list() -> None:
    pass
    # assert grouper.slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    # assert grouper.slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0],
    #                                                        [False]]
    # assert grouper.slice_list([3, 4, 5, 2, 3, 2], 2) == [[3, 4], [5, 2], [3, 2]]
    # assert grouper.slice_list([3, 4], 2) == [[3, 4]]
    # assert grouper.slice_list([1, 2, 3], 0) == []
    # assert grouper.slice_list([], -1) == []
    # assert grouper.slice_list([3, 4, 5], 1) == [[3], [4], [5]]


def test_windows() -> None:
    assert grouper.windows([3, 4, 6, 2, 3], 2) == [[3, 4], [4, 6], [6, 2],
                                                   [2, 3]]
    assert grouper.windows(['a', 1, 6.0, False], 3) == [['a', 1, 6.0],
                                                        [1, 6.0, False]]
    assert grouper.windows([1, 2, 3], 3) == [[1, 2, 3]]
    assert grouper.windows([1, 2, 3], 0) == []
    assert grouper.windows([1, 2, 3], 1) == [[1], [2], [3]]
    assert grouper.windows([1, 2, 3], -1) == []


# End of helpers
###############################################################################
# TEST FOR ALPHA GROUPER CLASS


def test_alpha_make_grouping() -> None:
    # already alphabetical order
    c1 = course.Course('CSC148')
    q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                 ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([q1])
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(2, 'Marian Kondo')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob')
    student_five = course.Student(5, 'Boab')
    c1.enroll_students([student_one, student_two, student_three,
                        student_four, student_five])
    a1 = grouper.AlphaGrouper(2)
    grouping1 = grouper.Grouping()
    group1 = grouper.Group([student_five, student_four])
    group2 = grouper.Group([student_three, student_one])
    group3 = grouper.Group([student_two])
    grouping1.add_group(group1)
    grouping1.add_group(group2)
    grouping1.add_group(group3)
    assert a1.make_grouping(c1, s1).get_groups()[0].get_members() \
           == group1.get_members()
    assert len(a1.make_grouping(c1, s1).get_groups()[0]) == \
           len(a1.make_grouping(c1, s1).get_groups()[1])


# End of Alpha Grouper Class
###############################################################################
# TEST FOR RANDOM GROUPER CLASS


def test_random_make_grouping() -> None:
    c1 = course.Course('CSC148')
    q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                 ['Movie', 'Sing', 'Dance', 'Game'])
    s1 = survey.Survey([q1])
    student_one = course.Student(1, 'Geoff Yuen')
    student_two = course.Student(2, 'Marian Kondo')
    student_three = course.Student(3, 'Charlie Brown')
    student_four = course.Student(4, 'Bob')
    student_five = course.Student(5, 'Boab')
    c1.enroll_students([student_one, student_two, student_four, student_five])
    a2 = grouper.RandomGrouper(2)
    random_grouping_first = a2.make_grouping(c1, s1)
    assert str(a2.make_grouping(c1, s1).get_groups()) != str(
        random_grouping_first.get_groups())


# End of Random Grouper Class
###############################################################################
# TEST FOR GREEDY GROUPER CLASS


def test_helper_find_max() -> None:
    group = grouper.GreedyGrouper(2)
    temp = [course.Student(1, 'Geoff')]
    student1 = course.Student(2, 'Marian')
    student_lst = [student1]
    q1 = survey.MultipleChoiceQuestion(1, 'How are you', ['Good', 'Bad'])
    student1.set_answer(q1, survey.Answer('Good'))
    s1 = survey.Survey([q1])
    assert group.helper_find_max(student_lst, s1, temp) is None


def test_greedy_make_grouping() -> None:
    c1 = course.Course('CSC148')
    q1 = survey.YesNoQuestion(1, 'Happy?')
    s1 = survey.Survey([q1])
    s1.set_criterion(criterion.LonelyMemberCriterion(), q1)
    student_one = course.Student(1, 'Geoff Yuen')
    answer1 = survey.Answer(False)
    student_one.set_answer(q1, answer1)
    student_two = course.Student(2, 'Marian Kondo')
    answer2 = survey.Answer(True)
    student_two.set_answer(q1, answer2)
    student_three = course.Student(3, 'Charlie Brown')
    answer3 = survey.Answer(False)
    student_three.set_answer(q1, answer3)
    student_four = course.Student(4, 'Bob')
    answer4 = survey.Answer(False)
    student_four.set_answer(q1, answer4)
    student_five = course.Student(5, 'Boab')
    answer5 = survey.Answer(False)
    student_five.set_answer(q1, answer5)
    c1.enroll_students([student_one, student_two, student_three,
                        student_four, student_five])
    a3 = grouper.GreedyGrouper(2)
    grouping1 = grouper.Grouping()
    group1 = grouper.Group([student_one, student_three])
    group2 = grouper.Group([student_two, student_four])
    group3 = grouper.Group([student_five])
    grouping1.add_group(group1)
    grouping1.add_group(group2)
    grouping1.add_group(group3)
    assert a3.make_grouping(c1, s1).get_groups()[
               0].get_members() == group1.get_members()


# End of Greedy Grouper Class
###############################################################################
# TEST FOR WINDOW GROUPER CLASS


def test_window_make_grouping() -> bool:
    c1 = course.Course('CSC148')
    q1 = survey.YesNoQuestion(1, 'Happy?')
    s1 = survey.Survey([q1])
    s1.set_criterion(criterion.LonelyMemberCriterion(), q1)
    student_one = course.Student(1, 'Geoff Yuen')
    answer1 = survey.Answer(False)
    student_one.set_answer(q1, answer1)
    student_two = course.Student(2, 'Marian Kondo')
    answer2 = survey.Answer(True)
    student_two.set_answer(q1, answer2)
    student_three = course.Student(3, 'Charlie Brown')
    answer3 = survey.Answer(False)
    student_three.set_answer(q1, answer3)
    student_four = course.Student(4, 'Bob')
    answer4 = survey.Answer(False)
    student_four.set_answer(q1, answer4)
    student_five = course.Student(5, 'Boab')
    answer5 = survey.Answer(False)
    student_five.set_answer(q1, answer5)
    c1.enroll_students([student_one, student_two, student_three,
                        student_four, student_five])
    a3 = grouper.WindowGrouper(2)
    grouping1 = grouper.Grouping()
    group1 = grouper.Group([student_one, student_three])
    group2 = grouper.Group([student_two, student_four])
    group3 = grouper.Group([student_five])
    grouping1.add_group(group1)
    grouping1.add_group(group2)
    grouping1.add_group(group3)
    group1_mem = a3.make_grouping(c1, s1).get_groups()[0].get_members()
    group2_mem = group1.get_members()


# End of WindowGrouper
################################################################################
# TEST CASES FOR GROUP.PY


def test_len_group() -> bool:
    g1 = grouper.Group([course.Student(1, 'Geoff Yuen'),
                        course.Student(2, 'Marian Kondo')])
    assert len(g1) == 2


def test_contains_group() -> bool:
    s1 = course.Student(1, 'Geoff Yuen')
    s2 = course.Student(2, 'Marian Kondo')
    s3 = course.Student(1, 'Charlie Brown')
    g1 = grouper.Group([s1, s2])
    assert (s1 in g1) is True
    assert (s3 in g1) is True


def test_str_single_line() -> bool:
    g1 = grouper.Group([course.Student(1, 'Geoff Yuen'),
                        course.Student(2, 'Marian Kondo')])
    assert 'Geoff Yuen' in str(g1) and 'Marian Kondo' in str(g1)


def test_get_members() -> bool:
    s1 = course.Student(1, 'Geoff Yuen')
    s2 = course.Student(2, 'Marian Kondo')
    g1 = grouper.Group([])
    assert g1.get_members() == []
    g1 = grouper.Group([s1, s2])
    assert g1.get_members() == [s1, s2]


# End of Group class
###############################################################################
# TEST FOR GROUPING CLASS


def test_len_grouping() -> bool:
    stud = grouper.Grouping()
    assert len(stud) == 0
    g1 = grouper.Group([course.Student(1, 'Geoff')])
    stud.add_group(g1)
    assert len(stud) == 1


def test_str_grouping() -> bool:
    stud = grouper.Grouping()
    g1 = grouper.Group(
        [course.Student(1, 'Geoff'), course.Student(2, 'Marian')])
    stud.add_group(g1)
    assert ('Geoff' in str(stud))
    assert ('Marian' in str(stud))


def test_helper_every_member_list() -> bool:
    stud = grouper.Grouping()
    s1 = course.Student(1, 'Geoff')
    s2 = course.Student(2, 'Marian')
    group = grouper.Group([s1, s2])
    stud.add_group(group)
    assert stud.helper_every_member_list() == [s1, s2]


def test_add_group_group_contains_zero_members() -> bool:
    grouping = grouper.Grouping()
    g1 = grouper.Group([])
    assert grouping.add_group(g1) == False


def test_add_group_student_appears_in_more_than_one_group_in_groups() -> bool:
    grouping = grouper.Grouping()
    g1 = grouper.Group([course.Student(1, 'Geoff')])
    assert grouping.add_group(g1) == True
    g2 = grouper.Group([course.Student(1, 'Marian')])
    assert grouping.add_group(g2) == False
    g3 = grouper.Group([course.Student(1, 'Geoff')])
    assert grouping.add_group(g3) == False


def test_get_groups() -> bool:
    stud = grouper.Grouping()
    s1 = course.Student(1, 'Geoff')
    g1 = grouper.Group([s1])
    assert stud.get_groups() == []
    stud.add_group(g1)
    assert stud.get_groups() == [g1]


# End of Grouping class
###############################################################################

if __name__ == '__main__':
    pytest.main(['tests.py'])
